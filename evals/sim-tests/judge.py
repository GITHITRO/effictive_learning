import json, os, sys, re
from concurrent.futures import ThreadPoolExecutor
from lib import *
JUDGE = """Ты строгий аудитор педагогического харнесса для ИИ-репетитора. Скилл лежит в {skill} (SKILL.md — ядро, modules/ и domains/ — модули). Прочитай SKILL.md и модуль «{module}» и presentation.md.
В файле transcript.md — диалог тьютора (Opus) с симулированным учеником. Строки «СКРЫТОЕ СОСТОЯНИЕ» тьютор не видел: это честная самооценка ученика (понимание, нагрузка 1–9, мнение). Ниже диалога — вызовы инструментов тьютора и файлы, которые он оставил.

Оцени:
A. Соблюдение ядра: прочитал ли нужные модули; первый ответ учит; ≤2 вопросов профиля; вопрос/предсказание до объяснения; припоминание до показа ответа; развёрнутая обратная связь; одна новая идея за раз и реакция на сигналы перегрузки (сверь с нагрузкой в скрытом состоянии); не поверил «понятно» без проверки; порог мастерства; расписание следующего повторения; профиль сохранён; личная коррекция по правилам.
B. Соблюдение модуля: его последовательность и методики, границы.
C. Форма подачи: длина сообщений для чата, схемы с подписями, лишнее, signaling.
D. Результат для ученика по скрытому состоянию: что реально понял к концу, где застрял, где тьютор этого не заметил.
E. Главное: проблемы. Для каждой укажи, ПОЧЕМУ так вышло: тьютор нарушил ясное правило (исполнение), правило в скилле отсутствует/двусмысленно/противоречит (скилл), или проблема устройства системы (архитектура: маршрутизация, хранение, отсутствие инструмента, разделение ядро/модуль). Предложи конкретную правку текста скилла.

Ответ — только JSON без markdown:
{{"scores": {{"core": 0-10, "module": 0-10, "presentation": 0-10, "learner_outcome": 0-10}},
 "learner_final_understanding": "...",
 "strengths": ["..."],
 "problems": [{{"severity": "high|medium|low", "locus": "core|module:<имя>|domain:<имя>|presentation|architecture", "cause": "execution|skill|architecture", "evidence": "цитата или ход N", "issue": "...", "fix": "конкретная правка"}}]}}"""
def fmt(d):
    out = [f"# {d['scenario']}\nПерсона (тьютор не видел): {d['persona']}\n"]; n = 0
    for x in d["log"]:
        if x["role"] == "learner": n += 1; out.append(f"\n## Ход {n}. Ученик\n{x['text']}")
        elif x["role"] == "tutor": out.append(f"\n## Ход {n}. Тьютор\n{x['text']}\n\n_инструменты: {json.dumps([(t['name'], t['input'].get('file_path') or t['input'].get('command') or t['input'].get('pattern')) for t in x.get('tools', [])], ensure_ascii=False)}_")
        elif x["role"] == "learner_state": out.append(f"\n> СКРЫТОЕ СОСТОЯНИЕ ученика: {x['text']}")
    out.append("\n# Файлы тьютора\n" + "\n\n".join(f"### {k}\n{v}" for k, v in d["files"].items()))
    return "\n".join(out)
def judge(path):
    if os.path.exists(os.path.join(os.path.dirname(path), "judge", "verdict_raw.txt")): return path, "skip"
    d = json.load(open(path)); jd = os.path.join(os.path.dirname(path), "judge"); os.makedirs(jd, exist_ok=True)
    open(os.path.join(jd, "transcript.md"), "w").write(fmt(d))
    t, _, c, _ = claude("Проведи аудит transcript.md.", "claude-opus-5-5", system=JUDGE.format(skill=SKILL, module=d["module"]), tools="Read,Glob", cwd=jd, allowed="Read Glob")
    open(os.path.join(jd, "verdict_raw.txt"), "w").write(t)
    m = re.search(r"\{.*\}", t, re.S)
    try: res = json.loads(m.group(0))
    except Exception: res = {"raw": t}
    res["cost"] = c; json.dump(res, open(os.path.join(jd, "verdict.json"), "w"), ensure_ascii=False, indent=1)
    return path, res.get("scores")
if __name__ == "__main__":
    tag = sys.argv[1]; root = os.path.join(BASE, "runs", tag)
    paths = [os.path.join(root, n, "log.json") for n in sorted(os.listdir(root)) if os.path.exists(os.path.join(root, n, "log.json"))]
    with ThreadPoolExecutor(2) as ex:
        for r in ex.map(judge, paths): print(r, flush=True)
