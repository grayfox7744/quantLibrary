import utility.windutility as wu

indexPrice = wu.wsi('000905.SH', 'close', '2016-06-22', '2016-06-23 11:01:00')
futurePrice = wu.wsi('IC1609.CFE', 'close', '2016-06-22', '2016-06-23 11:01:00')
basis = futurePrice - indexPrice
# basis.plot()
futurePrice1 = wu.wsi('IC1607.CFE', 'close', '2016-06-22', '2016-06-23 11:01:00')
futurebasis = futurePrice - futurePrice1
futurebasis.plot()