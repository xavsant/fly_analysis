import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/generated_daily_settle.csv")

# Calculate fly
df["fly"] = 2 * df["nov"] - (df["oct"] + df["dec"])

# Variables
dte_min = 0
dte_max = 60
rolling = 5
df_filtered = df[(df["dte"] >= dte_min) & (df["dte"] <= dte_max)]

# Plot
plt.figure(figsize=(12, 6))
plt.plot(df_filtered["dte"], df_filtered["fly"].rolling(rolling, center=True).mean(), linewidth=2.5)
plt.xlabel("Days to Expiry (DTE)")
plt.ylabel("Fly")
plt.title("Fly Behaviour to Expiry")
plt.grid(True)
plt.tight_layout()
plt.gca().invert_xaxis()
plt.savefig("data/fly_dte_graph.jpg")
plt.show()

# Delta PNL
enter_trade = 40 # days to expiry
exit_trade = 5
enter_fly = df[df["dte"] == enter_trade]["fly"].values[0]
exit_fly = df[df["dte"] == exit_trade]["fly"].values[0]
delta_pnl = exit_fly - enter_fly # for one unit
print(f"Delta PNL from entering {enter_trade} dte and exiting {exit_trade} dte is {delta_pnl}.")

