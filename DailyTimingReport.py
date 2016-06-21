import utility.windutility as wu
import numpy as np
from datetime import date
import talib
tickerList = ['000001.SH']

# enddate = wu.tdaysoffset(-1, date.today())
enddate = date.today()
startdate = wu.tdaysoffset(-240, date.today())
data = wu.wsd(tickerList, 'close', startdate, enddate)
close = np.array(list(data['close']))
talib.MACD(close)