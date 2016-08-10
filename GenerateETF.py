# -*- coding: utf-8 -*-

# step1： 读入指数权重文件
import utility.windutility as wu
import pandas as pd
import numpy as np
from datetime import date, timedelta
import glob


today = date.today()
enddate = date.today() # should be last trading day
asset_dif = input('sub&red amount:')
target_pos = input('target position:')
# check 日期文件
datestr = enddate.strftime('%Y%m%d')
stmt = ("M://IMP//QZWJ//159949//*%s*.xlsx") % (datestr)
filename = glob.glob(stmt)

tmp = pd.read_excel(filename[0])
codes = tmp.iloc[:,1]
# transform, should write a function
rawTicker = ['%06.0f' % code for code in codes]
tmp['tickers'] = pd.Series([i + '.SH' if i[0] in {'5','6'} else i + '.SZ' for i in rawTicker])
tmp['share'] = tmp.iloc[:,4]
tmp['price'] = tmp.iloc[:,3]
tmp['weight'] =tmp.share * tmp.price /sum(tmp.share * tmp.price)
index = tmp[['tickers', 'weight', 'price']]


# step2: 读入持仓文件
tmp = pd.read_excel(u'M:\\分级基金\\50ETF\\综合信息查询_基金证券.xls')
tmp = tmp[:-1]
codes = tmp[u'证券代码']
rawTicker = ['%06.0f' % code for code in codes]
tmp['tickers'] = pd.Series([i + '.SH' if i[0] in {'5','6'} else i + '.SZ' for i in rawTicker])
tmp['position'] = tmp[u'持仓']
tmp['mv'] = tmp[u'市值']
holdings = tmp[['tickers','position', 'mv']]

equity = tmp[u'市值'].sum()
position = tmp[u'市值比净值(%)'].sum()

# step3: 检查是否停牌
status = wu.wss(list(holdings['tickers']), 'trade_status', today)
tmp =  pd.merge(holdings, status, left_on = 'tickers', right_index = True)
data = pd.merge(tmp, index)


# 计算

asset = equity / position * 100
asset = asset + asset_dif
equity_dif = asset * target_pos - equity  #今日买入

# 可交易列表
float = data[data['TRADE_STATUS'] == u'交易']
float_value = float['mv'].sum()
float_target_value = float_value + equity_dif

float['targetmv'] = float_target_value * float['weight'] / float['weight'].sum()
float['position_diff'] = (float['targetmv'] - float['mv']) / float['price']
float['volumn'] = np.round(float['position_diff'] / 100) * 100
# 生成交易单

tickerList = [i[0:6] for i in float.tickers]
direction = [1 if i > 0 else 2 for i in float.volumn]
amount  = list(np.abs(float.volumn))
priceMode1 = [1 for i in float.tickers]
priceMode2 = [1 for i in float.tickers]
marketCode = [1 if i[0] in {'5', '6'} else 2 for i in float.tickers]

tmp = [tickerList, direction, amount, priceMode1, priceMode2, marketCode]
tmp1 = np.transpose(tmp)

tmp2 = pd.DataFrame(tmp1, columns = ['ticker', 'direction', 'amount', 'mode1','mode2', 'mktcode'])
order = tmp2[tmp2['amount'] != '0.0']

orderfile = u'M:\\分级基金\\创业板50\\' + datestr + '.xlsx'
order.to_excel(orderfile, index = False)
