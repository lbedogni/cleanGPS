import numpy as np
import matplotlib.pyplot as plt

#dataB = np.loadtxt('beijing_speeds.csv')
#dataS = np.loadtxt('sf_speeds.csv')
#dataShan = np.loadtxt('shanghai_speeds.csv')
dataTor = np.loadtxt('torino_speeds.csv')
dataBar = np.loadtxt('bari_speeds.csv')
dataMil = np.loadtxt('milano_speeds.csv')
dataNap = np.loadtxt('napoli_speeds.csv')
dataRom = np.loadtxt('roma_speeds.csv')
#dataNYC = np.loadtxt('nyc_speeds.csv')

#sorted_dataB = np.sort(dataB)
#sorted_dataS = np.sort(dataS)
#sorted_dataShan = np.sort(dataShan)
sorted_dataTor = np.sort(dataTor)
sorted_dataBar = np.sort(dataBar)
sorted_dataMil = np.sort(dataMil)
sorted_dataNap = np.sort(dataNap)
sorted_dataRom = np.sort(dataRom)
#sorted_dataNYC = np.sort(dataNYC)

#yvals_B = np.arange(len(sorted_dataB))/float(len(sorted_dataB))
#yvals_S = np.arange(len(sorted_dataS))/float(len(sorted_dataS))
#yvals_Shan = np.arange(len(sorted_dataShan))/float(len(sorted_dataShan))
yvals_Tor = np.arange(len(sorted_dataTor))/float(len(sorted_dataTor))
yvals_Bar = np.arange(len(sorted_dataBar))/float(len(sorted_dataBar))
yvals_Mil = np.arange(len(sorted_dataMil))/float(len(sorted_dataMil))
yvals_Nap = np.arange(len(sorted_dataNap))/float(len(sorted_dataNap))
yvals_Rom = np.arange(len(sorted_dataRom))/float(len(sorted_dataRom))
#yvals_NYC = np.arange(len(sorted_dataNYC))/float(len(sorted_dataNYC))

#BE = plt.plot(sorted_dataB,yvals_B)
#SF = plt.plot(sorted_dataS,yvals_S)
#SH = plt.plot(sorted_dataShan,yvals_Shan)
TO = plt.plot(sorted_dataTor,yvals_Tor)
BA = plt.plot(sorted_dataBar,yvals_Bar)
MI = plt.plot(sorted_dataMil,yvals_Mil)
NA = plt.plot(sorted_dataNap,yvals_Nap)
RO = plt.plot(sorted_dataRom,yvals_Rom)
#NY = plt.plot(sorted_dataNYC,yvals_NYC)

plt.axis([0, 50, 0, 1])

#plt.legend(('Beijing', 'San Francisco', 'Shanghai', 'Torino', 'Bari', 'Milano', 'Napoli', 'Roma', 'NYC'), loc='upper right', shadow=True)
#plt.legend(('Torino', 'Bari', 'Milano', 'Napoli', 'Roma', 'NYC'), loc='upper right', shadow=True)
plt.legend(('Torino', 'Bari', 'Milano', 'Napoli', 'Roma'), loc='upper right', shadow=True)

plt.show()
