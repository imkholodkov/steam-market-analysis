# steam-market-analysis

![CI](https://github.com/imkholodkov/steam-market-analysis/actions/workflows/ci.yml/badge.svg)

Анализ рынка игр в Steam: каркас проекта для магистерской лабораторной работы №1.
На этом шаге настроены управление зависимостями, статическая типизация, линтер,
тесты, конфигурация, логирование, CLI и непрерывная интеграция. Логика анализа
данных будет добавляться в следующих лабораторных.

## Требования

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)

## Установка

```bash
git clone https://github.com/imkholodkov/steam-market-analysis.git
cd steam-market-analysis
uv sync
```

## Конфигурация

Настройки читаются из переменных окружения с префиксом `RG_` (см. `.env.example`).

| Переменная          | Описание                          | По умолчанию |
|---------------------|------------------------------------|--------------|
| `RG_GITHUB_TOKEN`   | Токен GitHub (не выводится в CLI) | не задан     |
| `RG_DATA_DIR`       | Директория для данных             | `data`       |
| `RG_LOG_LEVEL`       | Уровень логирования               | `INFO`       |
| `RG_REQUEST_TIMEOUT` | Таймаут HTTP-запросов, сек        | `10.0`       |
| `RG_MAX_CONCURRENCY` | Максимум параллельных запросов    | `4`          |

## Использование

```bash
uv run sma version
# 0.1.0

uv run sma check-config
# data_dir: data
# log_level: INFO
# request_timeout: 10.0
# max_concurrency: 4
# github_token: не задан
```

## Разработка

```bash
uv run ruff check .          # линт
uv run ruff format --check . # форматирование
uv run mypy                  # типизация (strict)
uv run pytest                # тесты и покрытие
uv run pre-commit run --all-files
```

## Структура проекта

```
src/steam_market_analysis/
├── cli.py              # точка входа CLI (команда `sma`)
├── config.py            # настройки на pydantic-settings
├── logging_setup.py     # настройка логирования
├── models/               # заготовка: доменные модели
├── sources/              # заготовка: источники данных
├── storage/              # заготовка: слои хранения данных
├── pipelines/            # заготовка: пайплайны обработки
└── api/                  # заготовка: внешний API
tests/                    # тесты pytest
```
