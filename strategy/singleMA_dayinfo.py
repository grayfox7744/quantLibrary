from pyalgotrade import strategy
from pyalgotrade.broker.fillstrategy import DefaultStrategy
from pyalgotrade.broker.backtesting import TradePercentage
from pyalgotrade.technical import ma
from pyalgotrade.technical import cross

class singleMA(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, length, initialCash = 1000000):
        strategy.BacktestingStrategy.__init__(self, feed, initialCash)
        self.__instrument = instrument
        self.getBroker().setFillStrategy(DefaultStrategy(None))
        self.getBroker().setCommission(TradePercentage(0.001))
        self.__position = None
        self.__prices = feed[instrument].getPriceDataSeries()
        self.__malength = int(length)

        self.__ma = ma.SMA(self.__closeD, self.__malength)

        self.__datetime = feed[instrument].getDateTimes()
        self.__open = feed[instrument].getOpenDataSeries()
        self.__high = feed[instrument]. getHighDataSeries()
        self.__low = feed[instrument].getLowDataSeries()
        self.__close = feed[instrument].getCloseDataSeries()

    def getPrice(self):
        return self.__prices

    def getMA(self):
        return self.__ma

    def onEnterCanceled(self, position):
        self.__position = None

    def onEnterOk(self, position):
        pass

    def onExitCanceled(self, position):
        self.__position.exitMarket()

    def onExitOk(self, position):
        self.__position = None

    def onBars(self, bars):

        if self.__ma[-1] is None:
            return

        if self.__position is not None:
            if not self.__position.exitActive() and cross.cross_below(self.__prices, self.__ma):
                self.__position.exitMarket()

        if self.__position is None:
            if cross.cross_above(self.__prices, self.__ma):
                shares = int(self.getBroker().getEquity() * 0.2 / bars[self.__instrument].getPrice())
                self.__position = self.enterLong(self.__instrument, shares)

    def dayInfo(self, bar):
        try:
            self.__openD[-1]
        except AttributeError:
            self.__openD = []
            self.__highD = []
            self.__lowD = []
            self.__closeD = []
            self.__upper_limit = []
            self.__lower_limit = []

        if len(self.__datetime) < 2:
            self.__openD.append(bar.getOpen())
            self.__highD.append(self.__high[-1])
            self.__lowD.append(self.__low[-1])
            self.__closeD.append(self.__close[-1])
            return

        # if another day
        if self.__datetime[-1].date() != self.__datetime[-2].date():
            self.__openD.append(bar.getOpen())
            self.__highD.append(self.__high[-1])
            self.__lowD.append(self.__low[-1])
            self.__closeD.append(self.__close[-1])
            self.__upper_limit.append(round(round(self.__closeD[-2] * 1.1 * 1000) / 10) / 100)
            self.__lower_limit.append(round(round(self.__closeD[-2] * 0.9 * 1000) / 10) / 100)
            print self.__datetime[-1].date(), self.__datetime[-2].date(), self.__openD[-1]

        elif self.__datetime[-1].date() == self.__datetime[-2].date():
            if self.__high[-1] > self.__highD[-1]:
                self.__highD[-1] = self.__high[-1]

            if self.__low[-1] < self.__lowD[-1]:
                self.__lowD[-1] = self.__low[-1]

            self.__closeD[-1] = self.__close[-1]

if __name__ == '__main__':
    from pyalgotrade import bar, plotter
    import utility.windutility as wu
    from utility import dataframefeed
    from pyalgotrade.stratanalyzer import returns

    strat = singleMA
    instrument = '000001.SH'
    fromDate = '20120318'
    toDate = '20160317'
    frequency = bar.Frequency.MINUTE
    paras = [20]
    plot = True

    data = wu.wsi(instrument, 'open, high, low, close, volume', fromDate, toDate)
    # data['adjclose'] = data['close'] * data['adjfactor'] / data['adjfactor'][-1]
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
