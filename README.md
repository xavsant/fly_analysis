# Fly Analysis
This repo provides an overview and simple analysis for **fly trading with calendar spreads**.

## How to Use
### 1. Generate data
Use the dummy historical dataset in `/data/generated_daily_values.csv` or further experiment with the output in `/generate_data.py`.
### 2. Run analysis
Execute `/analysis.py` to get a chart and ${\Delta}PNL$.

## Definitions
### 1. What is a spread?
A spread is the difference in value between two related objects.<br>
This repo focuses on calendar spread - for instance, the difference in monthly average price for an asset from January to February.
### 2. What is a fly?
Shortform for butterfly, it's a structure that combines **2 calendar spreads**.
- Measures the relative value of a middle month compared to the average of 2 surrounding months (in the case of swaps, it would comparing the value of a middle contract against the average of 2 surrounding contracts (the wings)
### 3. How is a fly calculated?
For months **M1 (front month), M2 (middle month), M3 (back month)**, the fly is calculated as:

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

### 4. What does the fly value imply?
- We say the middle month is **rich** (overpriced) when the fly is positive: the middle month has a higher value than the average of the wings
- We say the middle month is **cheap** (underpriced) when the fly is negative: the middle month has a lower value than the average of the wings

## Buying/Selling the Fly
### 1. Buying
- Long the middle month, short the wings
- Profit if the middle month becomes **richer** (outperforms) relative to the wings: fly goes up
### 2. Selling
- Short the middle month, long the wings
- Profit if the middle month becomes **cheaper** (underperforms) relative to the wings: fly goes down
### Note
It doesn't matter where the fly starts but the direction of the movement.
- In words, if the fly is negative (cheap) and we believe that the middle month will outperform the wings, buy the fly (long the middle month)
- In values, if we believe that the fly will increase in value ($ x_{t+1} > x_t $), buy the fly

It's important to figure out when to enter and exit the trade! (experiment by changing `enter_trade` and `exit_trade` in [analysis.py](https://github.com/xavsant/fly_analysis/blob/main/analysis.py))

## Fly vs Outright Long/Short Month
### 1. Isolate relative value
- If you successfully take a position on a month, it's harder to see whether it's because the middle month outperformed/underperformed or because of flat price moves
- On the flipside, if you unsuccessfully take a position on a month, the fly would hedge against a flat price move (if you buy the fly and all months -$10, PNL is $0, where if you were long on a month your PNL would be -$10)
- Thus, a fly allows you to bet specifically on the curve shape without caring about overall price direction
### 2. Lower margin requirements
- When you take a position you must post initial margins to cover losses
- Outright long/short > Spreads > Butterflies in terms of margin
### Note
- Regardless of trade, you can still take a big hit if your **relative view** is incorrect; middle month behaves differently
- However, with flies you're more insulated from broad rallies/crashes
- The risk is concentrated on curve shape, which should generally move less violently than flat prices
