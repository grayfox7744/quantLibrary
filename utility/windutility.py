# -*- coding: utf-8 -*-
"""
Created on Thu Sep 17 10:07:46 2015

@author: H00731
"""

import pandas as pd
from WindPy import w

w.start()

def wsd(tickers, fields, startdate, enddate, cfg=""):
    if isinstance(tickers,str):
        tickers = tickers.replace(',','').split()

    if isinstance(fields,str):
        fields = fields.replace(',','').split()

    if len(tickers) == 1:
        tmp = w.wsd(tickers, fields, startdate, enddate, cfg)
        return pd.DataFrame(dict(zip(fields, tmp.Data)),index = tmp.Times)
    elif len(fields) == 1:
        tmp = w.wsd(tickers, fields, startdate, enddate, cfg)
        return pd.DataFrame(dict(zip(tickers, tmp.Data)),index = tmp.Times)
    else:
        print 'cannot surrport multiple code with multiple fields'


def wss(tickers, fields, date):
    if isinstance(tickers,str):
        tickers = tickers.replace(',','').split()

    if isinstance(fields,str):
        fields = fields.replace(',','').split()

    tmp = w.wss(tickers, fields, 'tradedate = %s'%(date))
    return pd.DataFrame(dict(zip(tmp.Fields, tmp.Data)),index = tmp.Codes, columns= tmp.Fields)



def wsi(tickers, fields, startdate, enddate):
    if isinstance(tickers,str):
        tickers = tickers.replace(',','').split()

    if isinstance(fields,str):
        fields = fields.replace(',','').split()

    if len(tickers) == 1:
        tmp = w.wsi(tickers, fields, startdate, enddate)
        return pd.DataFrame(dict(zip(fields, tmp.Data)),index = tmp.Times)
    elif len(fields) == 1:
        tmp = w.wsi(tickers[0], fields, startdate, enddate)
        df = pd.DataFrame(dict(zip([tickers[0]], tmp.Data)),index = tmp.Times)

        for ticker in tickers[1:]:
            tmp = w.wsi(ticker, fields, startdate, enddate)
            df1 = pd.DataFrame(dict(zip([ticker], tmp.Data)),index = tmp.Times)
            df = pd.merge(df, df1, left_index = True, right_index = True)

        return df
    else:
        print 'cannot surrport multiple code with multiple fields'

def tdaysoffset(n, date):
    tmp =  w.tdaysoffset(n, date)
    return tmp.Data[0][0]

if __name__ == '__main__':
    import utility.windutility as wu
    # data = wu.wsi('150018.SZ, 150019.SZ', 'close',"2016-01-25 09:00:00", "2016-01-25 10:37:00" )
    # wu.wss("000006.SZ,000002.SZ", "trade_status,high",'2016-1-16')
    w.wsd('000001.SZ', 'pe', '2016-1-1','2016-3-1',)
    print(data)


def edb(code,startdate, enddate,name):
        tmp = w.edb(code,  startdate, enddate)
        return pd.DataFrame(dict(zip([name], tmp.Data)),index = tmp.Times)

