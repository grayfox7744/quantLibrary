from pyalgotrade import strategy
from pyalgotrade.broker.fillstrategy import DefaultStrategy
from pyalgotrade.broker.backtesting import TradePercentage
from pyalgotrade.technical import ma

class SingleMA(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, n):
        strategy.BacktestingStrategy.__init__(self, feed)
        self.__instrument = instrument
        self.getBroker().setFillStrategy(DefaultStrategy(None))
        self.getBroker().setCommission(TradePercentage(0.001))
        self.__position = None
        self.__prices = feed[instrument].getPriceDataSeries()
        self.__malength = int(n)
        self.__ma = ma.SMA(self.__prices, self.__malength)

    def getPrice(self):
        return self.__prices

    def getMA(self):
        return self.__ma

    def onEnterCanceled(self, position):
        self.__position = None

    def onEnterOk(self, position):
        execInfo = position.getEntryOrder().getExecutionInfo()
        self.info("BUY at $%.2f" % (execInfo.getPrice()))

    def onExitOk(self, position):
        execInfo = position.getExitOrder().getExecutionInfo()
        self.info("SELL at $%.2f" % (execInfo.getPrice()))
        self.__position = None

    def onExitCancelled(self, position):
        self.__position.exitMarket()


    def onBars(self, bars):
        closePrice = bars[self.__instrument].getPrice()

        if self.__ma[-1] is None:
            return

        if self.__position is not None:
            if not self.__position.exitActive() and closePrice < self.__ma[-1]:
                self.__position.exitMarket()

        if self.__position is None:
            if closePrice > self.__ma[-1]:
                shares = int(self.getBroker().getEquity() * 0.9 / bars[self.__instrument].getPrice())
                self.__position = self.enterLong(self.__instrument, shares)


if __name__ == "__main__":
    from pyalgotrade import bar, plotter
    import utility.windutility as wu
    from utility import dataframefeed

    strat = SingleMA
    instrument = '000001.SH'
    fromDate = '20000101'
    toDate = '20160311'
    frequency = bar.Frequency.DAY
    paras = [20]
    plot = True

    dat = wu.wsd(instrument, 'open, high, low, close, volume, adjfactor', fromDate, toDate)
    dat['adjclose'] = dat['close'] * dat['adjfactor'] / dat['adjfactor'][-1]
    feed = dataframefeed.Feed()
    feed.addBarsFromDataFrame(instrument, dat)

    strat = strat(feed, instrument, *paras)



    if plot:
        plt = plotter.StrategyPlotter(strat, True, True, True)
        ma = strat.getMA()
        plt.getInstrumentSubplot('indicator').addDataSeries('ma', ma)
        # price = strat.getPrice()
        # plt.getInstrumentSubplot('price').addDataSeries('price', price)

    strat.run()

    if plot:
        plt.plot()