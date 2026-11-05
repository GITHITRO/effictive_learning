#!/usr/bin/env python3
"""Stop-хук Claude Code: проверяет итоговое сообщение тьютора через check_turn и один раз возвращает его на доработку.

Подключается плагином (hooks/hooks.json). Срабатывает только в папке, где есть learner-state.json или learner-profile.md,
то есть во время урока, и не мешает обычной работе.
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check_turn import check

def last_assistant_text(path):
    text = ""
    for line in open(path):
        try: e = json.loads(line)
        except Exception: continue
        if e.get("type") == "user" and isinstance(e.get("message", {}).get("content"), str): text = ""
        if e.get("type") == "assistant":
            parts = [c.get("text", "") for c in e.get("message", {}).get("content", []) if c.get("type") == "text"]
            if parts: text = "\n".join(parts)
    return text

def main():
    data = json.load(sys.stdin)
    if data.get("stop_hook_active"): return
    cwd = data.get("cwd") or os.getcwd()
    if not os.environ.get("TUTOR_LESSON") and not any(os.path.exists(os.path.join(cwd, f)) for f in ("learner-state.json", "learner-profile.md")): return
    text = last_assistant_text(data["transcript_path"])
    if not text: return
    age = "school" if os.environ.get("TUTOR_AGE") == "school" else "adult"
    issues, words = check(text, age=age)
    if issues:
        print(json.dumps({"decision": "block", "reason": "Это сообщение уйдёт ученику. Перепиши его целиком (без упоминания проверки), исправив:\n- " + "\n- ".join(issues)}, ensure_ascii=False))

if __name__ == "__main__":
    main()
