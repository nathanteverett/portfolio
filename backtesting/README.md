# 10-Year Mean-Reversion Investment Strategy Backtest
By Nathan T. Everett

## Introduction

This program is the implementation of a mean-reversion trading strategy based on the simple moving average (SMA) of top performing stocks. The data comes from yfinance, a python package that utilizes Yahoo's API on historical market data. The data set provides daily stock prices. Therefore, all of the prices are evaluated daily on market close.

The goal of this strategy is to get more exposure to the top companies of the S&P 500 than the index or its ETFs alone. Of course being so closely related to the S&P will mean that it will be strongly correlated. However, the goal of this strategy is to investigate if exposure to the top 10 companies alone will be significant enough to outperform the index as a whole. 
## Methods

In the following backtest, five 10-year periods were selected: 2015-2025, 2011-2021, 2005-2015, 2000-2010, 1995-2005. These periods were chosen to investigate the effect in bull markets like 2011-2021 and 2015-2025, and bear markets where a bubble popped in the middle and end of these periods, like 1995-2005 and 2000-2010, respectively. 

The strategy looks at the top 10 performing stocks in the S&P 500 at the beginning of the starting date. When a stock dips below its 20-day SMA by 10%, the stock is purchased. The amount of cash spent of each stock is fixed at \\$500 per investment. In addition to a modest starting amount of \\$10,000, a cash flow of \\$1,000 per month is also assumed for the duration. Furthermore, a brokerage fee of 2% annually, compounding annually, is assumed. No selling of stocks occurs. 

For each period, the portfolio was compared to a  simple dollar cost averaging (DCA) strategy on the SPY ETF. The initial amount was put into the SPY right away, and each monthly cash flow was immediately invested.

## Results

For strong bull markets, this strategy works well. Most noticably this strategy outperformed the S&P in the 2015-2025 period. In this era, the strategy yielded 243.72% ROI while the SPY portfolio yielded 123.10% ROI.

However, all of the other four periods did not out-perform the SPY. This likely happened for a few reasons. Firstly, many of these stocks are not mean-reverting; many companies that are in the top of the S&P at the start time did not stay in the top by the end. While the S&P restructures often, this strategy follows the companies until the end of the period. 

Furthermore, this strategy was very weak in bear markets. In the worst case, the strategy yielded a negative ROI of -8.41% in the 2000-2010 period. The SPY portfolio didn't do well at this time either, as the market was in its early recovery phase after the 2008 financial crisis, but the losses were still more pronounced than compared to the SPY portfolio.

## Conclusion

The strategy is not effective in its current state. In the era of the magnificent 7 it would likely perform very well. However, a bull run that we have seen in the last 15 years is unprecedented. There would be no way to guess that this strategy would work without forward knowledge. The S&P wins again.

## Outlook 

There are many things that could improve this strategy. Firstly, the portfolio should be more adaptive. Stocks should be sold at relative peaks and there should be preparation for restructuring to reflect the S&P. Secondly, the threshold for the SMA should correlate with the amount of stock purchased. The better the deal of the stock, the more you should buy. Finally, SMA average time should be optimized. Many of the parameters in this investigation were kept constant. Adaptive parameters could help yield higher returns and protect against non-mean-reverting stocks
