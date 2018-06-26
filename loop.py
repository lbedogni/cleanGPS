#!/usr/bin/python3
from os import listdir
import os
from os.path import isfile, join
import sys

for ff in listdir(sys.argv[1]):
    ss = "./removeOutsideBBox.py " + str(sys.argv[1]) + "/" + str(ff) + " " + str(sys.argv[2])
    os.system(ss)
    #print(ss)
