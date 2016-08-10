from datetime import date
import glob
import pandas as pd
from dbfread import DBF
import utility.windutility as wu

asset = input('fund asset:')
targetPosition = input('target position:')
# find index file
today = date.today()
datestr = today.strftime('%Y%m%d')
stmt = ("M://IMP//QZWJ//159949//*%s*.dbf") % (datestr)
filename = glob.glob(stmt)

# read index dbf file to get holdings
s = []
for row in DBF(filename[0],encoding='iso-8859-1'):
    s.append(row)

tmp = pd.DataFrame(s)
codes = tmp['ZQDM']
rawTicker = ['%06.0f' % float(code) for code in codes]
tickers = [i + '.SH' if i[0] in {'5','6'} else i + '.SZ' for i in rawTicker]
tmp['tickers'] = pd.Series(tickers)
tmp['share'] = tmp['JRLTGS']
index = tmp[['tickers', 'share']]

# read holding file
tmp = pd.read_excel(u'M:\\分级基金\\50ETF\\综合信息查询_组合证券.xls')
tmp = tmp[:-1]
codes = tmp[u'证券代码']
rawTicker = ['%06.0f' % code for code in codes]
tmp['tickers'] = pd.Series([i + '.SH' if i[0] in {'5','6'} else i + '.SZ' for i in rawTicker])
tmp['name'] = tmp[u'证券名称']
tmp['position'] = tmp[u'持仓']
holdings = tmp[['tickers','name','position']]

# get prices
price = wu.wsq(tickers, 'rt_latest, rt_trade_status')

# merge
tmp = pd.merge(index, price, left_on= 'tickers', right_index = True)
data = pd.merge(tmp, holdings, how = 'left')
data.rename(columns = {'RT_LATEST':'price'}, inplace = True)
data.rename(columns = {'RT_TRADE_STATUS':'status'}, inplace = True)
data = data.fillna(0)

# calulate indicators on data
data['indexWeight'] = data.share * data.price / sum(data.share * data.price)
data['targetHoling'] = asset * targetPosition * data.indexWeight / data.price
data['hodingDiff'] = data['targetHoling'] - data['position']
data['holdingWeight'] = data.position * data.price / sum(data.position * data.price)
data['weightDiff'] = data['indexWeight'] - data['holdingWeight']

# save to excel
file = u'M:\\分级基金\\etfDailyReport\\159949.xlsx'
data.to_excel(file, index = False)
