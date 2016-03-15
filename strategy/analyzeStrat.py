from pyalgotrade import bar, plotter
import utility.windutility as wu
from utility import dataframefeed
from strategy import SingleMA
from pyalgotrade.stratanalyzer import drawdown, sharpe, returns
import pandas as pd

instrument = '000001.SH'
fromDate = '20000101'
toDate = '20121109'
frequency = bar.Frequency.DAY
paras = 10
plot = False

dat = wu.wsd(instrument, 'open, high, low, close, volume, adjfactor', fromDate, toDate)
dat['adjclose'] = dat['close'] * dat['adjfactor'] / dat['adjfactor'][-1]

def run_strategy(paras):
    feed = dataframefeed.Feed()
    feed.addBarsFromDataFrame(instrument, dat)
    strat = SingleMA.SingleMA(feed, instrument, paras)

# attach analyzers
    returnsAnalyzer = returns.Returns()
    strat.attachAnalyzer(returnsAnalyzer)
    drawdownAnalyzer = drawdown.DrawDown()
    strat.attachAnalyzer(drawdownAnalyzer)
    sharpeRatioAnalyzer = sharpe.SharpeRatio()
    strat.attachAnalyzer(sharpeRatioAnalyzer)

    strat.run()
    print "Final portfolio value: $%.2f with paras %d" % (strat.getBroker().getEquity(), paras)
    return strat.getBroker().getEquity()

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

print finalPortfolio
output = pd.DataFrame(finalPortfolio)

# print "Max drawdown: %.2f%%" % (drawdownAnalyzer.getMaxDrawDown() * 100)
# print "Sharpe ratio: %.2f" % (sharpeRatioAnalyzer.getSharpeRatio(0.03))