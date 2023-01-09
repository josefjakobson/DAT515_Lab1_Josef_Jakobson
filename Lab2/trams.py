import tramdata
from graphs import WeightedGraph, view_shortest
import json

TRAM_FILE = "tramnetwork.json"

class Tramnetwork(WeightedGraph):
    def __init__(self, stops_dict, lines_dict, times_dict, start=None):
        super().__init__(start)
        self._stops = stops_dict
        self._lines = lines_dict
        self._times = times_dict
    
    def stop_position(self, stop):
        return self._stops[stop]
    
    def transition_time(self, stop1, stop2):
        try:
            return self._times[stop1][stop2]
        except KeyError:
            return self._times[stop2][stop1]
    
    def geo_distance(self, stop1, stop2):
        return tramdata.distance_between_stops(stop1, stop2)
    
    def stop_lines(self, stop):
        return [line for line in self._lines if stop in self._lines[line]]
    
    def line_stops(self, line):
        val = self._lines[line].copy()
        return val
    
    def all_lines(self):
        return [line for line in self._lines]
    
    def all_stops(self):
        return [stop for stop in self._stops]
    
    def extreme_positions(self):
        max = (0,0)
        min = (0,0)
        for stop in self._stops:
            if max[0] < stop["lat"] and max[1] < stop["lon"]:
                max = (stop["lat"], stop["lon"])
                maxstop = stop
            if min[0] > stop["lat"] and min[1] > stop["lon"]:
                min = (stop["lat"], stop["lon"])
                minstop = stop
        return {"max" : maxstop, "min" : minstop}


def readTramNetwork(tramfile = TRAM_FILE):
    with open(tramfile, encoding="utf-8") as f:
        dict = json.load(f)
    
    return Tramnetwork(dict["stops"], dict["lines"], dict["times"])


def demo():
    G = readTramNetwork()
    a, b = input('from,to ').split(',')
    view_shortest(G, a, b)

if __name__ == '__main__':
    demo()