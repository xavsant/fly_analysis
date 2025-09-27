import numpy as np
import pandas as pd

np.random.seed(42)

dates = pd.date_range(start="2024-01-01", end="2024-09-30", freq="D")

# Generate daily values with random noise around each baseline
contract = {
    "date": dates,
    "oct": [95 + np.random.normal(-0.2, 0.3) for _ in dates],
    "nov": [94 + np.random.normal(-0.3, 0.2) for _ in dates],
    "dec": [96 + np.random.normal(0, 0.1) for _ in dates],
}
df = pd.DataFrame(contract)
df["month"] = df["date"].dt.month

# Days to expiry (based on Oct/Nov/Dec)
df["dte"] = (pd.Timestamp("2024-09-30") - df["date"]).dt.days

df.to_csv("data/generated_daily_settle.csv", index=False)
