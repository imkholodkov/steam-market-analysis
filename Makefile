.PHONY: results build serve clean

results:  ## расчёт с кэшем: пропускается, если данные и скрипт не менялись
	uv run python scripts/build_results.py

build: results
	uv run mkdocs build --strict

serve: results
	uv run mkdocs serve

clean:
	rm -rf site .cache docs/p3/generated
