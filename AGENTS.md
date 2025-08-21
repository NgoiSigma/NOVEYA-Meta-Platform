---

```markdown
# AGENTS.md — FDL-GROMADA-NOVEYA

> Инструкция для ИИ-агентов и разработчиков. Репозиторий содержит ядро FDL-Громады: компилятор, граф-движок, FastAPI для живой коммуникации агентов, спецификацию языка и манифест. См. перечень в README.  

---

## 0) Приоритет источников
1) Явные указания пользователя в текущем чате/задаче.  
2) Этот `AGENTS.md` в текущей директории.  
3) Локальные `AGENTS.md` в подпапках (перекрывают правила **в пределах своей папки**).  
4) `README.md`, `fdl_language_spec.md`, `fdl_manifest.md`.

---

## 1) Карта репозитория (ориентиры)
```

.github/                 # CI, шаблоны
assets/                  # символы/иконки (напр. taurus\_sigil.svg)
docs/                    # документация (если есть)
LICENSE, NOTICE.md
README.md
fdl\_language\_spec.md     # спецификация FDL
fdl\_macro\_patterns.fdl   # макро-паттерны FDL
fdl\_manifest.md          # манифест архитектуры
fdl\_compiler.py          # компилятор/валидатор FDL
fdl\_graph\_engine.py      # граф-визуализация/анализ
gromada\_live\_api.py      # FastAPI интерфейс живой связи агентов

````

---

## 2) Окружение (Python 3.11+)
Рекомендуется: Linux/macOS/WSL, менеджер `uv` или `pip`.

Установка:
```bash
git clone https://github.com/NgoiSigma/fdl-gromada-noveya.git
cd fdl-gromada-noveya

# Зависимости (если есть requirements.txt)
uv pip install -r requirements.txt 2>/dev/null || true
# либо:
pip install -r requirements.txt 2>/dev/null || true

# Минимальный набор, если requirements.txt отсутствует:
pip install ruff pytest pyright mypy fastapi uvicorn networkx graphviz pydot
# (networkx/graphviz/pydot — для графа; fastapi/uvicorn — для live API)
````

> Агент: если зависимостей не хватает — **не падай**. Установи недостающее по сообщениям об ошибках и продолжай.

---

## 3) Контроль качества (Quality Gates) — обязательно перед PR

```bash
ruff fix . && ruff check .
pyright || mypy .
pytest -q || echo "no tests yet"
```

Политика отказа: если линтер/типы падают — правь до зелёного; если тестов нет — сгенерируй smoke-тесты CLI (см. §10).

---

## 4) Runbooks (playbooks агента)

> Запускать команды **из корня** репозитория.

### 4.1 FDL Compiler — компиляция/валидация

```bash
# Базовая проверка синтаксиса/правил
python fdl_compiler.py --input fdl_macro_patterns.fdl --check

# Пайплайн по фазам ФДЛ (пример интерфейса)
python fdl_compiler.py --phase init       --input fdl_macro_patterns.fdl --out out/phase_init.json
python fdl_compiler.py --phase expand     --input out/phase_init.json     --out out/phase_expand.json
python fdl_compiler.py --phase synthesize --input out/phase_expand.json   --out out/phase_synth.json
```

### 4.2 Graph Engine — построение/анализ графа смыслов

```bash
# Построить граф из макро-паттернов и сохранить артефакты
python fdl_graph_engine.py \
  --input fdl_macro_patterns.fdl \
  --format png --out out/graph/gromada_graph.png \
  --metrics out/graph/metrics.json
```

### 4.3 Live API — живая связка агентов (FastAPI)

```bash
# Локальный запуск API (uvicorn)
uvicorn gromada_live_api:app --reload --host 0.0.0.0 --port 8000

# Примеры curl (по желанию API):
# curl -X POST http://localhost:8000/compile -F "file=@fdl_macro_patterns.fdl"
# curl -X POST http://localhost:8000/graph   -F "file=@fdl_macro_patterns.fdl"
```

> Если какой-то модуль или эндпойнт ещё не реализован — создай **заглушку** (CLI + `--help`/`/health`, код возврата 0) и минимальный тест.

---

## 5) Артефакты (куда всё складывать)

```
out/
  phase_init.json
  phase_expand.json
  phase_synth.json
  graph/
    gromada_graph.png
    metrics.json
logs/
artifacts/
  validation/
```

---

## 6) Стиль кода

* PEP8; линтер — **Ruff** (см. шаблон `pyproject.toml` ниже).
* Докстринги: Google-style/NumPy-style.
* Имена: `snake_case` для функций/модулей, `CamelCase` для классов.
* Публичные API документируй в `docs/` (если нет — создай).

---

## 7) Политика PR

Перед PR **обязательно**:

1. `ruff check .` — 0 ошибок;
2. `pyright` или `mypy` — без критических;
3. `pytest -q` — зелёные (или есть smoke-тесты CLI);
4. Обновлён `docs/` или `README.md`, если менялся публичный интерфейс;
5. В `CHANGELOG.md` добавлен краткий FDL-лог изменения (что/зачем/влияние).

Рекомендация `CODEOWNERS`:

```
/fdl_compiler.py       @owners
/fdl_graph_engine.py   @owners
/gromada_live_api.py   @owners
```

---

## 8) Этические и символические правила

* Уважай ограничения из `NOTICE.md` / LICENSE (Apache-2.0) и раздел «SYMBOL USE NOTICE».
* Символы (напр. `taurus_sigil.svg`) использовать **целостно**, с указанием источника; запрещено для эксплуататорских/закрытых систем.
* Изменения FDL-аксиом/языка — только через отдельный PR и согласование владельцев.

---

## 9) CI (GitHub Actions)

> Если workflow отсутствует — создай `.github/workflows/ci.yml`:

```yaml
name: gromada-ci
on:
  push: { branches: [ main ] }
  pull_request: { branches: [ main ] }
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Install deps
        run: |
          python -m pip install -U pip
          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
          pip install ruff pytest pyright mypy fastapi uvicorn networkx graphviz pydot || true
      - name: Lint
        run: ruff check .
      - name: Type check
        run: pyright || mypy .
      - name: Tests
        run: pytest -q || echo "no tests yet"
```

---

## 10) Мини-шаблоны (быстрый scaffold)

**`pyproject.toml` (Ruff + Pyright)**

```toml
[tool.ruff]
line-length = 100
target-version = "py311"
select = ["E","F","I","UP","N","B"]
ignore = ["ANN101","ANN102"]

[tool.pyright]
include = ["."]
pythonVersion = "3.11"
```

**Smoke-тесты CLI** `tests/test_cli_smoke.py`

```python
import subprocess

def run_ok(cmd: str):
    assert subprocess.call(cmd, shell=True) == 0

def test_compiler_help():  run_ok("python fdl_compiler.py --help")
def test_graph_help():     run_ok("python fdl_graph_engine.py --help")
def test_api_import():     run_ok("python -c 'import gromada_live_api; print(1)'")
```

**`.gitignore` (артефакты)**

```
out/
logs/
artifacts/
__pycache__/
*.pyc
.ipynb_checkpoints/
```

---

## 11) Диагностика

* **Модуль не найден** → проверь путь запуска (из корня), версию Python.
* **Нет system Graphviz** → установи пакет ОС (`graphviz`) и Python-биндинги (`graphviz`/`pydot`).
* **FastAPI не стартует** → проверь `uvicorn`, занятый порт, импорты.
* **Отчёты пустые** → проверь входные файлы (`fdl_macro_patterns.fdl`) и аргументы CLI.

---

## 12) Локальные AGENTS.md

Разрешены в `docs/`, `assets/` и рядом с любым модулем. Они **перекрывают** корневой **в своей папке** (например, отдельные инструкции по рендеру графов или API).

```

[1]: https://github.com/NgoiSigma/fdl-gromada-noveya "GitHub - NgoiSigma/fdl-gromada-noveya: Resonance-based FDL architecture and semantic agent SDK for NOVЕYA. A living logic system for self-organization and conscious ecosystems."
