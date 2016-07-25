import pandas as pd
from datetime import date
import glob

today = date.today()

# find index file
datestr = today.strftime('%Y%m%d')
stmt = ("M://IMP//QZWJ//159949//*%s*.xlsx") % (datestr)
filename = glob.glob(stmt)

pd.read_excel(filename[0])