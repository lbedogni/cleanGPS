#!/usr/bin/python3
# Usage thisfile.py file delta_time_in_sec time_position
import sys,os
COUNTER = 0

ff = open(sys.argv[1],'r')
BASEDIR = sys.argv[2]

basenamefile = os.path.basename(sys.argv[1])
print(basenamefile)

try:
    os.stat("tmp")
except:
    os.mkdir("tmp") 

for line in ff.readlines():
    ll = line.split()
    ll[int(sys.argv[3])] = int(ll[int(sys.argv[3])]) + int(sys.argv[2])
    ll[int(sys.argv[3])] = str(ll[int(sys.argv[3])])
    line = " ".join(ll)

    if "#INTERPOLATE" in line:
        # We need to write and continue
        fw = open("tmp/interp_" + basenamefile + "_" + str(COUNTER),'a+')
        fw.write(line + "\n")
        fw.close()
    else:
        # We are at a crucial point, so we have to change file
        fw = open("tmp/interp_" + basenamefile + "_" + str(COUNTER),'a+')
        fw.write(line + "\n")
        fw.close()
        if "#" in line:
            COUNTER += 1
            fw = open("tmp/interp_" + basenamefile + "_" + str(COUNTER),'a+')
            fw.write(line + "\n")
            fw.close()

#os.remove("tmp/" + basenamefile + "_" + str(COUNTER))

ff.close()
