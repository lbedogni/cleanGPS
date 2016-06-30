#!/usr/bin/python3
import sys

ff = open(sys.argv[1],'r')
allSpeeds = {}

total = 0

for line in ff.readlines():
    l = float(line)
    if l in allSpeeds:
        allSpeeds[l] += 1
    else:
        allSpeeds[l] = 1
    total += 1.0

print("Finished reading elements")

counter = 0
increment = 0.1
fw = open(sys.argv[1] + ".final", 'w+')
for key in sorted(allSpeeds):
    if float(key) > increment:
        fw.write(str(key) + " " + str(counter/total) + "\n")
        increment += 0.1
    counter = counter + allSpeeds[key]


fw.close()
