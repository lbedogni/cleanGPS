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

CACHE_NEAREST = {}
CACHE_SPEEDS = {}

fspeeds = open('roads.' + str(PREFIX) + '.final.csv','r')
for line in fspeeds.readlines():
    ll = line.split(",")
    try:
        CACHE_SPEEDS[ll[0].strip()] = float(ll[1].strip())
    except:
        CACHE_SPEEDS[ll[0].strip()] = -1
fspeeds.close()

fwNear = open(str(PREFIX) + '.cache.nearest.csv','r')
for line in fwNear.readlines():
    ll = line.split(",")
    CACHE_NEAREST[str(ll[0]) + "," + str(ll[1])] = str(ll[2]).strip()
fwNear.close()

S_BASE = "http://router.project-osrm.org/viaroute?hl=en&"
S_BASE_NEAREST = "http://router.project-osrm.org/nearest?loc="
S_END = "&output=gpx"

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
    if (gpx):
        return S_BASE + "loc=" + str(lats) + "," + str(lons) + "&loc=" + str(late).strip() + "," + str(lone).strip() + S_END
    return S_BASE + "loc=" + str(lats) + "," + str(lons) + "&loc=" + str(late).strip() + "," + str(lone).strip() + "&output=json&compression=false"
    
def prints(file, one,two,three,four):
#    print(file)
    fw = open(file, "a+")
    fw.write(str(one) + " " + str(math.floor(float(two))) + " " + str(three) + " " + str(four) + "\n")
    fw.close()

def queryServiceNearest(lat, lon):
    stringToGet = S_BASE_NEAREST + str(lon) + "," + str(lat)
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
            print("Querying service")
            xmlstring = urllib.request.urlopen(stringToGet, timeout = 2).read().decode("utf-8")
            #xmlstring = urllib.request.urlopen(req).read()
            toRepeat = False
        except urllib.error.HTTPError:
            # Probably error 400
            toRepeat = False
#            ff = open('exception_errors.log','a+')
#            ff.write(str(e.code) + " " + str(e.reason) + "\n")
#            ff.close()
            return False
        except:
            print("Connection problem. Pausing and repeating.")
            print(stringToGet)
            print(xmlstring)
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
            xmlstring = urllib.request.urlopen(stringToGet, timeout = 5).read().decode("utf-8")
            #xmlstring = urllib.request.urlopen(req).read()
            toRepeat = False
        except urllib.error.HTTPError:
            # Probably error 400
            toRepeat = False
#            ff = open('exception_errors.log','a+')
#            ff.write(str(e.code) + " " + str(e.reason) + "\n")
#            ff.close()
            return False
        except:
            print("Connection problem. Pausing and repeating.")
            print(stringToGet)
            print(xmlstring)
            time.sleep(5)
#    print("DONE")
#    print(xmlstring)
    if gpx:
        return ET.fromstring(xmlstring)
    return xmlstring

def parseQueryResponse(file, tree, id, difftime,  ttstart, line, gpx):
    if gpx:
        numelem = max(len(tree[1]), 1)
        deltatime = difftime / numelem
        timenow = ttstart
        for elem in tree[1]:
#            print("*** " + str(elem.attrib['lon']) + " " + str(elem.attrib['lat']))
            prints(file, str(id), str(math.ceil(timenow)), elem.attrib['lon'], elem.attrib['lat'] + " # from parseQueryResponse - " + str(line))
            #prints(file, str(id), str(timenow), elem.attrib['lon'], elem.attrib['lat'])
            timenow = float(timenow) + float(deltatime)
        return True
    else:
        # JSON
        import json
        jj = json.loads(tree)
        print("ALALALA TTSTART is " + str(ttstart))
        print("ALALALA DIFFTIME is + " + str(difftime))
        if 'route_geometry' in jj:
            print("***********************************************************************")
            numelem = len(jj['route_geometry'])
            if numelem >= 2:
                numelem -= 1
            deltatime = difftime / numelem
            print("TTSTART is " + str(ttstart) + ", NUMELEM is " + str(numelem) + ", DIFFTIME is " + str(difftime) + ", DELTATIME is " + str(deltatime))
            #fwDebug = open('nearest_debug.log','a')
            if deltatime > 1:
                timenow = ttstart
                #print(json.load(reader(tree)))
                #print("NEAREST_DEBUG  --- NEW ROUTE --- ")
                #fwDebug.write("NEAREST_DEBUG  --- NEW ROUTE --- " + "\n")
                lastRoad = -1
                allItems = {}
                for item in json.loads(tree)['route_geometry']:
                    nearest_road = -1
                    if str(item[1]) + "," + str(item[0]) in CACHE_NEAREST:
                        # We already have it
                        nearest = CACHE_NEAREST[str(item[1]) + "," + str(item[0])]
                        #print("NEAREST_DEBUG ** CACHE_HIT ** Coords are: " + str(item[1]) + " " + str(item[0]) + ". NEAREST is : " + str(nearest))
                        #fwDebug.write("NEAREST_DEBUG ** CACHE_HIT ** Coords are: " + str(item[1]) + " " + str(item[0]) + ". NEAREST is : " + str(nearest) + "\n")
                        nearest_road = str(nearest)
                    else:
                        #print("NEAREST_DEBUG ** CACHE_MISS ** Coords are: " + str(item[1]) + " " + str(item[0]))
                        nearest = queryServiceNearest(item[1],item[0])
                        ii = json.loads(nearest)
                        import re
                        nearest_road = re.sub("\(.*\)",'',str(ii['name']).strip()).strip()
                        CACHE_NEAREST[str(item[1]) + "," + str(item[0])] = nearest_road
                        fwNear = open(str(PREFIX) + '.cache.nearest.csv','a')
                        fwNear.write(str(item[1]) + "," + str(item[0]) + "," + nearest_road + "\n")
                        fwNear.close()
                        #print("NEAREST_DEBUG Coords are: " + str(item[1]) + " " + str(item[0]) + ". NEAREST is : " + str(nearest_road))
                        #fwDebug.write("NEAREST_DEBUG Coords are: " + str(item[1]) + " " + str(item[0]) + ". NEAREST is : " + str(nearest_road) + "\n")

                    if nearest_road == "":
                        nearest_road = lastRoad
                    else:
                        lastRoad = nearest_road

                    if nearest_road not in CACHE_SPEEDS:
                        fwMissing = open(str(PREFIX) + 'roads.missing','a')
                        fwMissing.write(str(nearest_road) + "\n")
                        fwMissing.close()
                        #print("NEAREST_DEBUG Can't find speed for road: " + str(nearest_road))
                        #fwDebug.write("NEAREST_DEBUG Can't find speed for road: " + str(nearest_road) + "\n")
                        CACHE_SPEEDS[nearest_road] = -1

#                    print("*** " + str(item[1]) + " " + str(item[0]))
                    allItems[timenow] = [float(item[1]), float(item[0]), CACHE_SPEEDS[nearest_road]]
                    timenow = float(timenow) + float(deltatime)
                # Now we need to compute distances bound to speeds
                allDistances = {}
                point1 = -1
                point2 = -1
                time1 = -1
                time2 = -1
 #               totalTime = 0
                print(allItems)
                summaTimes = 0
                summaDistance = 0
                lastIntermediate = 0
                #print("---------------------TIMEDEBUG--------------------------------")
                for intermediatePoint in sorted(allItems):
                    #print("******")
                    #print(allItems[intermediatePoint])
                    #print(intermediatePoint)
                    #print("ALL Points: " + " - ".join([str(allItems[intermediatePoint][0]), str(allItems[intermediatePoint][1]), str(allItems[intermediatePoint][2])]))
                    if point1 == -1:
                        # First time
                        point1 = (allItems[intermediatePoint][1],allItems[intermediatePoint][0])
                        time1 = ttstart
                        time2 = ttstart
                        lastIntermediate = ttstart
                        print("First time since point1 is -1")
                        print(point1)
                        print(intermediatePoint)
                    else:
                        point2 = (allItems[intermediatePoint][1],allItems[intermediatePoint][0])
                        distance = vincenty(point1, point2).miles * 1609.34
                        summaDistance += distance
                        deltaTime = intermediatePoint - lastIntermediate
                        lastIntermediate = intermediatePoint
                        time2 = intermediatePoint - time1
                        if allItems[intermediatePoint][2] == -1:
                            allItems[intermediatePoint][2] = 50

                        estimatedTime = distance / (allItems[intermediatePoint][2] / 3.6)
                        #print("TIMEDEBUG - Index = " + str(time2) + " - With " + str(distance) + " meters and " + str(allItems[intermediatePoint][2]) + " km/h the estimated time is " + str(estimatedTime))
                        summaTimes += estimatedTime
                        #print("TIMEDEBUG - summaTimes is now " + str(summaTimes))
                        allDistances[time2] = [point1, point2, distance, time2, allItems[intermediatePoint][2], estimatedTime]
#                        time1 = intermediatePoint
#                        totalTime = intermediatePoint - time1
                        point1 = point2

                #print("TIMEDEBUG = " + str(sorted(allDistances)))
                print("Total Distance = " + str(summaDistance) + " - Total time = " + str(summaTimes) + " - GPS delta time = " + str(difftime))
                allMinusOne = True
                totalDistance = 0
                factor = 1
                if summaTimes > 0:
                    factor = (difftime * 1.0) / (summaTimes)
                    fwFactor = open('allFactors.csv','a')
                    fwFactor.write(str(factor) + "\n")
                    fwFactor.close()
                for item in allDistances:
                    totalDistance += allDistances[item][2]
                    if allDistances[item][4] > -1:
                        allMinusOne = False

                avgSpeed = totalDistance / (difftime * 1.0)
                print("THE AVG SPEED IS " + str(avgSpeed))
                if avgSpeed > 50:
                    fwDDD = open('highspeeds.txt','a')
                    countAllDist = 0
                    lastItem = -1
                    fwDDD.write(id + " - ")
                    for item in allDistances:
                        if countAllDist == 0:
                            fwDDD.write(str(allDistances[item]))
                            countAllDist = 1
                        lastItem = allDistances[item]
                    fwDDD.write(" - " + str(lastItem[0]) + " - " + str(avgSpeed) + " - " + str(totalDistance) + " - " + str(difftime) + " --- " + str(line) + "\n")
                    fwDDD.close()
                else:
                    fwDDD = open('lowspeeds.txt','a')
                    countAllDist = 0
                    lastItem = -1
                    fwDDD.write(id + " - ")
                    for item in allDistances:
                        if countAllDist == 0:
                            fwDDD.write(str(allDistances[item]))
                            countAllDist = 1
                        lastItem = allDistances[item]
                    if (lastItem != -1):
                        print(lastItem)
                        fwDDD.write(" - " + str(lastItem[0]) + " - " + str(avgSpeed) + " - " + str(totalDistance) + " - " + str(difftime) + " --- " + str(line) + "\n")
                    else:
                        fwDDD.write("\n")
                    fwDDD.close()

#                if not allMinusOne:
#                    print("********** We have at least a speed greater than -1 ********")
#                    print(allDistances)
                    

                incrementalTime = ttstart
                #print("TIMEDEBUG *** START - FACTOR is " + str(factor) + " - WE START AT " + str(ttstart) + " with a difftime of " + str(difftime) + " - summaTimes is " + str(summaTimes) + " - We finish at " + str(difftime + ttstart) + " ***")
                lastTime = -1
                for itemDistance in sorted(allDistances):
                    # Here we should compute all distances and times
                    #print("TIMEDEBUG - Checking item " + str(allDistances[itemDistance]))
#                    print("We write: " + str(incrementalTime) + " - " + str(allDistances[itemDistance][1][0]) + " - " + str(allDistances[itemDistance][1][1]))
                    if lastTime == -1:
                        incrementalTime = ttstart
                        estimatedTime = float(allDistances[itemDistance][5])
                        #print("TIMEDEBUG - TIME NOW IS " + str(incrementalTime))
                        prints(file, str(id), str(incrementalTime), allDistances[itemDistance][0][0], str(allDistances[itemDistance][0][1]) + " #--- " + str(ttstart))
                        incrementalTime += (estimatedTime * factor)
                        prints(file, str(id), str(incrementalTime), allDistances[itemDistance][1][0], str(allDistances[itemDistance][1][1]) + " #--- " + str(ttstart))
                    else:
                        estimatedTime = float(allDistances[itemDistance][5])
                        incrementalTime += (estimatedTime * factor)
                        #print("TIMEDEBUG - ESTIMATED TIME is " + str(estimatedTime) + " with factor(" + str(estimatedTime * factor) + ") - TIME NOW IS " + str(int(incrementalTime)))
                        prints(file, str(id), str(int(incrementalTime)), allDistances[itemDistance][1][0], str(allDistances[itemDistance][1][1]) + " #--- " + str(ttstart))
                    lastTime = itemDistance
#                    print("We increment by " + str(itemDistance))
                
                # Write last point
#                if lastTime != -1:
#                    prints(file, str(id), str(ttstart + difftime), allDistances[lastTime][1][0], str(allDistances[lastTime][1][1]) + " #--- " + str(ttstart))
#                    estimatedTime = float(allDistances[lastTime][5])
#                    print("TIMEDEBUG - ESTIMATED TIME is " + str(estimatedTime) + " with factor(" + str(estimatedTime * factor) + ") - TIME NOW IS " + str(incrementalTime))
                
                #for intermediatePoint in json.loads(tree)['route_name']:
 #                   print("NEAREST_DEBUG route_name : : " + str(intermediatePoint))
                    #fwDebug.write("NEAREST_DEBUG route_name : : " + str(intermediatePoint) + "\n")
                #fwDebug.close()
                #print("*** END ***")
                return True
            else:
                print("****")
                print(deltatime)
                print(difftime)
                print(numelem)
                print(line)
                print("----")
                timenow = ttstart
                deltaitems = numelem / difftime
                counter = 1
                for item in json.loads(tree)['route_geometry']:
                    if counter == 1 or counter % deltaitems == 0:
#                        print("*** " + str(item[1]) + " " + str(item[0]))
                        prints(file, str(id), str(math.ceil(timenow)), item[1], str(item[0]) + " # from parseQueryResponse - " + str(line).strip())
                        timenow = float(timenow) + 1
                    counter += 1
                return True


        else:
            # Need to parse data from the caller
            print("PROBLEM")
            return False

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
    print(line)
    ll = line.split(",")
    ID = ll[0].strip()
    tt = math.ceil(float(ll[1].strip()))
    lat = ll[2].strip()
    lon = ll[3].strip()
    if lon.strip() == "" or lat.strip() == "":
        return
    else:
        return ID,tt,lon,lat

def getTripsBeijing(line):
    print(line)
    ll = line.split(",")
    ID = ll[0].strip()
    #tt = math.ceil(float(ll[1].strip()))
    from datetime import datetime
    #tt = int(datetime.datetime.fromtimestamp(int(tt)).strftime("%Y-%m-%d $H:$M:$S"))
    tt = datetime.strptime(ll[1].strip(), '%Y-%m-%d %H:%M:%S').timestamp()
    print(tt)
    lat = ll[2].strip()
    lon = ll[3].strip()
    if lon.strip() == "" or lat.strip() == "":
        return
    else:
        return ID,tt,lon,lat
    
def getTripsSF(line):
#    print(line)
    ll = line.split(" ")
    tt = math.ceil(float(ll[3].strip()))
    #import datetime
    #tt = int(datetime.datetime.fromtimestamp(int(tt)).strftime("%Y%m%d"))
    #tt*= 1000
    lat = ll[1].strip()
    lon = ll[0].strip()
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
#        elif city == "rome":
            # ROME
#            if ttstart == -1:
                #First round
#                [ID,ttstart,lonstart,latstart] = getTripsRome(line)
#                continue
#            else:
                #Second or more round
#                [ID,ttend,lonend,latend] = getTripsRome(line)
        elif city == "beijing":
            # ROME
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
            print("Different trip, treat it as new one")
            ttstart = ttend
            lonstart = lonend
            latstart = latend
            continue
        
        if difftime == 0 and (city in ["rome","sf","turin","palermo","milan","bari"]):
            prints(OUTPUTDIR + "/" + str(file) + "_" + str(ID) + ".csv", str(ID), str(ttend), latend, lonend)
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

        allCities = ["rome","sf","turin","bari","palermo","milan","beijing","shanghai"]
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
        print("NOT Valid Point")
        print(str(lat) + "," + str(LATMIN))
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
        ll = line.split(" ")
        thistime = 0
        try:
            thistime = time.mktime(time.strptime(ll[1], "%Y-%m-%d %H:%M:%S"))
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
#            print("**** difftime > THRESHOLD. line = " + line.strip())
#            print("****** lastlat: " + lastlat,  ", lastlng: ", lastlng)
            # We need to interpolate
            # In difftime seconds we need to go form lastlat,lastlng to ll[2],ll[3], every deltasec
            dist = measure(float(ll[2]),float(ll[3]),float(lastlng),float(lastlat))
            difftime = max(1,difftime)
            speed = dist/difftime
#            if speed > SPEEDTHRESHOLD:
                # This is not an error, but it might be that it's the same vehicle on a different day
#                print("ERROR")
#                print(str(ll) + " " + str(difftime) + " " + str(lasttime) + " " + str(thistime) + " " + str(speed))
#                sys.exit()
#                lasttime = thistime
#                lastlat = ll[2]
#                lastlng = ll[3]
#                prints(FINALDIR + "/" + os.path.basename(file), ll[0],lasttime,lastlat,str(lastlng).strip())
#                continue
            numtime = int(math.ceil(difftime / deltasec))
            difflng = (float(ll[2]) - float(lastlng))/numtime
            difflat = (float(ll[3]) - float(lastlat))/numtime
            thislat = float(lastlat)
            thislng = float(lastlng)
            #lasttime = thistime
            increment = difftime / numtime
            if increment != 1:
                print("Error! increment is " + str(increment) + ". diffitime = " + str(difftime) + ", numtime = " + str(numtime))
#            print("ENTERING TO INTERPOLATE",lasttime,thistime)
            #prints(FINALDIR + "/" + os.path.basename(file), ll[0],lasttime,thislat,str(thislng) + " #FIRST INTERPOLATE POINT")
            for i in range(1,numtime):
                thislat = float(thislat) + float(difflat)
                thislng = float(thislng) + float(difflng)
                prints(FINALDIR + "/" + os.path.basename(file), ll[0],lasttime + i * increment,thislat,str(thislng) + " #INTERPOLATE POINT")
#                if not checkValidPoint(thislat, thislng):
#                    continue
#                else:
            prints(FINALDIR + "/" + os.path.basename(file), ll[0],ll[1],ll[2],ll[3].strip() + " #LAST INTERPOLATE POINT")
            lasttime = float(ll[1])
            lastlng = ll[2]
            lastlat = ll[3]

        else:
#            print("NO INTERPOLATE",lasttime,thistime)
            dist = measure(float(ll[3]),float(ll[2]),float(lastlng),float(lastlat))
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
if TRIPS:
    for file in os.listdir(WORKINGDIR):
        if os.path.isfile(WORKINGDIR + "/.done_" + sys.argv[7] + "_" + file):
            print(sys.argv[7] + " - Already parsed file: " + str(file))
        else:
            if ".done_" in file:
                continue
            print(str(sys.argv[7]) + "-" + str(sys.argv[8]) + ". Starting with file: " + file)
            for item in os.listdir(OUTPUTDIR):
                if file in item:
                    os.remove(OUTPUTDIR + "/" + item)
            print("Parsing")
            getPointsFromTrips(file)
            ftemp = open(WORKINGDIR + "/.done_" + sys.argv[7] + "_" + file, 'w+').close()
    counterFiles = 1
    print(sys.argv[7] + " - Now starting to clean the trace")
    for file in os.listdir(OUTPUTDIR):
        if os.path.isfile(OUTPUTDIR + "/.done_" + sys.argv[7] + "_" + file):
            continue
        if ".done" in file:
            continue
        print(str(counterFiles) + " files done")
        counterFiles += 1
        cleanTrace(OUTPUTDIR + "/" + file)
        if os.path.isfile(FINALDIR + "/" + os.path.basename(file)):
            ftemp = open(OUTPUTDIR + "/.done_" + sys.argv[7] + "_" + file, 'w+').close()

else:
    cleanTrace(WORKINGDIR + "/" + file)
