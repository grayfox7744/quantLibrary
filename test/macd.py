import utility.windutility as wu

diff = wu.wsd("000001.SH", "MACD", "2014-11-01", "2016-02-18", "MACD_L=26;MACD_S=12;MACD_N=9;MACD_IO=1;Fill=Previous")
dea = wu.wsd("000001.SH", "MACD", "2014-11-01", "2016-02-18", "MACD_L=26;MACD_S=12;MACD_N=9;MACD_IO=2;Fill=Previous")

macd = diff - dea

szzz = wu.wsd("000001.SH", "close", "2014-11-01", "2016-02-18")
rt = szzz.pct_change()

ind = macd.shift(1)

ind.plot()