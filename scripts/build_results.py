"""Расчёт результатов по выборке Steam и генерация страницы сайта.

Читает datasets/steam_sample.csv, считает показатели рынка, сохраняет графики
и Markdown-страницу в docs/lab2/p3/generated/. Пересчёт пропускается, если хеш
входных данных и этого скрипта совпадает с сохранённым в кэше.
"""

import hashlib
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATASET = ROOT / "datasets" / "steam_sample.csv"
OUT_DIR = ROOT / "docs" / "lab2" / "p3" / "generated"
CACHE_FILE = ROOT / ".cache" / "results.json"
OUTPUTS = ["results.md", "releases_by_year.png", "price_by_genre.png"]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


LOCKFILE = ROOT / "uv.lock"
MIN_REVIEWS = 10  # порог отзывов для доли положительных: у игр с 1–2 отзывами доля 0 % или 100 %


def cache_key() -> str:
    # uv.lock в ключе: смена версий pandas/matplotlib тоже требует пересчёта
    parts = (DATASET, Path(__file__), LOCKFILE)
    return "-".join(sha256(p)[:12] for p in parts)


def is_cached(key: str) -> bool:
    if not CACHE_FILE.exists():
        return False
    saved = json.loads(CACHE_FILE.read_text(encoding="utf-8"))
    return saved.get("key") == key and all((OUT_DIR / name).exists() for name in OUTPUTS)


def parse_genres(raw: str) -> list[str]:
    # В датасете два формата: [{"id": "1", "description": "Action"}] и ["Action", "Indie"]
    items = json.loads(raw) if isinstance(raw, str) and raw else []
    return [i["description"] if isinstance(i, dict) else str(i) for i in items]


def compute() -> None:
    # Тяжёлые импорты — только при реальном пересчёте, чтобы попадание в кэш было быстрым.
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import pandas as pd

    df = pd.read_csv(DATASET)
    df["year"] = pd.to_datetime(df["release_date"], errors="coerce").dt.year
    df["genre"] = df["genres"].map(parse_genres)
    df["reviews"] = df["positive"] + df["negative"]
    df["positive_share"] = df["positive"] / df["reviews"].where(df["reviews"] >= MIN_REVIEWS)

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    by_year = df.dropna(subset=["year"]).groupby("year").size()
    by_year = by_year[by_year.index >= 2006]
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(by_year.index.astype(int), by_year.values, color="#4c72b0")
    ax.set_xlabel("Год выхода")
    ax.set_ylabel("Число игр в выборке")
    fig.tight_layout()
    fig.savefig(OUT_DIR / "releases_by_year.png", dpi=120)
    plt.close(fig)

    genres = (
        # игра с несколькими жанрами учитывается в каждом из них
        df.explode("genre")
        .dropna(subset=["genre"])
        .groupby("genre")
        .agg(
            games=("app_id", "size"),
            median_price=("price", "median"),
            free_share=("price", lambda s: (s == 0).mean()),
            positive_share=("positive_share", "median"),
        )
        .sort_values("games", ascending=False)
        .head(10)
    )
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.barh(genres.index[::-1], genres["median_price"][::-1], color="#dd8452")
    ax.set_xlabel("Медианная цена, $")
    fig.tight_layout()
    fig.savefig(OUT_DIR / "price_by_genre.png", dpi=120)
    plt.close(fig)

    rows = "\n".join(
        f"| {g} | {int(r.games)} | {r.median_price:.2f} | {r.free_share:.0%} | {r.positive_share:.0%} |"
        for g, r in genres.iterrows()
    )
    summary = (
        f"| Показатель | Значение |\n|---|---|\n"
        f"| Игр в выборке | {len(df)} |\n"
        f"| Медианная цена, $ | {df['price'].median():.2f} |\n"
        f"| Доля бесплатных | {(df['price'] == 0).mean():.1%} |\n"
        f"| Медианная доля положительных отзывов (игры от {MIN_REVIEWS} отзывов) | {df['positive_share'].median():.1%} |\n"
    )
    (OUT_DIR / "results.md").write_text(
        "## Сводка\n\n" + summary + "\n"
        "## Выход игр по годам\n\n![Выход игр по годам](generated/releases_by_year.png)\n\n"
        "## Топ-10 жанров\n\nИгра с несколькими жанрами учитывается в каждом из них. "
        f"Доля положительных отзывов — по играм от {MIN_REVIEWS} отзывов.\n\n"
        "| Жанр | Игр | Медианная цена, $ | Бесплатных | Положительных отзывов |\n"
        "|---|---|---|---|---|\n" + rows + "\n\n"
        "![Медианная цена по жанрам](generated/price_by_genre.png)\n",
        encoding="utf-8",
    )


def main() -> int:
    start = time.perf_counter()
    key = cache_key()
    force = "--force" in sys.argv
    if not force and is_cached(key):
        print(f"cache hit key={key} elapsed={time.perf_counter() - start:.3f}s")
        return 0
    compute()
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    CACHE_FILE.write_text(json.dumps({"key": key}), encoding="utf-8")
    print(f"recomputed key={key} elapsed={time.perf_counter() - start:.3f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
