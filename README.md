# effictive_learning

Скиллы и плагины, по которым ИИ-агент учит человека фактам и умениям по доказательной методике: припоминание до ответа, интервальные повторения (FSRS), развёрнутая обратная связь, разобранные примеры, порог мастерства и профиль учащегося. В набор попадают только методики с контролируемыми исследованиями, эффектом на отложенном тесте и известными границами применения.

Сейчас здесь один плагин, **evidence-based-tutor** (версия 0.6.0).

## Структура

```
.claude-plugin/marketplace.json     каталог плагинов этого репозитория
plugins/evidence-based-tutor/
  .claude-plugin/plugin.json        манифест плагина (версия здесь)
  hooks/hooks.json                  Stop-хук: линтер хода тьютора
  skills/evidence-based-tutor/
    SKILL.md                        ядро: маршрутизация, основа, профиль, ход в чате
    modules/                        по типу знания: facts, procedures, systems,
                                    argumentation, motor, presentation
    domains/                        по предмету: programming, languages, history,
                                    economics, _template
    scripts/                        tutor_state.py (FSRS, журнал), check_turn.py, stop_hook.py
evals/
  sim-tests/                        симуляции: тьютор + ученик-персона + судья, отчёт и логи
  test-runs/                        ручные прогоны «со скиллом / без скилла»
  live-test/                        протокол живого теста на людях (без ключей ответов)
docs/reviewer.html                  обзор для ревьюера
tools/build.sh                      сборка zip-архивов в dist/
```

## Установка

**Claude Code, из этого репозитория:**

```
/plugin marketplace add GITHITRO/effictive_learning
/plugin install evidence-based-tutor@effictive-learning
```

Stop-хук срабатывает только в папке урока, где есть `learner-state.json` или `learner-profile.md`.

**claude.ai:** скачайте `evidence-based-tutor-skill-<версия>.zip` из [Releases](../../releases) и загрузите его в разделе скиллов. Для скриптов нужно включить выполнение кода.

Собрать архивы локально: `tools/build.sh` (нужны `python3` и `zip`).

## Как проверяем

1. **Симуляции** (`evals/sim-tests/`): тьютор со скиллом занимается с учеником-персоной со скрытым состоянием, судья оценивает диалог по рубрике. Итоги и найденные проблемы в [REPORT.md](evals/sim-tests/REPORT.md). Запуск требует Claude Code CLI: `cd evals/sim-tests && python3 run_sim.py <tag> [сценарии]`, затем `judge.py`.
2. **Живой тест** (`evals/live-test/`): внутрисубъектное сравнение «со скиллом / без скилла» с проверками сразу, на 7-й и 30-й день. Вопросы и ключи в репозиторий не кладутся, пока тест идёт.

## Участие

Как предлагать правки, добавлять предметы и модули, читайте в [CONTRIBUTING.md](CONTRIBUTING.md). Агентам: правила работы в [CLAUDE.md](CLAUDE.md).
