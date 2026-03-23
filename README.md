# Polymarket Insider Trading Tracker

**Goldsmiths Digital Sandbox — CW3 Project**
Prototype for detecting anomalous trading behaviour and potential insider activity on Polymarket.

---

## APIs

| Name | Endpoint |
|------|----------|
| `GAMMA_API` | https://gamma-api.polymarket.com |
| `DATA_API` | https://data-api.polymarket.com |
| `GOLDSKY_URL` | https://api.goldsky.com/api/public/project_cl6mb8i9h0003e201j6li0diw/subgraphs/pnl-subgraph/0.0.14/gn |
| `POLYGONSCAN_API` | https://api.etherscan.io/v2/api |

---

## Analysis Parameters

### Behavioural Signals

**Market Spread**
Checks if all of your positions are in the same market. If you're betting exclusively on Iran, the Oscars or who will Trump meet next, the parameter will flag your activity as suspicious.

**Creation / Cash-Out Gap**
Time elapsed between account creation and first 10,000 redemption. Flags accounts that are created shortly before large redemptions.

**Volume / Redemption Ratio**
Number of positions opened versus volume of redemptions. Flags accounts that have made large amounts of money on relatively few positions.

**Profit / Loss Ratio**
Absolute size of profits relative to losses. High ratio sustained over time is a core insider signal.

**Overall Success Rate**
Proportion of resolved positions that were profitable. Benchmarked against market baseline to identify statistical outliers.

**High-Frequency Trading**
Evidence of rapid, repeated position-taking within short time windows — may indicate automated or algorithmically-assisted trading.

**Relative Size of Winning Position**
Size of winning positions relative to the trader's other positions. Large asymmetric bets that resolve profitably are a key indicator.

---

### Blockchain Signals

**Initial Deposit Quantity** *(First 20 transactions)*
Sum of the first 20 deposits into the Polymarket wallet. Large opening deposits into new accounts are a red flag.

**24 / 48hr Deposit Amount** *(First 48 hours)*
Total capital deposited into the wallet within the first 24–48 hours of account activity. Rapid large inflows to new accounts warrant investigation.

**Deposit/Withdrawal** *(First 48 hours)*
Checks the amount entering and leaving the wallet within the first 48 hours. If there's a large capital inflow and equivalent outflow, the wallet will be flagged for suspicious activity.


---

## Notes

- All blockchain analysis via Polygonscan API (Polygon network)
- PnL data sourced from Goldsky subgraph
- This is a prototype — outputs are indicative, not evidentiary
