from pathlib import Path
from check import check_all

Path("reports").mkdir(exist_ok=True)

df = check_all()
df.to_csv("reports/results.csv", index=False)

n_pass = (df["overall"] == "PASS").sum()
print(df.to_string(index=False))
print()
print(f"{n_pass} of {len(df)} calculations passed QA.")
print("Saved to reports/results.csv")
