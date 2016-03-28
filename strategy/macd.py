from pyalgotrade import strategy
from pyalgotrade.technical import macd

class MACD(strategy.BacktestingStrategy)
    def __init__(self, feed, instrument, fast, slow, signal, maxLen):
        strategy.BacktestingStrategy.__init__(self, feed)
        self.__instrument = instrument
        self.__macd = macd.MACD(feed[instrument],)

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
        closePrice = bars[self.__instrument].getPrice()
        if self.__macd[-1] is None:
            return

        if self.__position is not None:
            if not self.__position.exitActive() and self.__macd[-1] < self.__macd[-2]:
                self.__position.exitMarket()

        if self.__position is None:
            if self.__macd[-1] > self.__macd[-2]:
                shares = int(self.getBroker().getEquity() * 0.9 / closePrice)
                self.__position = self.enterLong(self.__instrument, shares)

