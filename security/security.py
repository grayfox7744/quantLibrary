# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 21:32:49 2015

@author: H00731
"""
import windutility as wu

class Security:
    def __init__(self, ticker, name):
        self.ticker = ticker
        self.name = name
        Security.wsd = wu.wsd

class Fund(Security):
    def __init__(self, ticker, name):
        Security.__init__(self, ticker, name)
    '''
    def getTradingShare(self, startdate, enddate):
        return  wu.wsd(self.ticker, 'unit_floortrading', startdate, enddate)

    def getTotalShare(self, startdate, enddate):
        return wu.wsd(self.ticker, 'unit_fundshare_total', startdate, enddate, 'period = Q')
     '''
    def calculatePosition(self, startdate, enddate):
        pass

class Afund(Fund):
    def __init__(self, ticker, name, bticker, mticker, iticker):
        Fund.__init__(self, ticker, name)
        self.bticker = bticker
        self.mticker = mticker
        self.iticker = iticker

    def getImpliedYield(self, startdate, enddate):
        # function to be improved
        tmp = wu.wsd(self.ticker, 'anal_nextaayield, nav, close', startdate, enddate)
        return tmp['anal_nextaayield'] / (tmp['close'] - (tmp['nav'] - 1))

    def getTotalDiscount(self, startdate, enddate):
        aprice = wu.wsd(self.ticker, 'close', startdate, enddate)['close']
        bprice = wu.wsd(self.bticker, 'close', startdate, enddate)['close']
        mnav = wu.wsd(self.mticker, 'nav', startdate, enddate)['nav']
        ashare = wu.wsd(self.ticker, 'fund_subshareproportion', startdate, enddate)['fund_subshareproportion']
        bshare = 100 - ashare
        totalDiscount = (aprice * ashare + bprice * bshare) / mnav / 100 - 1
        return totalDiscount

class Mfund(Fund):
    def __init__(self, ticker, name, aticker, bticker, iticker):
        Fund.__init__(self, ticker, name)
        self.aticker = aticker
        self.bticker = bticker
        self.iticker = iticker
    '''
    def getTotalDiscount(self, startdate, enddate):
        aprice = getaprice(self, startdate, enddate)['close']
        bprice = wu.wsd(self.bticker, 'close', startdate, enddate)['close']
        mnav = wu.wsd(self.ticker, 'nav', startdate, enddate)['nav']
        ashare = wu.wsd(self.aticker, 'fund_subshareproportion', startdate, enddate)['fund_subshareproportion']
        bshare = 100 - ashare
        totalDiscount = (aprice * ashare + bprice * bshare) / mnav / 100 - 1
        return totalDiscount
    '''

    def getaprice(self, startdate, enddate):
        aprice = wu.wsd(self.aticker, 'close', startdate, enddate)
        return aprice

    def getbprice(self, startdate, enddate):
        bprice = wu.wsd(self.bticker, 'close', startdate, enddate)
        return bprice

class Stock(Security):
    def __init__(self, ticker, name):
        Security.__init__(self, ticker, name)

class Option(Security):
    def __init__(self, ticker, name, underlying, optionType, strike, maturity):
        Security.__init__(self, ticker, name)
        self.underlying = underlying
        self.optionType = optionType
        self.strike = strike
        self.maturity = maturity

