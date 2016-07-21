import utility.windutility as wu
import numpy as np
from datetime import date
import matplotlib.pyplot as plt

startdate = '2005-1-1'
enddate = date.today()
price1 = wu.wsd('801120.SI', 'close', startdate, enddate)
price2 = wu.wsd('000300.SH', 'close', startdate, enddate)
log_price1 = np.log(price1)
log_price2 = np.log(price2)
spread = log_price1 - log_price2
spread.plot()
'''
years = range(2008,2017)
yearlist = [str(year) for year in years]
for year in yearlist:
    spread[year].plot()
    '''