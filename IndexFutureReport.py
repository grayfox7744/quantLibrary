import pandas as pd
from pandas.tseries.offsets import MonthBegin
from datetime import datetime
import utility.windutility as wu

fromDate = raw_input('input fromDate date:')
toDate = raw_input('input toDate date:')
dateStr = raw_input('current Month in YYMM format:')

dateStr = datetime.strptime(dateStr,'%y%m')
interval = [0, 1, 3, 6]
monthList = [dateStr + i * MonthBegin() for i in interval]
strList = [datetime.strftime(i,'%y%m') for i in monthList]

icList = ['IC'+i+'.CFE' for i in strList]
ifList = ['IC'+i+'.CFE' for i in strList]
ihList = ['IC'+i+'.CFE' for i in strList]

indexList = ['000905.SH', '000300.SH', '000016.SH']
indexClose1 = wu.wss(indexList, 'close', fromDate)
indexClose2 = wu.wss(indexList, 'close', toDate)

icClose1 = wu.wss(icList, 'close', fromDate)
icClose2 = wu.wss(icList, 'close', toDate)

ic1 = indexClose1.CLOSE['000905.SH']
ic2 = indexClose2.CLOSE['000905.SH']

icStructure1 = (icClose1.CLOSE - ic1) / ic1
icStructure2 = (icClose2.CLOSE - ic2) / ic2

icStructure = pd.DataFrame([icStructure1,icStructure2],index = [fromDate, toDate])
tmp = icStructure.transpose()
tmp.plot()