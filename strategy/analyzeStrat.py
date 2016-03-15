from pyalgotrade import bar, plotter
import utility.windutility as wu
from utility import dataframefeed
from strategy import SingleMA
from pyalgotrade.stratanalyzer import drawdown, sharpe, returns, trades
import pandas as pd

instrument = 'CU.SHF'
fromDate = '20000730'
toDate = '20121109'
frequency = bar.Frequency.DAY
initialCash = 10000000
plot = False

dat = wu.wsd(instrument, 'open, high, low, close, volume, adjfactor', fromDate, toDate)
dat['adjclose'] = dat['close'] * dat['adjfactor'] / dat['adjfactor'][-1]

def run_strategy(paras):
    feed = dataframefeed.Feed()
    feed.addBarsFromDataFrame(instrument, dat)
    strat = SingleMA.SingleMA(feed, instrument, paras, initialCash)

# attach analyzers
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
    return {'returns':strat.getBroker().getEquity(), 'drawdown':drawdownAnalyzer.getMaxDrawDown(),'sr':sharpeRatioAnalyzer.getSharpeRatio(0.03),
            'total trades': tradeAnalyzer.getCount(),'win':tradeAnalyzer.getProfitableCount(), 'lose': tradeAnalyzer.getUnprofitableCount(),
            'average win profit': tradeAnalyzer.getPositiveReturns().mean(), 'average lose loss': tradeAnalyzer.getNegativeReturns().mean()}

    '''
    if plot:
         plt = plotter.StrategyPlotter(strat, True, True, True)
         ma = strat.getMA()
          plt.getInstrumentSubplot('15indicator').addDataSeries('ma', ma)
          plt.getOrCreateSubplot("returns").addDataSeries("simple return", returnsAnalyzer.getCumulativeReturns())
    '''

finalPortfolio = {}
for i in range(10,30):
    output = run_strategy(i)
    finalPortfolio[i] = output

df = pd.DataFrame(finalPortfolio)
print df
df.to_csv('D://strategyResults//timing//ma//test4.csv')

# print "Max drawdown: %.2f%%" % (drawdownAnalyzer.getMaxDrawDown() * 100)
# print "Sharpe ratio: %.2f" % (sharpeRatioAnalyzer.getSharpeRatio(0.03))