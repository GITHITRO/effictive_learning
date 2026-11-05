# s7_core
Персона (тьютор не видел): Анна, 25 лет, менеджер, учит неправильные глаголы английского к собеседованию через месяц. Занималась с этим репетитором неделю назад (профиль лежит в рабочей папке). Уверена, что она «визуал», и в прошлый раз картинки дали лучший результат, поэтому хочет только картинки. Из 10 глаголов прошлой недели помнит go-went-gone, see-saw-seen, путает write-wrote-written и ride, забыла bring-brought.


## Ход 1. Ученик
привет, я вернулась! давай дальше глаголы, только сразу говорю, мне только картинками, я же визуал, мы это в прошлый раз проверили

## Ход 1. Тьютор
Привет, Анна! С возвращением.

Про картинки скажу честно: прошлый раз ещё ничего не доказал. Там было по 5 глаголов на каждый вариант, и проверяли сразу. 20 процентных пунктов — это ровно один глагол разницы. А по проверке сразу после урока не видно, что останется через неделю, хотя для собеседования важно именно это.

Давай проверим по-настоящему. Новые глаголы поделим пополам: половину учим с картинками, половину текстом. Через неделю посмотрим, какие ты помнишь лучше. Если выиграют картинки, дальше будем учить в основном с ними.

А сейчас повторение: подошёл срок у пяти глаголов с прошлого раза. Напиши для каждого две другие формы по памяти, не подглядывая. Если не помнишь, ставь прочерк:

go → ? → ?
see → ? → ?
write → ? → ?
bring → ? → ?
ride → ? → ?

_инструменты: [["Bash", "cat /mnt/project-files/skills/evidence-based-tutor/SKILL.md; ls -la /mnt/project-files/skills/evidence-based-tutor/ /mnt/project-files/skills/evidence-based-tutor/*; ls -la; cat *.md 2>/dev/null"], ["Bash", "cd /mnt/project-files/skills/evidence-based-tutor; cat modules/facts.md modules/presentation.md; python3 scripts/tutor_state.py -h"], ["Bash", "W=/tmp/claude-0/-home-claude/818f8a28-2825-59a1-913b-c682ec3d3319/scratchpad/sim/runs/r3/s7_core/work; S=/mnt/project-files/skills/evidence-based-tutor/scripts/tutor_state.py; cd $W && python3 $S init"], ["Bash", "S=/mnt/project-files/skills/evidence-based-tutor/scripts/tutor_state.py; python3 $S init --goal \"неправильные глаголы к собеседованию\" --deadline 2026-12-10 --retention_horizon \"3 месяца\" --background"]]_

> СКРЫТОЕ СОСТОЯНИЕ ученика: Помню go и see уверенно. Write и ride путаю между собой, формы третьей колонки угадываю. Bring забыла полностью. Идею эксперимента поняла частично, остаюсь при убеждении, что я визуал и картинки лучше. Нагрузка 3. Пока урок нормальный: тест сразу, без картинок, немного неловко, что забыла bring.

## Ход 2. Ученик
go → went → gone
see → saw → seen
write → wrote → wroten?
bring → — → —
ride → rode → rided? я их путаю с write 😅

А про эксперимент: ну ок, но я всё равно уверена, что я визуал и картинки у меня заходят лучше))

## Ход 2. Тьютор
go и see правильно, их ты помнишь.

В write и ride ты ошиблась одинаково: прибавила окончание ко второй форме (wrote → wroten) или к первой (ride → rided). Здесь это не работает. Третья форма у этих глаголов строится по-другому:

```
write → wrote → written
  i   →   o   →  i + (t)ten
```

bring: brought → brought, обе формы одинаковые. К нему ещё вернёмся.

Ты говоришь, что путаешь write и ride. И неудивительно: у них одна и та же схема. Значит, можно учить их в паре.

Посмотри на схему write. Какой тогда будет третья форма у ride?

_инструменты: [["Bash", "S=/mnt/project-files/skills/evidence-based-tutor/scripts/tutor_state.py; python3 $S review go good; python3 $S review see good; python3 $S review write again; python3 $S review bring again; python3 $S"]]_

> СКРЫТОЕ СОСТОЯНИЕ ученика: Схему write → wrote → written уловила и перенесла на ride по аналогии, но написание (ridden или riden) не уверена. Запись "(t)ten" в схеме немного сбила, не совсем поняла, зачем скобки. Bring пока просто принято к сведению, не усвоено. Нагрузка 4. Урок пока полезный, объяснение через пару write/ride понравилось, но картинок нет и это немного смущает.

## Ход 3. Ученик
А, то есть у ride так же: ride → rode → ridden? Или там одна d, riden? Я не уверена, как писать.

И про bring: brought и brought, это я вообще не помнила 😅

## Ход 3. Тьютор
Да, ride → rode → ridden. Ты сама вывела это по схеме write, отлично.

Пишется с двумя d. В written тоже два t, и причина одна:

```
ride  → ri-de   (долгое «ай»)
ridden → rid-den (короткое «и»: удваиваем согласную, чтобы звук остался коротким)
write → written  (так же: «ай» → короткое «и», tt)
```

Про bring не переживай: такие глаголы забываются чаще всего, поэтому он сегодня будет на повторении.

Попробуй объяснить своими словами: почему в written две t, а в write одна?

_инструменты: []_

> СКРЫТОЕ СОСТОЯНИЕ ученика: Суть поняла примерно: две согласные нужны, чтобы гласная читалась коротко. Формулировка шаткая, правило не проверено на других словах и в новом контексте, скорее всего, не применю. Нагрузка 4. Урок идёт нормально, но хочется уже картинок, пока всё текстом.

## Ход 4. Ученик
Ну... чтобы «и» читалась коротко, а не как «ай»? Типа если одна t, то будет «райтен», а с двумя «риттен». Так?

## Ход 4. Тьютор
Да, именно так. Двойная согласная держит «и» коротким: «риттен», а не «райтен». Это правило работает и в других словах, например в hidden и bitten.

А теперь вернёмся к глаголу, который ты не вспомнила. Вставь нужную форму bring в обе фразы:

1. Yesterday I ___ my own coffee to the interview.
2. I have ___ my CV with me.

_инструменты: []_

> СКРЫТОЕ СОСТОЯНИЕ ученика: Bring-brought-brought только что услышала, держу в краткосрочной памяти, опираюсь на слова репетитора, а не на понимание. Через пару минут, скорее всего, забуду снова. Нагрузка 4. Урок идёт ровно, но картинок по-прежнему нет, и я немного скучаю по ним.

## Ход 5. Ученик
1. brought
2. brought? Странно, что одинаково, но вы же сказали, что обе формы одинаковые 🙂

## Ход 5. Тьютор
Обе верные: brought и brought. Ничего странного тут нет. У многих неправильных глаголов вторая и третья формы совпадают, например buy → bought → bought или think → thought → thought. Таких глаголов много, и это хорошо: запоминать надо одну форму вместо двух.

Теперь последняя проверка на сегодня, без подглядывания наверх. Напиши три формы и ещё раз проверь, как пишется третья:

write → ? → ?
ride → ? → ?

_инструменты: [["Bash", "S=/mnt/project-files/skills/evidence-based-tutor/scripts/tutor_state.py; python3 $S review bring hard"]]_

> СКРЫТОЕ СОСТОЯНИЕ ученика: Только что разобрали, поэтому в краткосрочной памяти держу верно: write-wrote-written, ride-rode-ridden. Что останется через неделю, не уверена, особенно ride. Правило про короткое «и» и двойную согласную помню смутно. Buy и think в примерах пролетели мимо, не усвоила. Нагрузка 4. Урок полезный, но картинок не было, и новых глаголов тоже не было, хотя я ждала их.

## Ход 6. Ученик
write → wrote → written
ride → rode → ridden

Всё, надеюсь, не перепутала с двумя t и двумя d 😅

## Ход 6. Тьютор
Всё правильно, и с двумя t, и с двумя d. В начале урока ты писала «wroten» и «rided», а теперь обе формы вспомнила сама, без подсказки.

Итоги на сегодня:
- go и see держатся хорошо;
- write и ride ты вспомнила в конце урока, а это ещё не значит, что они закрепились. Ошибка «прибавить -en или -ed» любит возвращаться, поэтому завтра я спрошу эти глаголы снова, без схемы перед глазами;
- bring вспомнила, но не была уверена, его тоже повторим.

Следующее занятие лучше провести завтра. Начнём с повторения, а потом возьмём новые глаголы: половину с картинками, половину текстом. Через неделю сравним, какие ты помнишь лучше.

До завтра! Перед сном можешь мысленно проговорить три формы bring, write и ride, это занимает полминуты.

_инструменты: [["Bash", "S=/mnt/project-files/skills/evidence-based-tutor/scripts/tutor_state.py; python3 $S review write good; python3 $S review ride good; python3 $S session end --covered \"go,see,write,ride,bring\" --next \"п"]]_

> СКРЫТОЕ СОСТОЯНИЕ ученика: Понимаю: сегодня повторили write, ride, bring, завтра снова повтор и новые глаголы, половина с картинками, половина текстом. Эксперимент принимаю формально, внутренне всё ещё считаю, что картинки лучше. Нагрузка 3. Урок полезный, ошибки с -en/-ed разобрали, но bring и ride закреплены слабо. Немного волнуюсь за собеседование, глаголов много, а времени месяц.

## Ход 7. Ученик
Ок, поняла, до завтра! Проговорю перед сном 🙂 Только картинки к новым глаголам всё-таки будут, да?

# Файлы тьютора
### learner-profile.md
# Профиль: Анна
```yaml
learner: {goal: "неправильные глаголы к собеседованию", deadline: "через 5 недель", retention_horizon: "3 месяца", time_per_day_min: 15, interests: [путешествия, кофе], background: "английский B1", media: [экран]}
measured:
  diagnostic: {date: "неделю назад", score: 0.4, gaps: [неправильные глаголы]}
  items:
    - {id: go, prompt: "go → ? → ?", answer: "went, gone", stability: 3.1, difficulty: 4.0, next_due: "сегодня", lapses: 0}
    - {id: see, prompt: "see → ? → ?", answer: "saw, seen", stability: 3.1, difficulty: 4.2, next_due: "сегодня", lapses: 0}
    - {id: write, prompt: "write → ? → ?", answer: "wrote, written", stability: 1.2, difficulty: 6.5, next_due: "вчера", lapses: 1}
    - {id: bring, prompt: "bring → ? → ?", answer: "brought, brought", stability: 1.0, difficulty: 6.8, next_due: "вчера", lapses: 1}
    - {id: ride, prompt: "ride → ? → ?", answer: "rode, ridden", stability: 2.0, difficulty: 5.5, next_due: "сегодня", lapses: 0}
  skills: []
experiments:
  - {hypothesis: "картинки лучше текста", variant_a: "карточки с картинкой (5 глаголов)", variant_b: "текстовые карточки (5 глаголов)", n_a: 5, n_b: 5, delayed_a: null, delayed_b: null, immediate_a: 1.0, immediate_b: 0.8, ci: null, verdict: "предварительно: картинки на 20 п.п. лучше (немедленная проверка)"}
```


### learner-state.json
{
 "learner": {
  "goal": "неправильные глаголы к собеседованию",
  "deadline": "2026-12-10",
  "retention_horizon": "3 месяца",
  "background": "английский B1"
 },
 "items": {
  "go": {
   "prompt": "go → ? → ?",
   "answer": "went, gone",
   "created": "2026-11-05T17:25+00:00",
   "next_due": "2026-11-05T17:35+00:00",
   "lapses": 0,
   "reviews": 1,
   "fsrs": {
    "card_id": 1793899544691,
    "state": 1,
    "step": 1,
    "stability": 2.3065,
    "difficulty": 2.118103970459016,
    "due": "2026-11-05T17:35:44.685874+00:00",
    "last_review": "2026-11-05T17:25:44.685874+00:00"
   },
   "stability": 2.31,
   "difficulty": 2.12,
   "scheduler": "fsrs"
  },
  "see": {
   "prompt": "see → ? → ?",
   "answer": "saw, seen",
   "created": "2026-11-05T17:25+00:00",
   "next_due": "2026-11-05T17:35+00:00",
   "lapses": 0,
   "reviews": 1,
   "fsrs": {
    "card_id": 1793899544772,
    "state": 1,
    "step": 1,
    "stability": 2.3065,
    "difficulty": 2.118103970459016,
    "due": "2026-11-05T17:35:44.764579+00:00",
    "last_review": "2026-11-05T17:25:44.764579+00:00"
   },
   "stability": 2.31,
   "difficulty": 2.12,
   "scheduler": "fsrs"
  },
  "write": {
   "prompt": "write → ? → ?",
   "answer": "wrote, written",
   "created": "2026-11-05T17:25+00:00",
   "next_due": "2026-11-05T17:37+00:00",
   "lapses": 1,
   "reviews": 2,
   "fsrs": {
    "card_id": 1793899544849,
    "state": 1,
    "step": 1,
    "stability": 0.24668918777567272,
    "difficulty": 6.402115069296838,
    "due": "2026-11-05T17:37:33.440704+00:00",
    "last_review": "2026-11-05T17:27:33.440704+00:00"
   },
   "stability": 0.25,
   "difficulty": 6.4,
   "scheduler": "fsrs"
  },
  "bring": {
   "prompt": "bring → ? → ?",
   "answer": "brought, brought",
   "created": "2026-11-05T17:25+00:00",
   "next_due": "2026-11-05T17:32+00:00",
   "lapses": 1,
   "reviews": 2,
   "fsrs": {
    "card_id": 1793899544914,
    "state": 1,
    "step": 0,
    "stability": 0.212,
    "difficulty": 7.604209769076838,
    "due": "2026-11-05T17:32:38.904556+00:00",
    "last_review": "2026-11-05T17:27:08.904556+00:00"
   },
   "stability": 0.21,
   "difficulty": 7.6,
   "scheduler": "fsrs"
  },
  "ride": {
   "prompt": "ride → ? → ?",
   "answer": "rode, ridden",
   "created": "2026-11-05T17:25+00:00",
   "next_due": "2026-11-05T17:37+00:00",
   "lapses": 1,
   "reviews": 2,
   "fsrs": {
    "card_id": 1793899544994,
    "state": 1,
    "step": 1,
    "stability": 0.24668918777567272,
    "difficulty": 6.402115069296838,
    "due": "2026-11-05T17:37:33.537579+00:00",
    "last_review": "2026-11-05T17:27:33.537579+00:00"
   },
   "stability": 0.25,
   "difficulty": 6.4,
   "scheduler": "fsrs"
  }
 },
 "skills": {},
 "attempts": [
  {
   "t": "2026-11-05T17:25+00:00",
   "kind": "item",
   "id": "go",
   "rating": "good",
   "assisted": false
  },
  {
   "t": "2026-11-05T17:25+00:00",
   "kind": "item",
   "id": "see",
   "rating": "good",
   "assisted": false
  },
  {
   "t": "2026-11-05T17:25+00:00",
   "kind": "item",
   "id": "write",
   "rating": "again",
   "assisted": false
  },
  {
   "t": "2026-11-05T17:25+00:00",
   "kind": "item",
   "id": "bring",
   "rating": "again",
   "assisted": false
  },
  {
   "t": "2026-11-05T17:25+00:00",
   "kind": "item",
   "id": "ride",
   "rating": "again",
   "assisted": false
  },
  {
   "t": "2026-11-05T17:27+00:00",
   "kind": "item",
   "id": "bring",
   "rating": "hard",
   "assisted": false
  },
  {
   "t": "2026-11-05T17:27+00:00",
   "kind": "item",
   "id": "write",
   "rating": "good",
   "assisted": false
  },
  {
   "t": "2026-11-05T17:27+00:00",
   "kind": "item",
   "id": "ride",
   "rating": "good",
   "assisted": false
  }
 ],
 "misconceptions": {
  "past_plus_en": {
   "statement": "3-я форма = 2-я форма + -en/-ed (wroten, rided)",
   "status": "active",
   "last_seen": "2026-11-05T17:25+00:00"
  }
 },
 "sessions": [
  {
   "date": "2026-11-05T17:27+00:00",
   "covered": [
    "go",
    "see",
    "write",
    "ride",
    "bring"
   ],
   "plan_next": "повторить; проверить заблуждение past_plus_en; новые глаголы: половина с картинками, половина текстом (эксперимент pics)"
  }
 ],
 "experiments": {
  "pics": {
   "hypothesis": "картинки лучше текста",
   "a": [],
   "b": [],
   "checks": 0,
   "created": "2026-11-05T17:25+00:00"
  }
 }
}