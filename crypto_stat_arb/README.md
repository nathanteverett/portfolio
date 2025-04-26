# Statistical Arbitrage in Crypto: Predicting Momentum and Reversal
### A quant strategy by Nathan T. Everett

Key:
1. Momentum strategy: Crypto Momentum Directional Index Strategy.ipynb
2. Reversal strategy: Correlated Basket Pair Reversal in Crypto.ipynb
3. Combo strategy: Directional Index Reveral and Momentum Strategy.ipynb

## Introduction
This project showcases two statistical arbitrage strategies and their combination into a single portfolio. These strategies use historical daily price data from Binance, using Binance python API. These dynamic signals aim to outperform passive buy-and-hold strategies. Both strategies utilize a trend indicator called Average Directional Index (ADI). This trend tends to predict when prices are showing momentum or reversal.

## Data Processing and Training Data
This portfolio uses historical daily high, low, and close price data from Binance, using Binance python API. The training data is split into a cross-sectional dataset utilizing randomly sampled high-market cap coins. A cross-sectional analysis is key to this strategy as different environments tend to show momentum and reversal at opposing times. Both data sets span January 2019 - April 2025. 

## Correlated Basket Pair Reversal
### Strategy
This strategy utilizes the idea that there is a general beta that drives crypto prices. When coins have a high correlation to one-another, they tend to be affected by the same beta strongly. When coins diverge from one another, then there is an arbitrage opportunity. Using a basket of coins, we can utilize these changes and amplify their effects. The basket is updated by a correlation on a rolling window. When coins are locally correlated, the arbitrage opportunity tends to be stronger. The reversal is done by finding the residual of the linear regressions of a basket of targets and a master coin. Note this is not a multiple regression, but the basket is a set of target variables on a the single independent (master) coin.

Finally, we use a trend indicator to determine whether or not we are in a reversal regime. A trend is found through a series of smoothed signals. When the direction of the trend is frequently changing, this indicated an environment that is beneficial for reversal.

### Performance
The dollar-neutral nature of this strategy made it's alpha very robust. It has a net sharpe of 2.22 and an information ratio of 2.18 when BTCUSDT is used as the master coin. A complete summary of performance can be found in table 1 below.
![Reversal strat results](reversal strat.png)

## Momentum Directional Index Strategy 
This strategy uses the ADI trend indicator to find momentum environments in crypto. It utilizes big market cap coins which are more robust to trend prediction due to their large trading volume.
