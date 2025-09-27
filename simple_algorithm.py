import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('data/generated_daily_settle.csv', index_col='date')

##############
# Parameters #
##############

enter_dte = 120
exit_dte = 7
short_SMA = 20
medium_SMA = 40
volume = 1000 # 1kt per trade

#########
# Rules #
#########

# Entry: go short when short_SMA crosses above medium_SMA
#        go long when short_SMA crosses below medium_SMA
# Exit: opposite cross OR dte >= exit_dte
# Why?: downward trend, looking for mean reversion
# What other rules can be added to make the trade more robust?

#################
# Get Variables #
#################

df["fly"] = 2 * df["nov"] - (df["oct"] + df["dec"])
df["short_SMA"] = df['fly'].rolling(window=short_SMA).mean()
df["medium_SMA"] = df['fly'].rolling(window=medium_SMA).mean()
df = df[(df['dte'] >= exit_dte) & (df['dte'] <= enter_dte)]

#########
# Trade #
#########

trades = [] 
position = 0 
entry_val = None 
exit_val = None 
entry_price = None 

for i, row in df.iterrows(): 
    short_sma = row["short_SMA"] 
    medium_sma = row["medium_SMA"] 
    fly = row["fly"] 
    dte = row["dte"] 
    
    # ENTRY rules 
    if position == 0: 
        if short_sma > medium_sma: 
            # downward mean reversion 
            position = -1
            entry_val = dte 
            entry_price = fly 
        elif short_sma < medium_sma: 
            # upward mean reversion 
            position = 1 
            entry_val = dte 
            entry_price = fly 
        
    # EXIT rules 
    else: 
        # Opposite crossover 
        if (position == -1 and short_sma < medium_sma) or \
        (position == 1 and short_sma > medium_sma) or \
        dte == exit_dte: 
            exit_price = fly 
            pnl = (exit_price - entry_price) * position * volume
        
            trades.append({ 
                "entry_dte": entry_val, 
                "exit_dte": dte, 
                "entry_price": entry_price, 
                "exit_price": exit_price, 
                "position": position, 
                "pnl": pnl }) 
        
            # reset 
            position = 0 
            entry_val = None 
            exit_val = None 
            entry_price = None

# Convert to DataFrame
trades_df = pd.DataFrame(trades)
trades_df.loc['total', 'pnl'] = trades_df['pnl'].sum()
print('PNL and positions for Systematic Trade:')
print(trades_df)

# Enter-Exit PNL, position = short
entry_fly = df[df['dte'] == enter_dte]['fly'].values[0]
exit_fly = df[df['dte'] == exit_dte]['fly'].values[0]
ee_pnl = -(exit_fly - entry_fly) * volume
print('PNL for Entry-Exit Trade:')
print("Entry Fly:", entry_fly, "Exit Fly:", exit_fly)
print("PNL:", ee_pnl)

#############
# SMA Graph # 
#############

plt.figure(figsize=(12,6))
plt.plot(df['dte'], df['short_SMA'], label='short_SMA', linewidth=2.5)
plt.plot(df['dte'], df['medium_SMA'], label='medium_SMA', linewidth=2.5)
plt.xlabel("Days to Expiry (DTE)")
plt.ylabel("Simple Moving Average (SMA)")
plt.grid(alpha=0.2)
plt.legend()
plt.tight_layout()
plt.gca().invert_xaxis()
plt.savefig("graphs/simple_algorithm_sma_dte.jpg")
plt.show()