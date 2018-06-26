#!/usr/bin/python3
import sys
import os

ff = open(sys.argv[1],'r')
bbox = sys.argv[2]
atleastone = False

bboxlat1 = float(bbox.split(',')[0])
bboxlng1 = float(bbox.split(',')[1])
bboxlat2 = float(bbox.split(',')[2])
bboxlng2 = float(bbox.split(',')[3])

for line in ff.readlines():
    ll = line.split(';')
    lat = float(ll[2])
    lng = float(ll[3])
    if lat > bboxlat1 and lat < bboxlat2 and lng > bboxlng1 and lng < bboxlng2:
        atleastone = True

if not atleastone:
    print("to remove")
    os.remove(sys.argv[1])
else:
    print("to keep")

