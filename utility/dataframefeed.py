# -*- coding: utf-8 -*-
"""
Created on Tue Mar 08 22:26:36 2016

@author: Administrator
"""
from pyalgotrade.barfeed import membf
from pyalgotrade import dataseries
from pyalgotrade import bar


class Feed(membf.BarFeed):
    def __init__(self, frequency=bar.Frequency.DAY, maxLen=dataseries.DEFAULT_MAX_LEN):
        membf.BarFeed.__init__(self, frequency, maxLen)
    
    def barsHaveAdjClose(self):
        return True  
        
    def addBarsFromDataFrame(self, instrument, df):
        loadedBars = []
        for row in df.iterrows():
            dateTime = row[0]
            open_ = row[1]['open']
            high = row[1]['high']
            low = row[1]['low']
            close = row[1]['close']
            volume = row[1]['volume']
            try:
                adjclose = row[1]['adjclose']
            except KeyError:
                adjclose = None

            bar_ = bar.BasicBar(dateTime, open_, high, low, close, volume, adjclose, self._BaseBarFeed__frequency)
            loadedBars.append(bar_)
            
        self.addBarsFromSequence(instrument, loadedBars)
        
        