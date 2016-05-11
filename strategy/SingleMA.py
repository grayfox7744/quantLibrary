from pyalgotrade import strategy
from pyalgotrade.broker.fillstrategy import DefaultStrategy
from pyalgotrade.broker.backtesting import TradePercentage
from pyalgotrade.technical import ma
from pyalgotrade.dataseries import SequenceDataSeries

class SingleMA(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, n, initialCash = 1000000):
        strategy.BacktestingStrategy.__init__(self, feed, initialCash)
        self.__instrument = instrument
        self.getBroker().setFillStrategy(DefaultStrategy(None))
        self.getBroker().setCommission(TradePercentage(0.001))
        self.__position = None
        self.__prices = feed[instrument].getPriceDataSeries()
        self.__malength = int(n)
        self.__ma = ma.SMA(self.__prices, self.__malength)
        self.__pos = SequenceDataSeries() # record signal

    def getPrice(self):
        return self.__prices

    def getMA(self):
        return self.__ma

    def testCon(self):
        if self.__position is not None:
            self.__pos.append(1)
        elif self.__position is None:
            self.__pos.append(0)

    def getPos(self):
        return self.__pos

    def onEnterCanceled(self, position):
        self.__position = None

    def onEnterOk(self, position):
        execInfo = position.getEntryOrder().getExecutionInfo()
        instrumentInfo = position.getInstrument()
        self.info("BUY %s at $%.2f" % (instrumentInfo, execInfo.getPrice()))

    def onExitOk(self, position):
        execInfo = position.getExitOrder().getExecutionInfo()
        instrumentInfo = position.getInstrument()
        self.info("SELL %s at $%.2f" % (instrumentInfo, execInfo.getPrice()))
        self.__position = None

    def onExitCancelled(self, position):
        self.__position.exitMarket()


    def onBars(self, bars):
        closePrice = bars[self.__instrument].getPrice()

        if self.__ma[-1] is None:
            return

        self.testCon()

        if self.__position is not None:
            if not self.__position.exitActive() and closePrice < self.__ma[-1]:
                self.__position.exitMarket()

        if self.__position is None:
            if closePrice > self.__ma[-1]:
                shares = int(self.getBroker().getEquity() * 0.9 / closePrice)
                self.__position = self.enterLong(self.__instrument, shares)


if __name__ == "__main__":
    from pyalgotrade import bar, plotter
    import utility.windutility as wu
    from utility import dataframefeed
    from pyalgotrade.stratanalyzer import returns

    strat = SingleMA
    instrument = '000001.SH'
    fromDate = '20100101'
    toDate = '20160331'
    frequency = bar.Frequency.DAY
    paras = [20]
    plot = True

    data = wu.wsd(instrument, 'open, high, low, close, volume, adjfactor', fromDate, toDate)
    data['adjclose'] = data['close'] * data['adjfactor'] / data['adjfactor'][-1]
    feed = dataframefeed.Feed()
    feed.addBarsFromDataFrame(instrument, data)

    strat = strat(feed, instrument, *paras)

    returnsAnalyzer = returns.Returns()
    strat.attachAnalyzer(returnsAnalyzer)

    if plot:
        # plt = plotter.StrategyPlotter(strat, True, True, True)
        # ma = strat.getMA()
        # plt.getInstrumentSubplot('indicator').addDataSeries('ma', ma)
        plt = plotter.StrategyPlotter(strat)
        plt.getInstrumentSubplot(instrument).addDataSeries('ma', strat.getMA())
        plt.getOrCreateSubplot('returns').addDataSeries('simple return', returnsAnalyzer.getReturns())
        # pos = strat.getPos()
        # plt.getOrCreateSubplot("position").addDataSeries("position", pos)

    strat.run()

    if plot:
        plt.plot()