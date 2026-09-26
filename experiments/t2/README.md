# Стенд T2: сравнение способов «эксперимент → страница»

Один и тот же расчёт (`analysis.py`, формат jupytext percent) прогоняется разными инструментами.
Данные — `datasets/steam_sample.csv`, скопированные в каталог стенда как `data.csv`.

Окружение стенда отдельное от проекта:

```bash
uv init --bare --python 3.12 . && uv add pandas matplotlib nbconvert nbclient ipykernel papermill jupytext myst-nb sphinx quarto-cli
uv run jupytext --to ipynb --set-kernel python3 analysis.py
```

| Инструмент | Команда |
|---|---|
| nbconvert | `uv run jupyter nbconvert --execute --to markdown analysis.ipynb` |
| papermill | `uv run papermill analysis.ipynb out.ipynb -p min_year 2023` |
| MyST-NB | `conf.py` + `uv run sphinx-build -b html . _build` |
| Quarto | `_quarto.yml` + `uv run quarto convert analysis.ipynb -o analysis.qmd && uv run quarto render` |
