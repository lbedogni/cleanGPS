#!/usr/bin/python3
import sys
import os

for line in open(sys.argv[1],'r'):
    ll = line.split(",")
#    print(line)
    fw = open(sys.argv[2] + "/NYC_" + str(ll[0].strip()) + ".csv","a")
    fw.write(line)
    fw.close()

#os.remove(sys.argv[1])
