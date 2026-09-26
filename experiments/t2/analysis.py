# %% [markdown]
# # Выход игр по годам

# %% tags=["parameters"]
min_year = 2020
dataset = "data.csv"

# %%

import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv(dataset)
df["year"] = pd.to_datetime(df["release_date"], errors="coerce").dt.year
df = df[df["year"] >= min_year]
by_year = df.groupby("year").size()
print(f"Игр: {len(df)}, медианная цена: {df['price'].median():.2f}")

# %%
fig, ax = plt.subplots(figsize=(8, 4))
ax.bar(by_year.index.astype(int), by_year.values)
ax.set_xlabel("Год выхода")
plt.show()
