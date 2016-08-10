import utility.windutility as wu
from datetime import date

# ticker = input('ticker')

today = date.today()
startdate = wu.tdaysoffset(-30, today)
enddate = wu.tdaysoffset(-1, today)

bars = wu.wsd('000001.SH','high, low, pre_close', startdate, enddate)
bars['a'] = bars.high - bars.low
bars['b'] = bars.high - bars.pre_close
bars['c'] = bars.pre_close - bars.low
bars1 = bars[['a','b','c']]
bars['atr'] = bars1.max(axis = 1)

writer = pd.ExcelWriter('D://reports//volatility.xlsx', engine='xlsxwriter')
bars.to_excel(writer)
writer.save()