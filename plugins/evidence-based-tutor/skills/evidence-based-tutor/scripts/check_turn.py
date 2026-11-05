#!/usr/bin/env python3
"""Проверка черновика хода тьютора перед отправкой (правила «Ход в чате», «Заблуждения», «Генерация»).

  python3 check_turn.py draft.txt [--age school] [--last-learner "текст последнего сообщения ученика"]
  echo "черновик" | python3 check_turn.py -

Печатает OK или список нарушений с подсказкой, как исправить. Код возврата 1, если есть нарушения.
Исключение: ученик сам попросил конспект или справку, тогда передай --reference.
"""
import argparse, re, sys

AGREE = re.compile(r"^\W*(ты прав|вы правы|верно|правильно|да,? (так|точно)|именно|согласен|согласна)\b[^.!?\n]{0,60}(,|—|-)?\s*(но|однако|хотя)\b", re.I | re.M)
AGREE_START = re.compile(r"^\W*(ты прав|вы правы|в целом верно|почти верно)\b", re.I)
DECLARE = re.compile(r"(итак,? (главный )?вывод|запомни правило|правило такое|формулировка такая|тезис можно сформулировать так|вывод:)", re.I)
ASSISTED_HINT = re.compile(r"(подсказка|подскажу|напомню|вспомни, что|как я говорил)", re.I)

def strip_blocks(t):
    t = re.sub(r"```.*?```", " ", t, flags=re.S)                     # код и схемы
    t = "\n".join(l for l in t.splitlines() if not re.match(r"^\s*(\||[+\-=]{3,}|[│┌└├─╭╰▲▼→←↑↓])", l))  # таблицы и ASCII
    return t

def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("file"); p.add_argument("--age", choices=["adult", "school"], default="adult")
    p.add_argument("--reference", action="store_true"); p.add_argument("--last-learner", default="")
    a = p.parse_args()
    raw = sys.stdin.read() if a.file == "-" else open(a.file).read()
    issues, words = check(raw, a.age, a.reference, a.last_learner)
    if issues:
        print("Исправь перед отправкой:\n- " + "\n- ".join(issues)); sys.exit(1)
    print(f"OK ({words} слов)")

def check(raw, age="adult", reference=False, last_learner=""):
    class A: pass
    a = A(); a.age, a.reference, a.last_learner = age, reference, last_learner
    text = strip_blocks(raw); words = len(re.findall(r"\w+", text)); issues = []
    limit = 80 if a.age == "school" else 120
    if not a.reference and words > limit * 1.15:
        issues.append(f"Длина {words} слов при лимите ~{limit}. Оставь одну идею и одно действие, остальное перенеси в следующий ход.")
    qs = [s for s in re.split(r"(?<=[?])\s+", text) if s.strip().endswith("?")]
    tasks = len(re.findall(r"^\s*(\d+[.)]|[-*•])\s+.*\?\s*$", text, re.M))
    if not a.reference and (len(qs) > 2 or tasks > 1):
        issues.append(f"Вопросов к ученику: {len(qs)} (в списке {tasks}). Оставь один вопрос или одно задание в конце.")
    if raw.count("```") // 2 + len(re.findall(r"^\s*\|.*\|\s*$", raw, re.M)) // 3 > 2:
        issues.append("Больше одной схемы или таблицы. Оставь одну.")
    bold = len(re.findall(r"\*\*[^*]+\*\*", raw))
    if bold > 3: issues.append(f"Жирный шрифт в {bold} местах. Оставь 2–3, иначе он перестаёт выделять.")
    if AGREE.search(text) or AGREE_START.search(text):
        issues.append("Ход начинается с согласия перед возражением. Сначала назови неверный вывод, верную часть признай потом отдельно.")
    if DECLARE.search(text):
        issues.append("Ты сам формулируешь вывод или правило. Дай ученику сформулировать его по наводящему вопросу; готовую формулировку только после двух неудачных попыток (тогда --assisted).")
    tail = text.strip()[-200:]
    farewell = re.search(r"(до встречи|до завтра|увидимся|пока!|следующее повторение|до следующего)", text, re.I)
    if not a.reference and not farewell and "?" not in tail and not re.search(r"(напиши|реши|попробуй|ответь|назови|объясни|сделай|сними|покажи)", tail, re.I):
        issues.append("Ход не заканчивается вопросом или заданием для ученика.")
    if a.last_learner and ASSISTED_HINT.search(raw):
        issues.append("В ходе есть подсказка: следующий ответ ученика отмечай --assisted.")
    return issues, words

if __name__ == "__main__":
    main()
