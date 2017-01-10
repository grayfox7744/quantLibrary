from pyalgotrade import strategy
from pyalgotrade.broker.fillstrategy import DefaultStrategy
from pyalgotrade.broker.backtesting import TradePercentage
from pyalgotrade.technical import macd
from pyalgotrade.dataseries import SequenceDataSeries
from pyalgotrade.talibext import indicator
from datetime import datetime

class MACD(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, fast, slow, signal, initialCash = 1000000):
        strategy.BacktestingStrategy.__init__(self, feed, initialCash)
        self.__instrument = instrument
        self.getBroker().setFillStrategy(DefaultStrategy(None))
        self.getBroker().setCommission(TradePercentage(0.001))
        self.__position = None
        self.__prices = feed[instrument].getPriceDataSeries()
        self.__fast = int(fast)
        self.__slow = int(slow)
        self.__signal = int(signal)

    def getPrice(self):
        return self.__prices

    def getMACD(self):
        return self.__macd

    def onEnterOk(self, position):
        execInfo = position.getEntryOrder().getExecutionInfo()
        instrumentInfo = position.getInstrument()
        self.info("BUY %s at $%.2f" % (instrumentInfo, execInfo.getPrice()))

    def onEnterCanceled(self, position):
        self.__position.exitMarket()

    def onExitOk(self, position):
        execInfo = position.getExitOrder().getExecutionInfo()
        instrumentInfo = position.getInstrument()
        self.info("SELL %s at $%.2f" % (instrumentInfo, execInfo.getPrice()))
        self.__position = None

    def onExitCanceled(self, position):
        self.__position.exitMarket()

    def onBars(self, bars):
        # closePrice = bars[self.__instrument].getPrice()
        closePrice = self.getFeed().getDataSeries(instrument).getCloseDataSeries()
        date = bars.getDateTime()
        
        self.__dif, self.__dea, self.__macd = indicator.MACD(closePrice, 200, self.__fast, self.__slow, self.__signal)


        if date < date1:
            return
        
        if self.__macd[-1] is None:
            return

        if self.__position is not None:
            if not self.__position.exitActive() and self.__macd[-1] < 0:
                self.__position.exitMarket()

        if self.__position is None:
            if self.__macd[-1] > 0:
                shares = int(self.getBroker().getEquity() * 0.9 / bars[self.__instrument].getPrice())
                self.__position = self.enterLong(self.__instrument, shares)

if __name__ == "__main__":
    from pyalgotrade import bar, plotter
    import utility.windutility as wu
    from utility import dataframefeed
    from pyalgotrade.stratanalyzer import returns, drawdown

    strat = MACD
    # instrument = '000001.SH'
    instrument = '000300.SH'
    fromDate = '20040104'
    toDate = '20170105'
    date1 = datetime(2005,1,1)
    frequency = bar.Frequency.DAY
    paras = [12, 26, 9]
    plot = True

    data = wu.wsd(instrument, 'open, high, low, close, volume, adjfactor', fromDate, toDate)
    data['adjclose'] = data['close'] * data['adjfactor'] / data['adjfactor'][-1]
    # data = wu.wsi(instrument, 'open, high, low, close, volume', fromDate, toDate)
    feed = dataframefeed.Feed()
    feed.addBarsFromDataFrame(instrument, data)

    strat = strat(feed, instrument, *paras)

    returnsAnalyzer = returns.Returns()
    strat.attachAnalyzer(returnsAnalyzer)
    
    drawDownAnalyzer = drawdown.DrawDown()
    strat.attachAnalyzer(drawDownAnalyzer)

    if plot:
        # plt = plotter.StrategyPlotter(strat, True, True, True)
        # ma = strat.getMA()
        # plt.getInstrumentSubplot('indicator').addDataSeries('ma', ma)
        plt = plotter.StrategyPlotter(strat)
        # plt.getInstrumentSubplot(instrument).addDataSeries('macd', strat.getMACD())
        plt.getOrCreateSubplot('returns').addDataSeries('simple return', returnsAnalyzer.getReturns())
        # pos = strat.getPos()
        # plt.getOrCreateSubplot("position").addDataSeries("position", pos)

    strat.run()
    
    print "max draw down: %2.f %%" % (drawDownAnalyzer.getMaxDrawDown() * 100)

    if plot:
        plt.plot()