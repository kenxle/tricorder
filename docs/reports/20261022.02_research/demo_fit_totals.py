"""Total the per-criterion fit scores in demo_fit_scores.csv (0 to 2 each, five criteria, 10 max).

Run: python3 -I demo_fit_totals.py
"""
import pathlib
import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent
df = pd.read_csv(HERE / "demo_fit_scores.csv")
wide = df.pivot(index="company", columns="criterion", values="score")
wide["total"] = wide.sum(axis=1)
wide = wide.sort_values("total", ascending=False)
wide.to_csv(HERE / "demo_fit_totals.csv")
print(wide.to_string())
