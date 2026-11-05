import json, os, sys, shutil
from concurrent.futures import ThreadPoolExecutor
from lib import *
from scenarios import S
LEARNER_MODEL = "claude-sonnet-5-5"
HOOK = bool(os.environ.get("SIM_HOOK"))
def run(name, tutor_model="claude-opus-5-5", max_turns=8, tag="r1"):
    sc = S[name]; wd = os.path.join(BASE, "runs", tag, name, "work"); shutil.rmtree(wd, ignore_errors=True); os.makedirs(wd)
    for fn, txt in sc.get("setup", {}).items(): open(os.path.join(wd, fn), "w").write(txt)
    tsys = TUTOR_SYS.format(skill=SKILL, extra=sc.get("extra", ""))
    lsys = LEARNER_RULES.format(persona=sc["persona"])
    tools = sc.get("tools", "Read,Write,Edit,Glob,Bash")
    log = []; ts = ls = None; cost = 0; msg = sc["opening"]
    for turn in range(max_turns):
        log.append({"role": "learner", "text": msg, "state": log[-1]["_state"] if False else None})
        t, ts, c, tc = claude(msg, tutor_model, system=tsys, session=ts, tools=tools, cwd=wd, allowed=tools.replace(",", " "), hook=HOOK); cost += c
        log.append({"role": "tutor", "text": t, "tools": tc})
        if turn == max_turns - 1: break
        l, ls, c, _ = claude("Репетитор: " + t, LEARNER_MODEL, system=lsys, session=ls); cost += c
        clean, state = split_state(l)
        log.append({"role": "learner_state", "text": state})
        end = "[КОНЕЦ]" in clean; msg = clean.replace("[КОНЕЦ]", "").strip()
        if end:
            log.append({"role": "learner", "text": msg}); break
    files = {f: open(os.path.join(wd, f)).read()[:6000] for f in os.listdir(wd) if os.path.isfile(os.path.join(wd, f))}
    out = {"scenario": name, "module": sc["module"], "tutor_model": tutor_model, "learner_model": LEARNER_MODEL, "persona": sc["persona"], "cost": cost, "log": [x for x in log if x.get("text") is not None], "files": files}
    json.dump(out, open(os.path.join(BASE, "runs", tag, name, "log.json"), "w"), ensure_ascii=False, indent=1)
    return name, cost, len(log)
if __name__ == "__main__":
    tag = sys.argv[1]; names = sys.argv[2].split(",") if len(sys.argv) > 2 else list(S)
    with ThreadPoolExecutor(7) as ex:
        for r in ex.map(lambda n: run(n, tag=tag), names): print(r, flush=True)
