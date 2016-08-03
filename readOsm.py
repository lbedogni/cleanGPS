from imposm.parser import OSMParser
import sys

speeds = {}

allRoads = {}

# simple class that handles the parsed OSM data.
class HighwayCounter(object):
    highways = 0
    maxspeed = -1
    name = 0
    name_1 = 0

    def ways(self, ways):
        # callback method for ways
        counterAA = 0
        for osmid, tags, refs in ways:
            #print "Another one: " + str(counterAA)
            counterAA += 1
            if 'name_1' in tags:
  #              print("NAME_1: " + str(tags['name_1']))
                self.name_1 += 1
            if 'maxspeed' in tags:
   #             print("MAXSPEED: " + str(tags['maxspeed']))
                self.maxspeed += 1
                if tags['maxspeed'] not in speeds:
                    speeds[tags['maxspeed']] = 0
                speeds[tags['maxspeed']] += 1
            if 'highway' in tags:
                if 'name' in tags:
                    self.name += 1
                    name = tags['name']
                    #while name in allRoads:
                    #    name  += "*"
                        #print "We already have this road: " + str(name)
                    if name not in allRoads:
                        allRoads[name] = []

                    if 'maxspeed' in tags:
                        allRoads[name].append([tags['highway'],tags['maxspeed']])
                    else:
                        allRoads[name].append([tags['highway'],-1])
    #          print(tags)
                self.highways += 1

# instantiate counter and parser and start parsing
counter = HighwayCounter()
p = OSMParser(concurrency=4, ways_callback=counter.ways)
p.parse(sys.argv[1])

print "Finished everything"

# done
print counter.highways
print counter.name
print counter.name_1
print counter.maxspeed
print speeds

print allRoads
fw = open('roads.turin.csv','w')
fw2 = open('roads.turin.final.csv','w')
for key in allRoads:
    print("Road: " + key.encode('utf-8'))
    fw.write(key.encode('utf-8') + "," + str(allRoads[key]) + "\n")
    # Get all speeds
    speeds = []
    assignedSpeed = -2
    print(allRoads[key])
    for item in allRoads[key]:
        if item[1] >= 30 and item[1] <= 130:
            speeds.append(item[1])
    if len(speeds) > 0:
        assignedSpeed = sum(speeds)/len(speeds)
    while assignedSpeed == -2:
        # Need to search for road type
        for item in allRoads[key]:
            if item[0] == "motorway":
                assignedSpeed = 130
            elif item[0] == "trunk":
                assignedSpeed = 90
            elif item[0] == "primary":
                assignedSpeed = 70
            elif item[0] == "tertiary":
                assignedSpeed = 50
            elif item[0] == "residential":
                assignedSpeed = 30
        if assignedSpeed == -2:
            # We have nothing for this road
            assignedSpeed = -1
    fw2.write(key.encode('utf-8') + "," + str(assignedSpeed) + "\n")

        
fw.close()
fw2.close()
