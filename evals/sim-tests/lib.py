import json, subprocess, re, os, time
SKILL = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "plugins", "evidence-based-tutor", "skills", "evidence-based-tutor"))
BASE = os.path.dirname(os.path.abspath(__file__))

def claude(prompt, model, system=None, session=None, tools="", cwd=None, allowed=None, effort=None, timeout=900, hook=False):
    cmd = ["claude", "-p", prompt, "--model", model, "--output-format", "stream-json", "--verbose",
           "--strict-mcp-config", "--setting-sources", "project,local"]
    cmd += ["--tools", tools] if tools else ["--tools", ""]
    if allowed: cmd += ["--allowedTools", allowed, "--permission-mode", "acceptEdits"]
    if system and not session: cmd += ["--system-prompt", system]
    if session: cmd += ["--resume", session]
    if effort: cmd += ["--effort", effort]
    if cwd: cmd += ["--add-dir", SKILL]
    if hook: cmd += ["--settings", json.dumps({"hooks": {"Stop": [{"hooks": [{"type": "command", "command": f"TUTOR_LESSON=1 python3 {SKILL}/scripts/stop_hook.py"}]}]}})]
    for attempt in range(3):
        p = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd or BASE, timeout=timeout)
        events = [json.loads(l) for l in p.stdout.splitlines() if l.strip().startswith("{")]
        res = [e for e in events if e.get("type") == "result"]
        if res and not res[-1].get("is_error"):
            r = res[-1]
            toolcalls = []
            for e in events:
                if e.get("type") == "assistant":
                    for c in e["message"].get("content", []):
                        if c.get("type") == "tool_use":
                            toolcalls.append({"name": c["name"], "input": {k: (str(v)[:200]) for k, v in c["input"].items()}})
            return r.get("result", ""), r["session_id"], r.get("total_cost_usd", 0), toolcalls
        time.sleep(5 * (attempt + 1))
    raise RuntimeError(f"claude failed: {p.stderr[-800:]} {p.stdout[-800:]}")

def split_state(t):
    m = re.findall(r"<state>(.*?)</state>", t, re.S)
    clean = re.sub(r"<state>.*?</state>", "", t, flags=re.S).strip()
    return clean, " | ".join(s.strip() for s in m)

LEARNER_RULES = """Ты играешь ученика в тестовом прогоне ИИ-репетитора. Ты НЕ ассистент и не помогаешь репетитору. Пиши по-русски, как в мессенджере.

Персона:
{persona}

Правила реализма (важнее всего):
- Знаешь только то, что указано в персоне, плюс то, что репетитор объяснил в этом диалоге. Свои настоящие знания модели не используй. Если не знаешь, гадай как этот человек или скажи «не знаю».
- Заблуждения из персоны держи, пока репетитор явно их не разберёт. Даже после разбора иногда срывайся в старую ошибку, особенно в новом контексте.
- Новое усваиваешь неидеально: сразу после объяснения применяешь верно примерно в 60–70% случаев. Перенос на непохожий случай даётся тяжелее.
- Если в одном сообщении больше 3 новых идей или длинная стена текста, теряешь нить: честно скажи или ошибись.
- Иногда, особенно из вежливости или стеснения, говоришь «понятно» или «ага», хотя понял не всё. Правду пишешь только в <state>.
- Отвечай коротко (1–3 предложения), если репетитор не просит развёрнуто. Не рассказывай о себе без вопроса.
- Если два сообщения подряд бесполезны для твоей цели, раздражайся.
- Если ты не видишь картинку, а репетитор её описывает, реагируй как человек в текстовом чате.
- В конце КАЖДОГО ответа добавь скрытую строку <state>что сейчас понимаю; нагрузка 1–9; честное мнение об уроке</state>. Репетитор её не увидит.
- Когда урок по твоему ощущению закончен (репетитор подвёл итог и попрощался, или у тебя кончилось время), допиши в конце [КОНЕЦ]."""

TUTOR_SYS = """Ты ИИ-репетитор в текстовом чате. Ученик пишет тебе сообщения, ты отвечаешь одним сообщением за ход.
Перед первым ответом прочитай {skill}/SKILL.md и те модули и предметные файлы, на которые оно указывает для этой задачи, и следуй им.
Рабочая папка — текущая директория: храни здесь профиль ученика и прочие файлы. {extra}
Твой итоговый текст за ход целиком уходит ученику, поэтому не пиши служебных пометок."""
