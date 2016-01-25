import utility.windutility as wu
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import date, timedelta
from pptx import Presentation

# tracking 50ETF historical volatility and implied volatility

enddate = date.today() - timedelta(1)
startdate = enddate - timedelta(365)
ticker = '510050.SH, IVIX.SH'
data = wu.wsd(ticker, 'close', startdate, enddate)
# data['return'] = data['close'].pct_change()
# data['vol_5d'] = pd.rolling_std(data['return'], window = 5) * np.sqrt(240)
# data['vol_20d'] = pd.rolling_std(data['return'], window = 20) * np.sqrt(240)

plt.figure()
data.plot(secondary_y = 'IVIX.SH')
plt.savefig('D:\\reports\\pic\\1.png')

# pic 2: future basis and index of last 5 trading days, 1 min data
ticker = '000016.SH,'


# create ppt file
prs = Presentation('D:\\reports\\templet\\templet.pptx')

layout = prs.slide_layouts[0]
slide = prs.slides.add_slide(layout)
title = slide.shapes.title
subtitle = slide.placeholders[1]
title.text = "Weekly Report"
subtitle.text = "Generated on {:%Y-%m-%d}".format(date.today())

layout1 = prs.slide_layouts[1]
slide = prs.slides.add_slide(layout1)
title = slide.shapes.title
title.text = "50ETF & IVIX "
placeholder = slide.placeholders[1]
pic = placeholder.insert_picture('D:\\reports\\pic\\1.png')

prs.save('D:\\reports\\ppt\\sample.pptx')
