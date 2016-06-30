#!/usr/bin/python3
import sys

ff = open(sys.argv[1],'r')
timebase = 0
fw = open('outfile.csv','a')
for line in ff.readlines():
    ll = line.split()
    time = int(ll[3])
    if timebase > 0:
        fw.write(str(time - timebase) + "\n")
        timebase = time
    else:
        timebase = time
fw.close()
