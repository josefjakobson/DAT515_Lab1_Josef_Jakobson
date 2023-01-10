import json

# imports added in Lab3 version
import math
import os
from .graphs import WeightedGraph
from django.conf import settings


# path changed from Lab2 version
# TODO: copy your json file from Lab 1 here
TRAM_FILE = os.path.join(settings.BASE_DIR, 'static\\tramnetwork.json')


class Tramnetwork(WeightedGraph):
    def __init__(self, stops_dict, lines_dict, times_dict, start=None):
        super().__init__(start)
        self._stops = stops_dict
        self._lines = lines_dict
        self._times = times_dict
        self._set_internal_graph()

    def _set_internal_graph(self):
        for line in self._lines:
            stops = self._lines[line]
            for i in range(len(stops)-1):
                stop1 = stops[i]
                stop2 = stops[i+1]
                self.add_edge(stop1, stop2)
                self[stop1][stop2]["weight"] = self.transition_time(stop1, stop2)
                self[stop1][stop2]["line"] = line

    def stop_position(self, stop):
        return self._stops[stop]
    
    def transition_time(self, stop1, stop2):
        if stop2 not in self[stop1] and stop1 not in self[stop2]:
            return None
        try:
            return self._times[stop1][stop2]
        except KeyError:
            return self._times[stop2][stop1]
    
    def geo_distance(self, stop1, stop2):
        if stop1 not in self._stops or stop2 not in self._stops:
            return "Unkown arguments"
        deltaLat = (float(self._stops[stop1]["lat:"]) - float(self._stops[stop2]["lat:"])) * math.pi/180
        deltaLon = (float(self._stops[stop1]["lon:"]) - float(self._stops[stop2]["lon:"])) * math.pi/180
        meanLat = (float(self._stops[stop1]["lat:"]) + float(self._stops[stop2]["lat:"]))* math.pi/180/2
        return round(6371.009*math.sqrt(deltaLat**2 + (math.cos(meanLat)*deltaLon)**2), 3)
        
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


def readTramNetwork():
    with open(TRAM_FILE, encoding="utf-8") as f:
        dict = json.load(f)
    return Tramnetwork(dict["stops"], dict["lines"], dict["times"])



# Bonus task 1: take changes into account and show used tram lines

def specialize_stops_to_lines(network):
    # TODO: write this function as specified
    return network


def specialized_transition_time(spec_network, a, b, changetime=10):
    # TODO: write this function as specified
    return changetime


def specialized_geo_distance(spec_network, a, b, changedistance=0.02):
    # TODO: write this function as specified
    return changedistance
