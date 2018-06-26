#!/usr/bin/python3
import sys,time,math
from vincenty import vincenty

num = sys.argv[1].split("_")[2]
progressive = sys.argv[1].split("_")[3]
directory = sys.argv[1].split("/")[0]
print(sys.argv[1])

f_interp = open(sys.argv[1],'r')
f_our = open(directory + "/our_" + num + "_" + num + "_" + progressive,'r')

START = -1
END = -1
for line in f_interp.readlines():
    if START == -1:
        START = line
    END = line
f_interp.close()
f_interp = open(sys.argv[1],'r')

START_POINT= (float(START.split()[3]),float(START.split()[2]))
END_POINT= (float(END.split()[3]),float(END.split()[2]))
total_distance = vincenty(START_POINT, END_POINT) * 1000

for line_interp in f_interp.readlines():
    line_interp = line_interp.strip()
    time_interp = line_interp.strip().split()[1]
    # Now find the row in GT
    found = False
    f_their = open(directory + "/their_" + num + "_" + progressive,'r')
    f_gt = open("COLOGNE/sampling_data/cologne_gap_1/" + num, 'r')
    while not found:
        line_gt = f_gt.readline().strip()
        if "time" in line_gt:
            continue # First line
        try:
            time_gt = line_gt.split(",")[1]
            t_gt = math.ceil(time.mktime(time.strptime(time_gt, "%Y-%m-%d %H:%M:%S")))
            time_gt = t_gt + 7200 # Timezone Conversion
            #print(str(time_gt) + " - " + str(time_interp))
            if int(time_gt) == int(time_interp):
                found = True # We found the same time, now compute the error
            if int(time_gt) > int(time_interp):
                # We missed it
                break
            #else:
            #    sys.exit()
        except:
            continue
    print("OK GT")

    found = False
    while not found:
        line_our = f_our.readline().strip()
        time_our = line_our.split()[1]
        if int(time_our) == int(time_interp):
            found = True # We found the same time, now compute the error
    print("OK OU")

    found = False
    while not found:
        line_their = f_their.readline().strip()
        try:
            time_their = line_their.split(" ")[1]
        except:
            break
        if "time" in line_their:
            continue # First line
        if time_their == time_interp:
            found = True # We found the same time, now compute the error
    print("OK TH")

    # Here we should have everything right
    print("**** " + str(sys.argv[1]) + " ****")
    print("GT - " + line_gt)
    print("LI - " + line_interp)
    print("TH - " + line_their)
    print("OU - " + line_our)
    f_their.close()

    # Now we need to compute the errors
    gt_point = (float(line_gt.split(",")[3]),float(line_gt.split(",")[2]))
    li_point = (float(line_interp.split()[3]),float(line_interp.split()[2]))

    th_error = "NA"
    if line_their.strip() != "":
        th_point = (float(line_their.split()[3]),float(line_their.split()[2]))
        th_error = vincenty(gt_point, th_point) * 1000
    ou_point = (float(line_our.split()[3]),float(line_our.split()[2]))

    li_error = vincenty(gt_point, li_point) * 1000
    ou_error = vincenty(gt_point, ou_point) * 1000

    fw = open("total_errors.csv","a+")
    fw.write(str(total_distance) + " " + str(li_error) + " " + str(th_error) + " " + str(ou_error) + "\n")
    fw.close()
    f_gt.close()

f_interp.close()

f_our.close()
