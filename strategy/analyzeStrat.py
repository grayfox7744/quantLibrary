from pyalgotrade import bar
import utility.windutility as wu
from utility import dataframefeed
from strategy import singleMA
from pyalgotrade.stratanalyzer import drawdown, sharpe, returns, trades
import pandas as pd

instrument = '000001.SH'
fromDate = '20000101'
toDate = '20160314'
frequency = bar.Frequency.DAY
initialCash = 1000000
filepath = 'D://strategyResults//timing//ma//test5.csv'

dat = wu.wsd(instrument, 'open, high, low, close, volume, adjfactor', fromDate, toDate)
dat['adjclose'] = dat['close'] * dat['adjfactor'] / dat['adjfactor'][-1]

def run_strategy(paras):
    feed = dataframefeed.Feed()
    feed.addBarsFromDataFrame(instrument, dat)
    strat = singleMA.SingleMA(feed, instrument, paras, initialCash)

    # attach analyzersgc
    returnsAnalyzer = returns.Returns()
    strat.attachAnalyzer(returnsAnalyzer)
    drawdownAnalyzer = drawdown.DrawDown()
    strat.attachAnalyzer(drawdownAnalyzer)
    sharpeRatioAnalyzer = sharpe.SharpeRatio()
    strat.attachAnalyzer(sharpeRatioAnalyzer)
    tradeAnalyzer = trades.Trades()
    strat.attachAnalyzer(tradeAnalyzer)

    strat.run()
    print "Final portfolio value: $%.2f with paras %d" % (strat.getBroker().getEquity(), paras)
    return {
        'returns': returnsAnalyzer.getCumulativeReturns()[-1],
        'drawdown': drawdownAnalyzer.getMaxDrawDown(),
        'longestDrawDownDuration': drawdownAnalyzer.getLongestDrawDownDuration(),
        'sr': sharpeRatioAnalyzer.getSharpeRatio(0.03),
        'total trades': tradeAnalyzer.getCount(),
        'win': tradeAnalyzer.getProfitableCount(),
        'lose': tradeAnalyzer.getUnprofitableCount(),
        'average win profit': tradeAnalyzer.getPositiveReturns().mean(),
        'average lose loss': tradeAnalyzer.getNegativeReturns().mean(),
        'wining ratio': tradeAnalyzer.getProfitableCount() / tradeAnalyzer.getCount(),
        'odds': -tradeAnalyzer.getPositiveReturns().mean() / tradeAnalyzer.getNegativeReturns().mean()
    }


finalPortfolio = {}
for i in range(10,250,5):
    output = run_strategy(i)
    finalPortfolio[i] = output

df = pd.DataFrame(finalPortfolio)
df1 = df.transpose()
df1.to_csv(filepath)

