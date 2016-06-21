import utility.windutility as wu
import numpy as np
import talib
import matplotlib.pyplot as plt

szzz = wu.wsd('000001.SH', 'close', '2016-1-1', '2016-6-21')
szzz1 = np.array(szzz['close'])
diff, dea, macd = talib.MACD(szzz1)