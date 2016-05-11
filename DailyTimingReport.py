import utility.windutility as wu
from datetime import date
tickerList = ['000001.SH']

enddate = wu.tdaysoffset(-1, date.today())
startdate = wu.tdaysoffset(-240, date.today())
wu.wsd(tickerList, 'close', startdate, enddate)
close = np.array(list(data['close']))