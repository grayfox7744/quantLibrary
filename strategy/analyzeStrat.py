from pyalgotrade import bar, plotter
import utility.windutility as wu
from utility import dataframefeed
from strategy import SingleMA
from pyalgotrade.stratanalyzer import drawdown
from pyalgotrade.stratanalyzer import sharpe

instrument = '000001.SH'
fromDate = '20000101'
toDate = '20121109'
frequency = bar.Frequency.DAY
paras = 20
plot = True

dat = wu.wsd(instrument, 'open, high, low, close, volume, adjfactor', fromDate, toDate)
dat['adjclose'] = dat['close'] * dat['adjfactor'] / dat['adjfactor'][-1]
feed = dataframefeed.Feed()
feed.addBarsFromDataFrame(instrument, dat)

strat = SingleMA.SingleMA(feed, instrument, paras)

# attach analyzers
drawdownAnalyzer = drawdown.DrawDown()
strat.attachAnalyzer(drawdownAnalyzer)
sharpeRatioAnalyzer = sharpe.SharpeRatio()
strat.attachAnalyzer(sharpeRatioAnalyzer)

if plot:
    plt = plotter.StrategyPlotter(strat, True, True, True)
    ma = strat.getMA()
    plt.getInstrumentSubplot('indicator').addDataSeries('ma', ma)
    # price = strat.getPrice()
    # plt.getInstrumentSubplot('price').addDataSeries('price', price)

strat.run()

if plot:
    plt.plot()

print "Max drawdown: %.2f%%" % (drawdownAnalyzer.getMaxDrawDown() * 100)
print "Sharpe ratio: %.2f" % (sharpeRatioAnalyzer.getSharpeRatio(0.03))