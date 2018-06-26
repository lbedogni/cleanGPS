#!/usr/bin/python3
# Usage: ./toolchain.py WORKINGDIR Trips/Points(Boolean) latmin lonmin latmax lonmax daystart dayend city
import sys
import os
import time
import urllib.request
import xml.etree.ElementTree as ET
import math
import shutil
import math

from geopy.distance import vincenty

print("In toolchain")

WORKINGDIR = sys.argv[1]
TRIPS = sys.argv[2]
LATMIN = float(sys.argv[3])
LONMIN = float(sys.argv[4])
LATMAX = float(sys.argv[5])
LONMAX = float(sys.argv[6])
DAYSTART = time.mktime(time.strptime(sys.argv[7], "%Y%m%d"))
DAYEND = time.mktime(time.strptime(sys.argv[8], "%Y%m%d"))
PREFIX = sys.argv[9]
OUTPUTDIR = PREFIX + "_tmp_" + sys.argv[7]
FINALDIR = PREFIX + "_out_" + sys.argv[8]
city = sys.argv[9]


TIME_ZERO = 0
TIME_NEGATIVE = 0

FOUNDLATMIN = 200
FOUNDLATMAX = -200
FOUNDLONMIN = 200
FOUNDLONMAX = -200
if os.path.isfile("distances" + str(city) + ".dat"):
    ff = open('distances' + str(city) + '.dat','r')
    ll = ff.readline()
    [FOUNDLATMIN,FOUNDLATMAX,FOUNDLONMIN,FOUNDLONMAX] = ll.split(" ")
    FOUNDLATMIN = float(FOUNDLATMIN)
    FOUNDLATMAX = float(FOUNDLATMAX)
    FOUNDLONMIN = float(FOUNDLONMIN)
    FOUNDLONMAX = float(FOUNDLONMAX)
    ff.close()

TIMETHRESHOLD = 1
SPEEDTHRESHOLD = 200

S_BASE = "http://router.project-osrm.org/route/v1/driving/"
S_BASE_NEAREST = "http://router.project-osrm.org/nearest/v1/driving/"
S_BASE = "http://localhost:5000/route/v1/driving/"
S_BASE_NEAREST = "http://localhost:5000/nearest/v1/driving/"
S_END = "&output=gpx"

print("All ok")

def cleanFiles():
    if os.path.isdir(OUTPUTDIR):
        shutil.rmtree(OUTPUTDIR)
    if os.path.isdir(FINALDIR):
        shutil.rmtree(FINALDIR)

def createDirs():
    if not os.path.isdir(OUTPUTDIR):
        os.makedirs(OUTPUTDIR)
    if not os.path.isdir(FINALDIR):
        os.makedirs(FINALDIR)

def checkFileTooBig(file):
    num_lines = sum(1 for line in open(WORKINGDIR + "/" + file))
    print(num_lines)    

def measure(lat1, lon1, lat2, lon2):
    R = 6378.137 # Radius of earth in KM
    dLat = (lat2 - lat1) * math.pi / 180;
    dLon = (lon2 - lon1) * math.pi / 180;
    a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(lat1 * math.pi / 180) * math.cos(lat2 * math.pi / 180) * math.sin(dLon/2) * math.sin(dLon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c
    return d * 1000

def composeString(lats,lons,late,lone,gpx):
    #if (gpx):
    #    return S_BASE + "loc=" + str(lats) + "," + str(lons) + "&loc=" + str(late).strip() + "," + str(lone).strip() + S_END
    #return S_BASE + "loc=" + str(lats) + "," + str(lons) + "&loc=" + str(late).strip() + "," + str(lone).strip() + "&output=json&compression=false"
    if (gpx):
        return S_BASE + "loc=" + str(lats) + "," + str(lons) + "&loc=" + str(late).strip() + "," + str(lone).strip() + S_END
    return S_BASE + str(lons).strip() + "," + str(lats).strip() + ";" + str(lone).strip() + "," + str(late).strip() + "?geometries=geojson"
    
def prints(file, one,two,three,four):
#    print(file)
    fw = open(file, "a+")
    fw.write(str(one) + " " + str(math.floor(float(two))) + " " + str(three) + " " + str(four) + "\n")
    fw.close()

def queryServiceNearest(lat, lon):
    stringToGet = S_BASE_NEAREST + str(lon) + "," + str(lat) + "?number=1"
    req = urllib.request.Request(
            stringToGet, 
            data=None, 
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
                }
            )
    toRepeat = True
    xmlstring = ""
    while toRepeat:
        try:
#            print("Querying service")
            print(stringToGet)
            xmlstring = urllib.request.urlopen(stringToGet, timeout = 2).read().decode("utf-8")
            #xmlstring = urllib.request.urlopen(req).read()
            toRepeat = False
        except urllib.error.HTTPError as e:
            # Probably error 400
#            toRepeat = False
#            ff = open('exception_errors.log','a+')
#            ff.write(str(e.code) + " " + str(e.reason) + "\n")
#            ff.close()
#            return False
            print("ERROR in the nearest query")
            print(e.code)
            print(e.reason)
            print(e)
            time.sleep(10)
        except:
            print("Connection problem. Pausing and repeating.")
            print(stringToGet)
#            print(xmlstring)
            time.sleep(5)
#    print("DONE")
#    print(xmlstring)
    return xmlstring

def queryService(lat1, lon1, lat2, lon2,gpx):
    print("We are querying the service to go from " + str(lat1) + "," + str(lon1) + " to " + str(lat2) + "," + str(lon2))
    stringToGet = composeString(lat1,lon1,lat2,lon2,gpx)
    print(stringToGet)
    req = urllib.request.Request(
            stringToGet, 
            data=None, 
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
                }
            )
    toRepeat = True
    xmlstring = ""
    while toRepeat:
        try:
#            print("Querying now")
            print(stringToGet)
            xmlstring = urllib.request.urlopen(stringToGet, timeout = 5).read().decode("utf-8")
#            print(xmlstring)
#            print("******")
            #xmlstring = urllib.request.urlopen(req).read()
            toRepeat = False
        except urllib.error.HTTPError as e:
            # Probably error 400
#            toRepeat = False
#            print("HTTP Error")
#            print(str(e) + " - " + str(e.code) + " - " + str(e.reason))
#            ff = open('exception_errors.log','a+')
#            ff.write(str(e.code) + " " + str(e.reason) + "\n")
#            ff.close()
#            return False
#            time.sleep(5)
            lat1 = float(lat1) + 0.001
            lon1 = float(lon1) + 0.001
            lat2 = float(lat2) + 0.001
            lon2 = float(lon2) + 0.001
            stringToGet = composeString(float(lat1),float(lon1),float(lat2),float(lon2),gpx)
            print("We have changed the coordinates to: " + str(stringToGet))
            req = urllib.request.Request(
                    stringToGet, 
                    data=None, 
                    headers={
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
                        }
                    )
        except:
            print("Connection problem. Pausing and repeating.")
            print(stringToGet)
#            print(xmlstring)
            time.sleep(5)
#    print("DONE")
    print(xmlstring)
    if gpx:
        return ET.fromstring(xmlstring)
    return xmlstring

def getTripsNYC(line):
    #print(line)
    ll = line.split(",")
    ttstart = math.ceil(time.mktime(time.strptime(ll[5], "%Y-%m-%d %H:%M:%S")))
    ttend = math.ceil(time.mktime(time.strptime(ll[6], "%Y-%m-%d %H:%M:%S")))
    lonstart = ll[10].strip()
    latstart = ll[11].strip()
    lonend = ll[12].strip()
    latend = ll[13].strip()
    if lonstart.strip() == "" or lonend.strip() == "" or latstart.strip() == "" or latend.strip() == "":
        return
    else:
        return ll[0],ttstart,ttend,lonstart,latstart,lonend,latend
    
def getTripsRome(line):
#    print(line)
    ll = line.split(",")
    ID = ll[0].strip()
    tt = math.ceil(float(ll[1].strip()))
    lon = ll[2].strip()
    lat = ll[3].strip()
    if lon.strip() == "" or lat.strip() == "":
        return
    else:
        return ID,tt,lon,lat

def getTripsCologne(line):
#    print(line)
    ll = line.split(",")
    ID = ll[0].strip()
    #tt = math.ceil(float(ll[1].strip()))
    from datetime import datetime
    #tt = int(datetime.datetime.fromtimestamp(int(tt)).strftime("%Y-%m-%d $H:$M:$S"))
    tt = datetime.strptime(ll[1].strip(), '%Y-%m-%d %H:%M:%S').timestamp()
    print(tt)
    lon = ll[2].strip()
    lat = ll[3].strip()
    if lon.strip() == "" or lat.strip() == "":
        return
    else:
        return ID,tt,lon,lat
    
def getTripsShenzen(line):
#    print(line)
    ll = line.split(",")
    ID = ll[0].strip()
    #tt = math.ceil(float(ll[1].strip()))
    from datetime import datetime
    #tt = int(datetime.datetime.fromtimestamp(int(tt)).strftime("%Y-%m-%d $H:$M:$S"))
    tt = datetime.strptime(ll[1].strip(), '%Y-%m-%d %H:%M:%S').timestamp()
    print(tt)
    lon = ll[2].strip()
    if (' ' in ll[3].strip()):
        lat = ll[3].strip().split(' ')[1]
    else:
        lat = ll[3].strip()
    if lon.strip() == "" or lat.strip() == "":
        return
    else:
        return ID,tt,lon,lat
    
def getTripsShanghai(line):
#    print(line)
    ll = line.split(",")
    ID = ll[0].strip()
    #tt = math.ceil(float(ll[1].strip()))
    from datetime import datetime
    #tt = int(datetime.datetime.fromtimestamp(int(tt)).strftime("%Y-%m-%d $H:$M:$S"))
    tt = datetime.strptime(ll[1].strip(), '%Y-%m-%d %H:%M:%S').timestamp()
    print(tt)
    lon = ll[2].strip()
    lat = ll[3].strip()
    if lon.strip() == "" or lat.strip() == "":
        return
    else:
        return ID,tt,lon,lat
    
def getTripsSF(line):
    #print(line)
    ll = line.split(" ")
    tt = math.ceil(float(ll[3].strip()))
    #import datetime
    #tt = int(datetime.datetime.fromtimestamp(int(tt)).strftime("%Y%m%d"))
    #tt*= 1000
    lat = ll[0].strip()
    lon = ll[1].strip()

def getTripsBeijing(line):
#    print(line)
    ll = line.split(",")
    ID = ll[0].strip()
    #tt = math.ceil(float(ll[1].strip()))
    from datetime import datetime
    #tt = int(datetime.datetime.fromtimestamp(int(tt)).strftime("%Y-%m-%d $H:$M:$S"))
    tt = datetime.strptime(ll[1].strip(), '%Y-%m-%d %H:%M:%S').timestamp()
#    print(tt)
    lon = ll[2].strip()
    lat = ll[3].strip()
    if lon.strip() == "" or lat.strip() == "":
        return
    else:
        return ID,tt,lon,lat
    
def getTripsSF(line):
    #print(line)
    ll = line.split(" ")
    tt = math.ceil(float(ll[3].strip()))
    #import datetime
    #tt = int(datetime.datetime.fromtimestamp(int(tt)).strftime("%Y%m%d"))
    #tt*= 1000
    lat = ll[0].strip()
    lon = ll[1].strip()
    if lon.strip() == "" or lat.strip() == "":
        return
    else:
        return tt,lon,lat

def getTripsDandelion(line):
#    print(line)
    ll = line.split(";")
    ID = ll[0].strip()
    #tt = math.ceil(float(ll[3].strip()))
    from datetime import datetime
    #tt = int(datetime.datetime.fromtimestamp(int(tt)).strftime("%Y-%m-%d $H:$M:$S"))
    tt = int(datetime.strptime(ll[1].strip(), '%Y-%m-%d %H:%M:%S').timestamp())
    #import datetime
    #tt = int(datetime.datetime.fromtimestamp(int(tt)).strftime("%Y%m%d"))
    #tt*= 1000
    lat = ll[2].strip()
    lon = ll[3].strip()
    if lon.strip() == "" or lat.strip() == "":
        return
    else:
        return ID,tt,lon,lat

def getPointsFromTrips(file):
    #print("getPointsFromTrip()")
    global TIME_NEGATIVE
    global TIME_ZERO
    import os.path
#    if os.path.isfile(OUTPUTDIR + "/" + file):
#        return
    fread = open(WORKINGDIR + "/" + file, "r")
    #print("Open file. Done.")
    counter = 0
    ttstart = -1
    for line in fread.readlines():
        if city == "nyc":
            # NYC
            # TEMPLATE: ""medallion, hack_license, vendor_id, rate_code, store_and_fwd_flag, pickup_datetime, dropoff_datetime, passenger_count, trip_time_in_secs, trip_distance, pickup_longitude, pickup_latitude, dropoff_longitude, dropoff_latitude
            if counter == 0:
                counter += 1
                continue
            ll_tmp = line.split(',')
            if ll_tmp[10].strip() != '' and ll_tmp[11].strip() != '' and ll_tmp[12].strip() != '' and ll_tmp[13].strip() != '':
                [ID,ttstart,ttend,lonstart,latstart,lonend,latend] = getTripsNYC(line)
            else:
                continue
        elif city == "shanghai":
            if ttstart == -1:
                #First round
                [ID,ttstart,lonstart,latstart] = getTripsShanghai(line)
                continue
            else:
                #Second or more round
                [ID,ttend,lonend,latend] = getTripsShanghai(line)
        elif city == "cologne":
            if ttstart == -1:
                #First round
                [ID,ttstart,lonstart,latstart] = getTripsCologne(line)
                continue
            else:
                #Second or more round
                [ID,ttend,lonend,latend] = getTripsCologne(line)
        elif city == "shenzen":
            if ttstart == -1:
                #First round
                try:
                    [ID,ttstart,lonstart,latstart] = getTripsShenzen(line)
                except:
                    pass
                continue
            else:
                #Second or more round
                try:
                    [ID,ttend,lonend,latend] = getTripsShenzen(line)
                except:
                    print("Problems in reading, I continue")
                    continue
        elif city == "beijing":
            if ttstart == -1:
                #First round
                [ID,ttstart,lonstart,latstart] = getTripsBeijing(line)
                continue
            else:
                #Second or more round
                [ID,ttend,lonend,latend] = getTripsBeijing(line)
        elif city == "sf":
            # San Francisco
            if ttstart == -1:
                # First round
                [ttstart,lonstart,latstart] = getTripsSF(line)
                continue
            else:
                #Second or more round
                [ttend,lonend,latend] = getTripsSF(line)
                ID = file
        elif city in ["turin","palermo","milan","rome","bari"]:
            # Dandelion
            if ttstart == -1:
                # First round
                [ID,ttstart,lonstart,latstart] = getTripsDandelion(line)
                continue
            else:
                #Second or more round
                [ID,ttend,lonend,latend] = getTripsDandelion(line)

        difftime = ttend - ttstart
        if difftime > 3600:
            #print("Difftime is " + str(difftime) + ". Different trip, treat it as new one")
            #print("****")
            #print("Print - " + str(line))
            #print("****")
            ttstart = ttend
            lonstart = lonend
            latstart = latend
            continue
        
        if difftime == 0 and (city in ["rome","sf","turin","palermo","milan","bari","cologne"]):
            prints(OUTPUTDIR + "/" + str(file) + "_" + str(ID) + ".csv", str(ID), str(ttend), lonend, latend)
        elif difftime == 0:
            TIME_ZERO += 1
            open('stats_' + str(sys.argv[7]) + '.data','w+').write("TIME_ZERO = " + str(TIME_ZERO) + ", TIME_LESS_ZERO = " + str(TIME_NEGATIVE) + "\n")
            open('errors_' + str(sys.argv[7]) + '.data','a+').write(line)
        elif difftime > 0:
            if checkValidPoint(latstart, lonstart) and checkValidPoint(latend, lonend) and (checkValidTime(ttstart) and checkValidTime(ttend)):
     #           prints(OUTPUTDIR + "/" + str(file) + "_" + str(ID) + ".csv", str(ID), str(ttstart), latstart, lonstart)
                print("I AM QUERYING THE SERVICE HERE")
                tree = queryService(latstart, lonstart, latend, lonend, False)
                if not tree or not parseQueryResponse(OUTPUTDIR + "/" + str(file) + "_" + str(ID) + ".csv", tree, str(ID), difftime,  ttstart, line, False):
                    if not tree:
                        prints(OUTPUTDIR + "/" + str(file) + "_" + str(ID) + ".csv", str(ID), str(ttstart), str(lonstart), str(latstart) + " # treeError - " + str(line))
                        prints(OUTPUTDIR + "/" + str(file) + "_" + str(ID) + ".csv", str(ID), str(ttend), str(lonend), str(latend) + " # treeError - " + str(line))
                    else:
                        prints(OUTPUTDIR + "/" + str(file) + "_" + str(ID) + ".csv", str(ID), str(ttstart), str(lonstart), str(latstart) + " # from parseQueryResponse - " + str(line))
                        prints(OUTPUTDIR + "/" + str(file) + "_" + str(ID) + ".csv", str(ID), str(ttend), str(lonend), str(latend) + " # from parseQueryResponse - " + str(line))
        else:
            print("HERE")
            TIME_NEGATIVE += 1
            open('stats_' + str(sys.argv[7]) + '.data','a+').write("TIME_ZERO = " + str(TIME_ZERO) + ", TIME_LESS_ZERO = " + str(TIME_NEGATIVE) + "\n")
            open('errors_' + str(sys.argv[7]) + '.data','a+').write(line)
#            print("difftime <= 0:" + str(line))

        allCities = ["rome","sf","turin","bari","palermo","milan","beijing","shanghai","cologne","shenzen"]
        if city in allCities:
            ttstart = ttend
            lonstart = lonend
            latstart = latend

        fread.close()

def checkValidTime(t):
    t = float(t)
    if t > DAYSTART and t < DAYEND:
        return True
#    print("NOT Valid Time")
#    print(t)
#    print(DAYSTART)
#    print(DAYEND)
    return False

def checkValidPoint(lat, lon):
    lat = float(str(lat).strip())
    lon = float(str(lon).strip())
#    print(LATMIN)
    if lat > LATMIN and lat < LATMAX and lon > LONMIN and lon < LONMAX:
        return True
    else:
#        print("NOT Valid Point")
#        print(str(lat) + "," + str(LATMIN) +"-"+str(LATMAX))
#        print(str(lon) + "," + str(LONMIN) +"-"+str(LONMAX))
        return False
#    changed = False
#    global FOUNDLATMAX
#    global FOUNDLATMIN
#    global FOUNDLONMIN
#    global FOUNDLONMAX
#    if lat < FOUNDLATMIN:
#        FOUNDLATMIN = lat
#        changed = True
#    if lat > FOUNDLATMAX:
#        FOUNDLATMAX = lat
#        changed = True
#    if lon < FOUNDLONMIN:
#        FOUNDLONMIN = lon
#        changed = True
#    if lon > FOUNDLONMAX:
#        FOUNDLONMAX = lon
#        changed = True
#    if changed:
        #distances = open('distances.dat','w+')
        #distances.write(str(FOUNDLATMIN) + ' ' + str(FOUNDLATMAX) + " " + str(FOUNDLONMIN) + " " + str(FOUNDLONMAX) + "\n")
        #distances.close()
#    return True

#    if lat > LATMIN and lat < LATMAX and lon > LONMIN and lon < LONMAX:
#        return True
#    print("NOT Valid Location")
#    return False
    
def cleanTrace(file):
    lasttime = 0
    lastlat = -1
    lastlng = -1    
    deltasec = 1
    print("BEGIN")
    ff = open(file, 'r')
    lines = [line for line in ff if line.strip()]
    lines.sort()
    ff.close()
    ff = open(file,'w+')
    ff.writelines(lines)
    ff.close()
    ff = open(file, 'r')
    print(sys.argv[7] + " - Cleaning file " + file)

    for line in ff.readlines():
        ll = line.split(",")
        thistime = 0
        try:
            thistime = time.mktime(time.strptime(ll[1], "%Y-%m-%d %H:%M:%S"))
            ll[1] = thistime
        except:
            thistime = float(ll[1])
            #print("Assuming time in seconds on file: " + file + ", line: " + str(line).strip())
        thistime = int(thistime)
        difftime = int(thistime - lasttime)
#        if not checkValidPoint(float(ll[2]), float(ll[3])):
#            print("Point not valid")
#            continue

        if lastlng == -1 or difftime > 3600:
           lasttime = thistime
           lastlng = ll[2]
           lastlat = ll[3]
#           print("****", ll[0],lasttime,lastlat,str(lastlng).strip())
           prints(FINALDIR + "/" + os.path.basename(file), ll[0],lasttime,str(lastlng),str(lastlat).strip())
            
        elif difftime > TIMETHRESHOLD:
            # We need to interpolate
            # In difftime seconds we need to go form lastlat,lastlng to ll[2],ll[3], every deltasec
            dist = measure(float(ll[2]),float(ll[3]),float(lastlng),float(lastlat))
            difftime = max(1,difftime)
            speed = dist/difftime
            numtime = int(math.ceil(difftime / deltasec))
            difflng = (float(ll[2]) - float(lastlng))/numtime
            difflat = (float(ll[3]) - float(lastlat))/numtime
            thislat = float(lastlat)
            thislng = float(lastlng)
            increment = difftime / numtime
            if increment != 1:
                print("Error! increment is " + str(increment) + ". diffitime = " + str(difftime) + ", numtime = " + str(numtime))
            for i in range(1,numtime):
                thislat = float(thislat) + float(difflat)
                thislng = float(thislng) + float(difflng)
                prints(FINALDIR + "/" + os.path.basename(file), ll[0],lasttime + i * increment,str(thislng),str(thislat) + " #INTERPOLATE POINT")
            prints(FINALDIR + "/" + os.path.basename(file), ll[0],ll[1],ll[2],ll[3].strip() + " #LAST INTERPOLATE POINT")
            lasttime = float(ll[1])
            lastlng = ll[2]
            lastlat = ll[3]

        else:
            print("SHOULD NEVER HAPPEN")
            sys.exit()
            dist = measure(float(ll[2]),float(ll[3]),float(lastlng),float(lastlat))
            difftime = max(1,difftime)
            speed = dist/difftime
            if speed < 200:
                prints(FINALDIR + "/" + os.path.basename(file), ll[0],thistime,ll[2],ll[3].strip() + " #NO INTERPOLATE")
    ff.close()
    
def getMeasuresBetweenPoints(file):
    THRESHOLD = 100
    fread = open(WORKINGDIR + "/" + file, "r")
    lastlat = -1
    latlon = -1
    lastid = -1
    lasttime = -1
    
    distances = {}
    for line in fread.readlines():
        ll = line.split(" ")
        if lastlat == -1 or ll[0] != lastid:
            lastid = ll[0]
            lasttime = ll[1]
            lastlon = ll[2]
            lastlat = ll[3]
            prints(file, ll[0], ll[1], ll[2], ll[3].strip())
            continue
        if ll[0] == lastid:
            distance = measure(float(lastlat), float(lastlon), float(ll[3]), float(ll[2]))
            dd = str(int(distance))
            if dd not in distances:
                distances[dd] = 1
            else:
                distances[dd] += 1
            if distance > THRESHOLD:
                difftime = float(ll[1]) - float(lasttime)
                tree = queryService(lastlat, lastlon, ll[3], ll[2], False)
                parseQueryResponse(file,tree, ll[0], difftime,  lasttime, line, False)
            else:
                prints(file, ll[0], ll[1], ll[2], ll[3].strip())

            lastlat = float(ll[3])
            lastlon = float(ll[2])
            lasttime = float(ll[1])
        else:
            lastid == ll[0]
            lastlat = float(ll[3])
            lastlon = float(ll[2])
            lasttime = float(ll[1])

    #for elem in distances:
    #    print(str(elem) + " " + str(distances[elem]))
        

#for file in os.listdir(WORKINGDIR):
#    if TRIPS:
#        checkFileTooBig(file)
#cleanFiles()
createDirs()
counterFiles = 0
print("Just before starting")
if TRIPS:
    print("Let's start")
    for file2 in os.listdir(WORKINGDIR):
        print("file is " + str(file2))
        if os.path.isfile(WORKINGDIR + "/.done_" + sys.argv[7] + "_" + file2):
            continue
        if ".done" in file2:
            continue
        print(str(counterFiles) + " files done")
        counterFiles += 1
        cleanTrace(WORKINGDIR + "/" + file2)
        if os.path.isfile(FINALDIR + "/" + os.path.basename(file2)):
            ftemp = open(WORKINGDIR + "/.done_" + sys.argv[7] + "_" + file2, 'w+').close()

else:
    cleanTrace(WORKINGDIR + "/" + file)
