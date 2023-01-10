from hypothesis import given, strategies as st
from DAT515_Lab1_Josef_Jakobson.Lab1 import tramdata
import trams
import json


def test_all_stops():
    network = trams.readTramNetwork()
    with open("tramnetwork.json", encoding="utf-8") as f:
        dict = json.load(f)
    for stop in network.all_stops():
        assert stop in dict["stops"]


def test_all_lines():
    network = trams.readTramNetwork()
    with open("tramnetwork.json", encoding="utf-8") as f:
        dict = json.load(f)
    for line in network.all_lines():
        assert line in dict["lines"]


def test_stop_position():
    network = trams.readTramNetwork()
    with open("tramnetwork.json", encoding="utf-8") as f:
        dict = json.load(f)
    for stop in network.all_stops():
        assert network.stop_position(stop) == dict["stops"][stop]

def test_transition_time():
    network = trams.readTramNetwork()
    with open("tramnetwork.json", encoding="utf-8") as f:
        dict = json.load(f)
    for line in dict["lines"]:
        stoplist = dict["lines"][line]
        for i in range(len(stoplist) - 1):
            assert network.transition_time(stoplist[i], stoplist[i+1]) == tramdata.time_between_stops(dict, line, stoplist[i], stoplist[i+1])

if __name__ == '__main__':
    test_all_stops()
    test_all_lines()
    test_stop_position()
    test_transition_time()
