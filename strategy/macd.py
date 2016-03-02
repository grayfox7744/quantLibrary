from pyalgotrade import strategy
from pyalgotrade.technical import macd

class MACD(strategy.BacktestingStrategy)
    def __init__(self, feed, instrument, fast, slow, signal, maxLen):
        strategy.BacktestingStrategy.__init__(self, feed)
        self._instrument = instrument
        self._macd = macd.MACD(feed[instrument],)
