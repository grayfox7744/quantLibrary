import itertools
import utility.windutility as wu
from utility import dataframefeed
from pyalgotrade import bar
from pyalgotrade.optimizer import local
from strategy import singleMA

instruments = ['000001.SH']
fromDate = '20000101'
toDate = '20160314'
frequency = bar.Frequency.DAY
feed = dataframefeed.Feed()
maPeriod = xrange(5,120)

for instrument in instruments:
    data = wu.wsd(instrument, 'open, high, low, close, volume, adjfactor', fromDate, toDate)
    data['adjclose'] = data['close'] * data['adjfactor'] / data['adjfactor'][-1]
    feed.addBarsFromDataFrame(instrument, data)


def parameters_generator():
    return itertools.product(instruments, maPeriod)

if __name__ == '__main__':
    local.run(singleMA.SingleMA, feed, parameters_generator())


