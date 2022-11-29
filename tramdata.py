import json
import math
import sys


def build_tram_stops(jsonobject):
    dict = json.load(jsonobject)
    stopsDict = {}
    for stop in dict:
        stopsDict[stop] = {}
        stopsDict[stop].update({"lat:" : dict[stop]["position"][0]})
        stopsDict[stop].update({"lon:" : dict[stop]["position"][1]})
    return stopsDict

def build_tram_lines(fullList):
    tramlineDict = {}
    for i in range(len(fullList)):
        if i % 2 == 0:
            tramlineDict[fullList[i][:-1]] = [" ".join(stop[:-1]) for stop in [trimmed.split() for trimmed in fullList[i+1]]]
    return tramlineDict
            
        
def build_stop_times(fullList):
    stopTimeDict = {}
    for i in range(len(fullList)):
        if i % 2 != 0:
            for j in range(len(fullList[i])-1):
                stop1 = " ".join(fullList[i][j].split()[:-1])
                stop2 = " ".join(fullList[i][j+1].split()[:-1])
                timeBetween = int(fullList[i][j+1].split()[-1][-2:]) - int(fullList[i][j].split()[-1][-2:])
                if stop1 in stopTimeDict:
                    stopTimeDict[stop1].update({stop2:timeBetween})
                else:
                    stopTimeDict[stop1] = {stop2:timeBetween}
    return stopTimeDict
        
def format_textfile(file):
    fullList = []
    with open(file, encoding='utf-8') as f:
        text = f.read()
        p = text.split("\n\n")
        for lines in p:
            line = lines.split("\n", 1)
            fullList.append(line[0])
            fullList.append(line[1].split("\n"))
    return fullList

def build_tram_network(stopdict, linedict, timedict):
    networkDict = {"stops":stopdict, "lines" : linedict, "times":timedict}
    with open('tramnetwork.json', 'w', encoding="utf-8") as f:
        json.dump(networkDict, f, indent=4, ensure_ascii=False)

        

def lines_via_stops(networkDict, stop):
    resultlist = []
    for line in networkDict["lines"]:
        if stop in networkDict["lines"][line]:
            resultlist.append(line)
    return resultlist

def lines_between_stops(networkDict, stop1, stop2):
    resultlist = []
    for line in networkDict["lines"]:
        if stop1 in networkDict["lines"][line] and stop2 in networkDict["lines"][line]:
            resultlist.append(line)
    return resultlist

def distance_between_stops(networkDict, stop1, stop2):
    deltaLat = (float(networkDict["stops"][stop1]["lat:"]) - float(networkDict["stops"][stop2]["lat:"])) * math.pi/180
    deltaLon = (float(networkDict["stops"][stop1]["lon:"]) - float(networkDict["stops"][stop2]["lon:"])) * math.pi/180
    meanLat = (float(networkDict["stops"][stop1]["lat:"]) + float(networkDict["stops"][stop2]["lat:"]))* math.pi/180/2
    return 6371.009*math.sqrt(deltaLat**2 + (math.cos(meanLat)*deltaLon)**2)


def time_between_stops(networkDict, line, stop1, stop2):
    stopset = networkDict["lines"][line]
    index1 = stopset.index(stop1)
    index2 = stopset.index(stop2)
    journeySet = stopset[index1:index2+1]
    totalTime = 0
    for i in range(len(journeySet) - 1):
        totalTime += networkDict["times"][journeySet[i]][journeySet[i+1]]
    
    return totalTime

def dialogue(jsonfile):
    dict = json.load(jsonfile)
    userInput = input("> ")
    while userInput != "quit":
        print(answer_query(dict, userInput))
        userInput = input("> ")

def answer_query(dict, userInput):
    if "via" in userInput:
        stop = " ".join(userInput.split()[1:])
        return lines_via_stops(dict, stop)
    elif "between" in userInput:
        userInput = userInput.split()
        andIndex = userInput.index("and")
        stop1 = " ".join(userInput[1:andIndex])
        stop2 = " ".join(userInput[andIndex+1:])
        return lines_between_stops(dict, stop1, stop2)
    elif "time" in userInput:
        userInput = userInput.split()
        fromIndex = userInput.index("from")
        toIndex = userInput.index("to")
        line = userInput[2:fromIndex][0]
        stop1 = " ".join(userInput[fromIndex+1:toIndex])
        stop2 = " ".join(userInput[toIndex+1:])
        return time_between_stops(dict, line, stop1, stop2)
    elif "distance" in userInput:
        userInput = userInput.split()
        fromIndex = userInput.index("from")
        toIndex = userInput.index("to")
        stop1 = " ".join(userInput[fromIndex+1:toIndex])
        stop2 = " ".join(userInput[toIndex+1:])
        return distance_between_stops(dict, stop1, stop2)
    else:
        return "Sorry, try again"



def initialize():
    tramstopsFile = open("tramstops.json")
    formattedList = format_textfile("tramlines.txt")
    stops = build_tram_stops(tramstopsFile)
    lines = build_tram_lines(formattedList)
    times = build_stop_times(formattedList)
    build_tram_network(stops, lines, times)
    tramstopsFile.close()





if __name__ == '__main__':
    if sys.argv[1:] == ['init']:
        initialize()
    else:
        with open("tramnetwork.json", encoding="utf-8") as f:
            dialogue(f)			
