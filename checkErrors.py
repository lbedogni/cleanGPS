#!/usr/bin/python3
# Usage python3 thisfile our_calibrated_file their_calibrated_file ground_truth_file our_error_file their_error_file

import sys
from datetime import datetime
import vincenty

ourFile = open(sys.argv[1], 'r')
theirFile = open(sys.argv[2], 'r')
groundTruthFile = open(sys.argv[3], 'r')

first = True

ourLastLine = ''
groundLastLine = ''
theirLastLine = ''

ourMissing = 0
theirMissing = 0

DELTA_TIME = 1



ourErrorFile = open(sys.argv[4],'w')
theirErrorFile = open(sys.argv[5],'w')

DEBUG_LOOPS = 21

ourLastLine = ourFile.readline().strip()
theirFile.readline()
theirLastLine = theirFile.readline().strip()

ourTime = int(int(ourLastLine.split()[1]))
theirTime = int(int(theirLastLine.split(' ')[1])) 

for line in groundTruthFile.readlines():
    #print(" ******************************** Another line form ground truth ******************************** ")
    if first:
        first = False
        continue
    ll = line.strip().split(',')
    groundTime = int(datetime.strptime(ll[1], '%Y-%m-%d %H:%M:%S').timestamp())
    #print(groundTime)
    groundCoord = (float(ll[3]), float(ll[2]))

#    print(theirTime)
    if theirTime - groundTime >= DELTA_TIME:
        # Too in advance, don't read another line
#        print("Don't advance, groundTime is " + str(groundTime))
        pass
    else:
        # We need to read another line

        # We need to read another line
        # print("Comparing: " + str(groundTime) + " - " + str(line.strip()) + " - " + str(ourLastLine))
        theirCoord = (float(theirLastLine.split(' ')[3]), float(theirLastLine.split(' ')[2]))

        distance = vincenty.vincenty(theirCoord, groundCoord) * 1000
        theirErrorFile.write(str(distance) + " " + str(theirTime) + " " + str(theirCoord) + " " + str(groundTime) + " " + str(
            groundCoord) + '\n')
        # print("Our Distance = " + str(distance))

#        print("Reading from their file")
        newline = theirFile.readline().strip()
        if newline != "":
#            print("**" + newline + "**")
            theirLastLine = newline
        while True and newline != "":
#            print("--" + theirLastLine + "--")
#            print("--" + newline + "--")
            newTime = int(int(theirLastLine.split(' ')[1]))
#            print(str(newTime) + " *** " + str(theirTime))
            if newTime != theirTime:
                break
            theirLastLine = theirFile.readline().strip()
        theirTime = int(int(theirLastLine.split(' ')[1]))
#        print(theirLastLine)

    if ourTime - groundTime > DELTA_TIME:
        # Too in advance, don't read another line
        pass
    else:
        # We need to read another line
        #print("Comparing: " + str(groundTime) + " - " + str(line.strip()) + " - " + str(ourLastLine))
        ourCoord = (float(ourLastLine.split()[3]), float(ourLastLine.split()[2]))

        distance = vincenty.vincenty(ourCoord, groundCoord) * 1000
        ourErrorFile.write(str(distance) + " " + str(ourTime) + " " + str(ourCoord) + " " + str(groundTime) + " " + str(groundCoord) + '\n')
        #print("Our Distance = " + str(distance))

        #print("Reading from our file")
        newline = ourFile.readline().strip()
        if newline != "":
            ourLastLine = newline
        while True and newline != "":
            newTime = int(int(ourLastLine.split()[1]))
            #print(str(newTime) + " *** " + str(ourTime))
            if newTime != ourTime:
                break
            ourLastLine = ourFile.readline().strip()
        ourTime = int(int(ourLastLine.split()[1]))
        #print(ourLastLine)

    if theirTime - groundTime > DELTA_TIME:
        theirMissing += 1
        #print("They missed: total = " + str(theirMissing))

    if ourTime - groundTime > DELTA_TIME:
        ourMissing += 1
        #print("We missed: total = " + str(ourMissing))

''''        DEBUG_LOOPS -= 1
    else:
        sys.exit()
'''
