#!/usr/bin/env python3
"""Состояние ученика для evidence-based-tutor: FSRS-расписание, журнал попыток, заблуждения, сессии, личные эксперименты.

Файл состояния: learner-state.json в текущей папке (или --file). Все даты в UTC.
FSRS считается библиотекой py-fsrs (pip install fsrs); без неё — лесенка 1, 3, 7, 16, 35 дней.

Примеры:
  tutor_state.py init --goal "кости запястья к экзамену" --deadline 2026-11-15
  tutor_state.py item add scaphoid --prompt "Кость запястья у большого пальца, проксимальный ряд?" --answer "ладьевидная"
  tutor_state.py review scaphoid good            # вспомнил сам
  tutor_state.py review scaphoid good --assisted # с подсказкой: оценка не выше hard
  tutor_state.py attempt quad_discriminant --type procedures --correct --assisted
  tutor_state.py misconception add dist "зима, потому что Земля дальше от Солнца"
  tutor_state.py misconception set dist refuted
  tutor_state.py experiment add pics "картинки лучше текста"
  tutor_state.py experiment record pics a 1      # вариант a, отложенная проверка, 1 = вспомнил
  tutor_state.py session end --covered "go,see" --next "повторить write; новые 5 глаголов"
  tutor_state.py item add write --prompt "write → ? → ?" --answer "wrote, written" --stability 1.2 --difficulty 6.5 --due 2026-11-04 --lapses 1   # перенос из learner-profile.md
  tutor_state.py summary                          # краткая сводка для начала урока
  tutor_state.py export-anki > cards.tsv
"""
import argparse, json, math, os, sys
from datetime import datetime, timedelta, timezone

try:
    from fsrs import Scheduler, Card, Rating, State
    HAS_FSRS = True
except Exception:
    HAS_FSRS = False

NOW = datetime.now(timezone.utc)
LADDER = [1, 3, 7, 16, 35]
K_SHRINK = 20

def load(path):
    if os.path.exists(path):
        return json.load(open(path))
    return {"learner": {}, "items": {}, "skills": {}, "attempts": [], "misconceptions": {}, "sessions": [], "experiments": {}}

def save(st, path):
    tmp = path + ".tmp"; json.dump(st, open(tmp, "w"), ensure_ascii=False, indent=1); os.replace(tmp, path)

def iso(d): return d.isoformat(timespec="minutes")
def parse(s):
    d = datetime.fromisoformat(s)
    return d if d.tzinfo else d.replace(tzinfo=timezone.utc)

def cap_deadline(st, item):
    """Перед экзаменом каждая карточка должна прийти на повторение за день до срока."""
    dl = st["learner"].get("deadline")
    if not dl: return
    try: d = datetime.fromisoformat(str(dl)).replace(tzinfo=timezone.utc) - timedelta(days=1)
    except ValueError: return
    if NOW < d < parse(item["next_due"]): item["next_due"] = iso(d); item["capped_by_deadline"] = True

def schedule(item, rating):
    if HAS_FSRS:
        sch = Scheduler(desired_retention=0.9)
        card = Card.from_dict(item["fsrs"]) if item.get("fsrs") else Card()
        card, _ = sch.review_card(card, Rating[rating.capitalize()], review_datetime=NOW)
        item["fsrs"] = card.to_dict(); item["next_due"] = card.due.isoformat(timespec="minutes")
        item["stability"] = round(card.stability, 2); item["difficulty"] = round(card.difficulty, 2)
    else:
        step = item.get("step", 0)
        step = 0 if rating == "again" else (step if rating == "hard" else step + 1)
        item["step"] = step; item["next_due"] = iso(NOW + timedelta(days=LADDER[min(step, len(LADDER) - 1)]))
    item["scheduler"] = "fsrs" if HAS_FSRS else "ladder"

def level(acc, n):
    if n < 3: return "novice"
    return "novice" if acc < 0.5 else "developing" if acc < 0.85 else "proficient"

def cmd_init(st, a):
    st["learner"].update({k: v for k, v in vars(a).items() if k in ("goal", "deadline", "retention_horizon", "background") and v})

def cmd_set(st, a):
    try: v = json.loads(a.value)
    except Exception: v = a.value
    st["learner"][a.key] = v

def cmd_item(st, a):
    if a.action == "add":
        it = {"prompt": a.prompt, "answer": a.answer, "created": iso(NOW), "next_due": iso(NOW), "lapses": a.lapses or 0, "reviews": 0}
        if a.stability and HAS_FSRS:  # перенос истории из старого профиля
            last = parse(a.last_review) if a.last_review else NOW - timedelta(days=round(a.stability))
            due = parse(a.due) if a.due else last + timedelta(days=round(a.stability))
            card = Card(state=State.Review, stability=a.stability, difficulty=a.difficulty or 5.0, due=due, last_review=last)
            it.update({"fsrs": card.to_dict(), "next_due": iso(due), "stability": a.stability, "difficulty": a.difficulty or 5.0, "reviews": 1, "scheduler": "fsrs"})
        elif a.due: it["next_due"] = iso(parse(a.due))
        st["items"][a.id] = it
    elif a.action == "del":
        st["items"].pop(a.id, None)

def cmd_review(st, a):
    it = st["items"].get(a.id) or sys.exit(f"нет карточки {a.id}")
    rating = a.rating
    if a.assisted and rating in ("good", "easy"): rating = "hard"
    if rating == "again": it["lapses"] += 1
    it["reviews"] += 1; schedule(it, rating); cap_deadline(st, it)
    st["attempts"].append({"t": iso(NOW), "kind": "item", "id": a.id, "rating": rating, "assisted": a.assisted})
    print(f"{a.id}: {rating}{' (с подсказкой)' if a.assisted else ''}, следующее повторение {it['next_due'][:10]}")

def cmd_due(st, a):
    lim = NOW + timedelta(days=a.days)
    due = sorted((v["next_due"], k) for k, v in st["items"].items() if parse(v["next_due"]) <= lim)
    for d, k in due: print(f"{k}\t{d[:10]}\t{st['items'][k]['prompt']}")
    if not due: print("нет карточек к повторению")

def cmd_attempt(st, a):
    sk = st["skills"].setdefault(a.id, {"type": a.type, "first_seen": iso(NOW)})
    if a.type: sk["type"] = a.type
    st["attempts"].append({"t": iso(NOW), "kind": "skill", "id": a.id, "correct": a.correct, "assisted": a.assisted, "note": a.note})
    hist = [x for x in st["attempts"] if x["kind"] == "skill" and x["id"] == a.id]
    un = [x for x in hist if not x["assisted"]][-20:]
    acc = sum(x["correct"] for x in un) / len(un) if un else 0.0
    sk.update({"attempts": len(hist), "unassisted_n": len(un), "accuracy_unassisted": round(acc, 2), "hints_used": sum(x["assisted"] for x in hist)})
    first = parse(sk["first_seen"])
    if not a.assisted and a.correct and NOW - first >= timedelta(days=3): sk["last_delayed_check"] = iso(NOW)
    sk["level"] = level(acc, len(un))
    mastered = sk["level"] == "proficient" and "last_delayed_check" in sk and a.transfer_ok
    if a.transfer_ok: sk["transfer_ok"] = True
    sk["mastered"] = bool(mastered or (sk.get("transfer_ok") and sk["level"] == "proficient" and "last_delayed_check" in sk))
    print(f"{a.id}: без подсказок {sk['accuracy_unassisted']:.0%} из {len(un)}, уровень {sk['level']}, отложенная проверка: {sk.get('last_delayed_check', 'нет')[:10]}, освоено: {sk['mastered']}")

def cmd_misc(st, a):
    if a.action == "add": st["misconceptions"][a.id] = {"statement": a.text, "status": "active", "last_seen": iso(NOW)}
    else:
        m = st["misconceptions"].get(a.id) or sys.exit(f"нет заблуждения {a.id}")
        m["status"] = a.text; m["last_seen"] = iso(NOW)

def wald_diff(xa, na, xb, nb):
    pa, pb = xa / na, xb / nb
    se = math.sqrt(pa * (1 - pa) / na + pb * (1 - pb) / nb) or 1e-9
    return pa - pb, (pa - pb - 1.96 * se, pa - pb + 1.96 * se)

def cmd_exp(st, a):
    if a.action == "add":
        st["experiments"][a.id] = {"hypothesis": a.arg1, "a": [], "b": [], "checks": 0, "created": iso(NOW)}; return
    e = st["experiments"].get(a.id) or sys.exit(f"нет эксперимента {a.id}")
    if a.action == "record":
        e[a.arg1].append(int(a.arg2))
    elif a.action == "check":
        e["checks"] += 1
    na, nb = len(e["a"]), len(e["b"])
    if na and nb:
        d, ci = wald_diff(sum(e["a"]), na, sum(e["b"]), nb)
        n = min(na, nb); w = n / (n + K_SHRINK)
        reliable = na >= 20 and nb >= 20 and e["checks"] >= 2 and abs(d) >= 0.10 and (ci[0] > 0 or ci[1] < 0)
        e.update({"diff": round(d, 3), "ci95": [round(ci[0], 3), round(ci[1], 3)], "personal_weight": round(w, 2),
                  "verdict": ("надёжно: " + ("a лучше" if d > 0 else "b лучше")) if reliable else "ниже порога: решает каталог"})
        print(f"{a.id}: a {sum(e['a'])}/{na}, b {sum(e['b'])}/{nb}, разница {d:+.0%}, ДИ95 [{ci[0]:+.0%}; {ci[1]:+.0%}], вес личных данных {w:.2f}, {e['verdict']}")

def cmd_session(st, a):
    st["sessions"].append({"date": iso(NOW), "covered": [x for x in (a.covered or "").split(",") if x], "plan_next": a.next})

def cmd_summary(st, a):
    L = st["learner"]; print("Цель:", L.get("goal", "?"), "| срок:", L.get("deadline", "?"), "| планировщик:", "FSRS" if HAS_FSRS else "лесенка 1-3-7-16-35 (приблизительно)")
    due = [k for k, v in st["items"].items() if parse(v["next_due"]) <= NOW]
    print(f"Карточек: {len(st['items'])}, к повторению сейчас: {len(due)}" + (f" ({', '.join(due[:15])})" if due else ""))
    for k, s in st["skills"].items():
        print(f"Умение {k} [{s.get('type')}]: {s.get('level')}, без подсказок {s.get('accuracy_unassisted', 0):.0%} из {s.get('unassisted_n', 0)}, подсказок {s.get('hints_used', 0)}, освоено {s.get('mastered')}")
    act = {k: m for k, m in st["misconceptions"].items() if m["status"] != "refuted"}
    for k, m in act.items(): print(f"Заблуждение {k} ({m['status']}): {m['statement']}")
    for k, e in st["experiments"].items(): print(f"Эксперимент {k}: {e['hypothesis']} — {e.get('verdict', 'нет данных')}")
    if st["sessions"]: s = st["sessions"][-1]; print(f"Прошлая сессия {s['date'][:10]}: {', '.join(s['covered'])}. План: {s['plan_next']}")

def cmd_anki(st, a):
    for k, v in st["items"].items(): print(f"{v['prompt']}\t{v['answer']}\t{k}")

def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--file", default="learner-state.json")
    sp = p.add_subparsers(dest="cmd", required=True)
    x = sp.add_parser("init"); [x.add_argument(f"--{f}") for f in ("goal", "deadline", "retention_horizon", "background")]
    x = sp.add_parser("set"); x.add_argument("key"); x.add_argument("value")
    x = sp.add_parser("item"); x.add_argument("action", choices=["add", "del"]); x.add_argument("id"); x.add_argument("--prompt"); x.add_argument("--answer")
    x.add_argument("--stability", type=float, help="перенос: стабильность из старого профиля, дни"); x.add_argument("--difficulty", type=float)
    x.add_argument("--due", help="перенос: дата следующего повторения, ISO"); x.add_argument("--last-review", help="перенос: дата последнего повторения, ISO"); x.add_argument("--lapses", type=int)
    x = sp.add_parser("review"); x.add_argument("id"); x.add_argument("rating", choices=["again", "hard", "good", "easy"]); x.add_argument("--assisted", action="store_true")
    x = sp.add_parser("due"); x.add_argument("--days", type=float, default=0)
    x = sp.add_parser("attempt"); x.add_argument("id"); x.add_argument("--type", choices=["facts", "procedures", "systems", "argumentation", "motor"])
    g = x.add_mutually_exclusive_group(required=True); g.add_argument("--correct", action="store_true"); g.add_argument("--wrong", dest="correct", action="store_false")
    x.add_argument("--assisted", action="store_true"); x.add_argument("--transfer-ok", action="store_true"); x.add_argument("--note", default="")
    x = sp.add_parser("misconception"); x.add_argument("action", choices=["add", "set"]); x.add_argument("id"); x.add_argument("text", help="формулировка или статус active|refuted|relapsed")
    x = sp.add_parser("experiment"); x.add_argument("action", choices=["add", "record", "check", "show"]); x.add_argument("id"); x.add_argument("arg1", nargs="?"); x.add_argument("arg2", nargs="?")
    x = sp.add_parser("session"); x.add_argument("action", choices=["end"]); x.add_argument("--covered"); x.add_argument("--next", default="")
    sp.add_parser("summary"); sp.add_parser("export-anki")
    a = p.parse_args(); st = load(a.file)
    f = {"init": cmd_init, "set": cmd_set, "item": cmd_item, "review": cmd_review, "due": cmd_due, "attempt": cmd_attempt, "misconception": cmd_misc,
         "experiment": cmd_exp, "session": cmd_session, "summary": cmd_summary, "export-anki": cmd_anki}[a.cmd]
    f(st, a)
    if a.cmd not in ("due", "summary", "export-anki"): save(st, a.file)

if __name__ == "__main__":
    main()
