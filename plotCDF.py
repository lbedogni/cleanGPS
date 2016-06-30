#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt('outfile.csv')

sorted_data = np.sort(data)

yvals=np.arange(len(sorted_data))/float(len(sorted_data))
print(yvals)

plt.plot(sorted_data,yvals)

plt.show()
