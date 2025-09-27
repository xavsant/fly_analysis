# Fly Analysis
This repo provides an overview and simple analysis for **fly trading with swaps and calendar spreads**.

## How to Use
### 1. Generate data
Use the dummy historical dataset in `/data/generated_daily_settle.csv` or further experiment with the output in `/generate_data.py`.
### 2. Run fly analysis
Execute `/analysis.py` to get a chart and PNL for an entry-exit trade.
### 3. Run settlement analysis
Execute `/to_settle.py` to get the PNL if you take the contract to settlement. Alternatively, refer to `/data/to_settle_daily_values_pnl_calculated.xlsx` for the calculations in excel.

## Definitions
### 1. What is a spread?
A spread is the difference in value between two related objects.<br>
This repo focuses on calendar spread - for instance, the difference in monthly average price for an asset from January to February.
### 2. What is a fly?
Shortform for butterfly, it's a structure that combines **2 calendar spreads**.
- Measures the relative value of 2x the middle month compared to its 2 surrounding months (wings)
### 3. How is a fly calculated?
For months **M1 (front leg), M2 (middle leg), M3 (back leg)**, the fly is calculated as:

$$
(M2 - M1) - (M3 - M2) =
2 * M2 - (M1 + M3)
$$

#### 3.1 Example

| Month | Price |
|-------|-------|
| M1    | 100   |
| M2    | 105   |
| M3    | 103   |

$$
Fly = 105 - (100 + 103) / 2 = 3.5
$$ 

#### 3.2 Alternative formula

> Note that the [implications of the formula](#4-what-does-the-fly-value-imply) are inversed for the following:

$$
(M1 + M3) - 2 * M2
$$

### 4. What does the fly value imply?
We can either enter and exit the fly when it's still a forward, or take it to [pricing](#going-into-pricing). This section treats fly values as an entry-exit trade.
- We say the middle leg is **rich** (overpriced) when the fly is positive: the middle leg has a higher value than the average of the wings
- We say the middle leg is **cheap** (underpriced) when the fly is negative: the middle leg has a lower value than the average of the wings

## Buying/Selling the Fly
### 1. Buying
- Long the middle leg, short the wings
- Profit if the middle leg becomes **richer** (outperforms) relative to the wings: fly goes up
### 2. Selling
- Short the middle leg, long the wings
- Profit if the middle leg becomes **cheaper** (underperforms) relative to the wings: fly goes down
### Note
It doesn't matter where the fly starts but the direction of the movement.
- In words, if the fly is negative (cheap) and we believe that the middle leg will outperform the wings, buy the fly
- In values, if we believe that the fly will increase in value ($ x_{t+1} > x_t $), buy the fly

It's important to figure out when to enter and exit the trade! (experiment by changing `enter_trade` and `exit_trade` in [analysis.py](https://github.com/xavsant/fly_analysis/blob/main/analysis.py))

## Fly vs Outright Long/Short Month
### 1. Isolate relative value
- If you successfully take a position on a month, it's harder to see whether it's because the middle leg outperformed/underperformed or because of flat price moves
- On the flipside, if you unsuccessfully take a position on a month, the fly would hedge against a flat price move (if you buy the fly and all months -$10, PNL is $0, where if you were long on a month your PNL would be -$10)
- Thus, a fly allows you to bet specifically on the curve shape without caring about overall price direction
### 2. Lower margin requirements
- When you take a position you must post initial margins to cover losses
- Outright long/short > Spreads > Butterflies in terms of margin
### Note
- Regardless of trade, you can still take a big hit if your **relative view** is incorrect; middle leg behaves differently
- However, with flies you're more insulated from broad rallies/crashes
- The risk is concentrated on curve shape, which should generally move less violently than flat prices

## Going into Settlement
### 1. Entry/Exit before Settlement
- Typically, we enter and exit a fly trade before the contract month starts
- i.e. we hold a view and trade it against the market expectation (forward pricing)
- This is because we are subject to a lot of volatility to settlement (depends on what's going on in the market/world at that moment)
### 2. Pricing
- When we roll into the contract month itself, the swap is no longer a forward mark, instead it goes into **pricing** and starts actively accruing daily settlement exposure
- This means that part of your fly becomes locked in, while the remaining are still treated as forward moves (the fly is also said to 'shrink' as less uncertainty overall)
- i.e. if you take the first month to pricing, the second and third month now act as a spread
### 3. Market-on Close (MOC)
A price assessment process, most famously used by [Platts](https://www.spglobal.com/content/dam/spglobal/general/en/documents/easset_upload_file58950_994814_e.pdf). 
- Platts observes all the bids, offers and trades submitted during the last 30 minutes of the trading day
- Those trades are used to publish the official index which becomes the settlement basis for swaps
- We can use the MOC to estimate the PNL for a fly going into pricing (estimate next leg's value based on what was traded in the market)

#### 3.1 Example

For simplicity, we look at a spread going into pricing. For a fly, you apply the same logic on the second spread as the middle leg goes into pricing.

| Date  | M1_Settle | M1_Business_Days_to_Expiry | M2_MOC |
|-------|-----------|----------------------------|--------|
| 01/01 | 100       | -1                         | 110    | 
| 01/02 | 98        | -2                         | 104    | 
| 01/03 | 101       | -3                         | 100    | 

Suppose you have the following table, where the settle and MOC is aligned to the date. The M1 contract goes into pricing when `M1_Business_Days_to_Expiry < 0` ('expiry' in this sense is when the contract is still traded as a forward swap).

**Variables:**
1. Volume: `3kt`
2. Type of Trade: `Sell M1/M2`
3. Position: `-3kt/3kt`

For each day in pricing, we'd put an amount of our volume into the settle (let's average and say 1kt per day).<br>
Because we're selling a spread, we're short/long M1/ M2. We make money if the value of M1/M2 goes down/up.<br><br>
This also means that we're 'missing' 3kt in M1, and we have bought 3kt in M2.<br>
Each day, we displace the position (ensure we're **delta neutral**) to approach 0/0 (in this case, buy 1kt in M1 and sell 1kt in M2).<br><br>
To calculate the daily PNL, we do the following:<br>

$$
MOC_{t} - Settle_{t} = PNL_{t}
$$

> Above would be **inversed** for a buy spread (buy/sell in M1/M2 as long/short).

Thus, the **total PNL** would be:

$$
(110 - 100) + (104 - 98) + (100 - 101) = 15
$$

---




