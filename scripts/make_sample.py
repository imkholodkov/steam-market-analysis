"""Отбор воспроизводимой выборки из полного CSV Steam Games Dataset (Kaggle)."""

import csv
import random
import sys
from pathlib import Path

COLUMNS = [
    "app_id",
    "name",
    "release_date",
    "price",
    "estimated_owners",
    "genres",
    "positive",
    "negative",
    "recommendations",
    "average_playtime_forever",
]
SAMPLE_SIZE = 10_000
SEED = 43
MIN_YEAR = 2020  # только игры, выпущенные с этого года


def main(src: Path, dst: Path) -> None:
    csv.field_size_limit(sys.maxsize)
    with src.open(encoding="utf-8", newline="") as f:
        rows = [
            {c: r[c] for c in COLUMNS}
            for r in csv.DictReader(f)
            if r["release_date"][:4].isdigit() and int(r["release_date"][:4]) >= MIN_YEAR
        ]
    rows.sort(key=lambda r: int(r["app_id"]))
    sample = random.Random(SEED).sample(rows, SAMPLE_SIZE)
    sample.sort(key=lambda r: int(r["app_id"]))
    dst.parent.mkdir(parents=True, exist_ok=True)
    with dst.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        w.writerows(sample)
    print(f"total={len(rows)} sample={len(sample)} -> {dst}")


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]))
