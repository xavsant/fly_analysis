import pandas as pd

def fly_pnl(df, M1_entry, M2_entry, M3_entry,
            M1_contract='Jan-26', M2_contract='Feb-26', position=1):
    """
    This function produces the expected pnl of holding a fly till settlement.

    Inputs
    ------
    df : dataframe with columns:
        Date, M0 Settlement, M1 Settlement, M0 contract, M1 contract

    M1_entry, M2_entry, M3_entry : entry levels
        e.g. 500, 500, 500

    M1_contract, M2_contract : strings
        e.g. 'Jan-26', 'Feb-26'
    """

    # ---------- Leg definitions ----------
    leg1 = df[df['M0 contract'] == M1_contract].copy()
    leg2 = df[df['M0 contract'] == M2_contract].copy()

    # ---------- Spread calculation ----------
    leg1['spread'] = leg1['M0 Settlement'] - leg1['M1 Settlement']
    leg2['spread'] = leg2['M0 Settlement'] - leg2['M1 Settlement']

    # ---------- Entry spreads ----------
    entry_spread_1 = M1_entry - M2_entry
    entry_spread_2 = M2_entry - M3_entry

    # ---------- Daily PnL ----------
    leg1['pnl'] = (leg1['spread'] - entry_spread_1) * position
    leg2['pnl'] = (entry_spread_2 - leg2['spread']) * position

    # ---------- Totals ----------
    pnl_leg1 = leg1['pnl'].sum()
    pnl_leg2 = leg2['pnl'].sum()
    total_pnl = pnl_leg1 + pnl_leg2

    # ---------- Implied fly ----------
    avg_spread_1 = leg1['spread'].mean()
    avg_spread_2 = leg2['spread'].mean()

    implied_fly = avg_spread_1 - avg_spread_2

    # ---------- Entry fly ----------
    entry_fly = entry_spread_1 - entry_spread_2

    return {
        "leg1": leg1,
        "leg2": leg2,
        "total_pnl": total_pnl,
        "implied_fly": implied_fly,
        "entry_fly": entry_fly
    }


# ---------------- MAIN ----------------

if __name__ == "__main__":

    df = pd.read_csv("data/to_settle_daily_values.csv",)
    df['Date'] = pd.to_datetime(df['Date'], format="%d/%m/%y")

    results = fly_pnl(
        df,
        M1_entry=500,
        M2_entry=495,
        M3_entry=498,
        M1_contract="Jan-25",
        M2_contract="Feb-25",
        position=-1
    )

    print("Total PNL:", results["total_pnl"])
    print()

    print("Entry Fly:", results["entry_fly"])
    print(f"Implied Fly: {results["implied_fly"]:.1f}")
    print()

    print("Leg 1 Daily PNL")
    print(results["leg1"])

    print()
    print("Leg 2 Daily PNL")
    print(results["leg2"])
