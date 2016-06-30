#!/usr/bin/python
import sys
import datetime
import time
from geopy.distance import vincenty

ff = open(sys.argv[1],'r')
timebase = 0
pointbase = (0,0)
fw = open(sys.argv[2] + '_speeds_high.csv','a')
fw2 = open(sys.argv[2] + '_speeds.csv','a')
for line in ff.readlines():
    ll = line.split(' ')
    if line.startswith("#") or line.startswith(" "):
        continue
    t = float(ll[1])
    lon = float(ll[2])
    lat = float(ll[3])

    if timebase > 0:
        delta = t - timebase
        dist = vincenty(pointbase, (lat,lon)).miles
        dist *= 1609
        if delta == 0:
            delta = 1
        speed = dist / delta
        if speed > 50:
            fw.write(str(sys.argv[1]) + " " + str(lat) + " " + str(lon) + " " + str(pointbase[0]) + " " + str(pointbase[1]) + "\n")
        fw2.write(str(speed) + "\n")

        timebase = t
        pointbase = (lat, lon)
    else:
        timebase = t
        pointbase = (lat, lon)
fw.close()
fw2.close()
