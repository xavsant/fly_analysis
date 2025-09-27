import pandas as pd

def spread_pnl(df, month: str, is_buy: bool):
    '''
    Gets the PNL for a spread that's going to settlement.

    df: DataFrame containing the settles, bdte and mark on curve merged on the date.
    month: The front month for the spread.
    is_buy: Whether this is a buy spread, False if sell spread. Buy spread = long front month, short back month.
    '''
    spread_df = df[df[month + '_bdte'] < 0]
    spread_df = spread_df[[month + '_settle', 'mark_on_curve']]

    spread_df['pnl'] = spread_df[month + '_settle'] - spread_df['mark_on_curve'] # sell front month, buy back month
    if not is_buy: # buy front month, sell back month
        spread_df['pnl'] = - spread_df['pnl']

    spread_df.loc['total', 'pnl'] = spread_df['pnl'].sum()

    return spread_df



if __name__ == "__main__":
    df = pd.read_csv("data/to_settle_daily_values.csv", index_col='date')

    front_leg = 'jan'
    middle_leg = 'feb'
    back_leg = 'mar'

    front_spread = spread_pnl(df, front_leg, is_buy = True)
    back_spread = spread_pnl(df, middle_leg, is_buy = False)
    total_pnl = front_spread.loc['total', 'pnl'] + back_spread.loc['total', 'pnl']


    # Get Results
    print('Total PNL:', total_pnl)
    print()
    print('Front Spread Daily PNL')
    print(front_spread)
    print()
    print('Back Spread Daily PNL')
    print(back_spread)

