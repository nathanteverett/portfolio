# Statistical Arbitrage in Crypto: Predicting Momentum and Reversal
### A quant strategy by Nathan T. Everett

Key:
1. Momentum strategy: Crypto Momentum Directional Index Strategy.ipynb
2. Reversal strategy: Correlated Basket Pair Reversal in Crypto.ipynb
3. Combo strategy: Directional Index Reveral and Momentum Strategy.ipynb

## Introduction
This project showcases two statistical arbitrage strategies and their combination into a single portfolio. These strategies use historical daily price data from Binance, using Binance python API. These dynamic signals aim to outperform passive buy-and-hold strategies. Both strategies utilize a trend indicator called "Average Directional Index." This trend tends to predict when prices are showing momentum or reversal.

## Data Processing and Training Data
This portfolio uses historical daily high, low, and close price data from Binance, using Binance python API. The training data is split into a cross-sectional dataset utilizing randomly sampled high-market cap coins. A cross-sectional analysis is key to this strategy as different environments tend to show momentum and reversal at opposing times.

## Correlated Basket Pair Reversal
This strategy utilizes the idea that there is a general beta that drives crypto prices. When coins have a high correlation to one-another, they tend to show rever

