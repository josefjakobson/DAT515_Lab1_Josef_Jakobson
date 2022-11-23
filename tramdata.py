import json

tramstopsFile = open("tramstops.json")



def build_tram_stops(jsonobject):
    dict = json.load(jsonobject)
    stopsDict = {}
    for stop in dict:
        stopsDict[stop] = {}
        stopsDict[stop].update({"lat:" : dict[stop]["position"][0]})
        stopsDict[stop].update({"lon:" : dict[stop]["position"][1]})

    
    return stopsDict
     
    


build_tram_stops(tramstopsFile)


def build_tram_lines(file):
    tramlineDict = {}
    stopTimeDict = {}
    fullList = []
    with open(file, encoding='utf-8') as f:
        text = f.read()
        p = text.split("\n\n")
        for lines in p:
            line = lines.split("\n", 1)
            fullList.append(line[0])
            fullList.append(line[1].split("\n"))

    for i in range(len(fullList)):
        if i % 2 == 0:
            tramlineDict[fullList[i]] = [" ".join(stop[:-1]) for stop in [trimmed.split() for trimmed in fullList[i+1]]]

    
    print(tramlineDict)

    for i in range(len(fullList)):
        if i % 2 != 0:
            line1 = fullList[i][0].split()
            timeOne = line[-1]
            

build_tram_lines("tramlines.txt")