import utility.windutility as wu

indexPrice = wu.wsi('000905.SH', 'close', '2016-06-21', '2016-06-21 15:01:00')
futurePrice = wu.wsi('IC1609.CFE', 'close', '2016-06-21', '2016-06-21 15:01:00')
basis = futurePrice - indexPrice
basis.plot()