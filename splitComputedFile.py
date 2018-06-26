#!/usr/bin/python3
# Usage thisfile.py interp_file file delta_time_in_sec time_position divide_for_1000
import sys,os,time,math
COUNTER = int(sys.argv[1].split('_')[2])
ALREADY_STARTED = False
PREFIX = sys.argv[6]

divide_for_1000 = sys.argv[5]

START = -1
END = -1
ff = open(sys.argv[1],'r')
for line in ff.readlines():
    if START == -1:
        START = int(line.split()[1])
    END = int(line.split()[1])
ff.close()

if divide_for_1000 == "True":
    divide_for_1000 = True
else:
    divide_for_1000 = False

basenamefile = os.path.basename(sys.argv[2])
fw = open("tmp/" + PREFIX + "_" + basenamefile + "_" + str(COUNTER), 'w+')

ff = open(sys.argv[2])
for line in ff.readlines():
    if "time" in line:
        continue
    ll = line.split()
#    if PREFIX == "their":
#        # Convert time
#        ll[int(sys.argv[4])] = math.ceil(time.mktime(time.strptime(ll[int(sys.argv[4])], "%Y-%m-%d %H:%M:%S")))
    if divide_for_1000:
        time = math.ceil(int(ll[int(sys.argv[4])])/1000) + int(sys.argv[3])
    else:
        time = int(ll[int(sys.argv[4])]) + int(sys.argv[3])
    if time >= START or ALREADY_STARTED:
        # We found the start or we have already started, so create the file or continue
        ALREADY_STARTED = True
        if time > END:
            break
        ll[int(sys.argv[4])] = str(time)
        fw.write(" ".join(ll) + "\n")

ff.close()
fw.close()
