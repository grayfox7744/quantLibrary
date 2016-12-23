import utility.windutility as wu
from datetime import date
# future daily basis
beginDate = '2016-12-16'
endDate = date.today().strftime('%Y-%m-%d')

indexPrice = wu.wsd('000905.SH', 'close', beginDate, endDate)
futurePrice = wu.wsd('IC1701.CFE', 'close', beginDate, endDate)
basis = futurePrice - indexPrice
# basis.plot()
