import numpy as np
import matplotlib.pyplot as plt
from WindPy import w
w.start()

plt.axis([0, 100, 97.2, 97.22])
plt.ion()
rtPrice = w.wsq('USDX.FX','rt_last')

for i in range(100):
    plt.scatter(i, rtPrice.Data[0][0])
    plt.pause(1)


