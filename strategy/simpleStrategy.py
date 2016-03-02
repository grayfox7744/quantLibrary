from pyalgotrade import strategy
from pyalgotrade.barfeed import yahoofeed
from pyalgotrade.stratanalyzer import returns
from pyalgotrade.stratanalyzer import sharpe
from pyalgotrade.utils import stats
from pyalgotrade.tools import yahoofinance


class MyStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed):
        strategy.BacktestingStrategy.__init__(self, feed, 1000000)

        # We wan't to use adjusted close prices instead of close.
        self.setUseAdjustedValues(True)

        # Place the orders to get them processed on the first bar.
        orders = {
            "aeti": 297810,
            "egan": 81266,
            "glng": 11095,
            "simo": 17293,
        }
        for instrument, quantity in orders.items():
            self.marketOrder(instrument, quantity, onClose=True, allOrNone=True)

    def onBars(self, bars):
        pass

# Load the yahoo feed from CSV files.
feed = yahoofeed.Feed()
yahoofinance.download_daily_bars("aeti",2011, "D:\\aeti-2011-yahoofinance.csv")
yahoofinance.download_daily_bars("egan", 2011, "D:\\egan-2011-yahoofinance.csv")
yahoofinance.download_daily_bars("glng", 2011, "D:\\glng-2011-yahoofinance.csv")
yahoofinance.download_daily_bars("simo", 2011, "D:\\simo-2011-yahoofinance.csv")
feed.addBarsFromCSV("aeti", "D:\\aeti-2011-yahoofinance.csv")
feed.addBarsFromCSV("egan", "D:\\egan-2011-yahoofinance.csv")
feed.addBarsFromCSV("glng", "D:\\glng-2011-yahoofinance.csv")
feed.addBarsFromCSV("simo", "D:\\simo-2011-yahoofinance.csv")

# Evaluate the strategy with the feed's bars.
myStrategy = MyStrategy(feed)

# Attach returns and sharpe ratio analyzers.
retAnalyzer = returns.Returns()
myStrategy.attachAnalyzer(retAnalyzer)
sharpeRatioAnalyzer = sharpe.SharpeRatio()
myStrategy.attachAnalyzer(sharpeRatioAnalyzer)

# Run the strategy
myStrategy.run()

# Print the results.
print "Final portfolio value: $%.2f" % myStrategy.getResult()
print "Anual return: %.2f %%" % (retAnalyzer.getCumulativeReturns()[-1] * 100)
print "Average daily return: %.2f %%" % (stats.mean(retAnalyzer.getReturns()) * 100)
print "Std. dev. daily return: %.4f" % (stats.stddev(retAnalyzer.getReturns()))
print "Sharpe ratio: %.2f" % (sharpeRatioAnalyzer.getSharpeRatio(0))