import unittest
from tramdata import *

TRAM_FILE = 'tramnetwork.json'

class TestTramData(unittest.TestCase):

    def setUp(self):
        with open(TRAM_FILE, encoding="utf-8") as trams:
            tramdict = json.loads(trams.read())
            self.stopdict = tramdict['stops']
            self.linedict = tramdict['lines']
            self.fulldict = tramdict

    def test_stops_exist(self):
        stopset = {stop for line in self.linedict for stop in self.linedict[line]}
        for stop in stopset:
            self.assertIn(stop, self.stopdict, msg = stop + ' not in stopdict')
    
    def test_lines_exist(self):
        lineset = []
        with open("tramlines.txt", encoding="utf-8") as f:
            text = f.read()
            p = text.split("\n\n")
            for line in p:
                lineset.append(line.split("\n", 1)[0][:-1])
            

        for line in lineset:
            self.assertIn(line, self.linedict, msg=line+"not in linedict")
    
    def test_stops_per_line(self):
        list = []
        stopset = []
        with open("tramlines.txt", encoding="utf-8") as f:
            text = f.read()
            p = text.split("\n\n")
            for lines in p:
                line = lines.split("\n", 1)
                list.append(line[1].split("\n"))

        for i in range(len(list)):
            stopset.append([" ".join(stop[:-1]) for stop in [trimmed.split() for trimmed in list[i]]]) 
            
        i = 0
        for line in self.linedict:
            self.assertEqual(stopset[i], self.linedict[line], msg="not in linedict")
            i += 1
            
    def test_feasible_distances(self):
        for stop1 in self.stopdict:
            for stop2 in self.stopdict:
                self.assertLessEqual(distance_between_stops(self.stopdict, stop1, stop2), 20)
            
    def test_same_time_between_stops(self):
        for line in self.linedict:
            for stop1 in self.linedict[line]:
                for stop2 in self.linedict[line]:
                    self.assertEqual(time_between_stops(self.fulldict, line, stop1, stop2), time_between_stops(self.fulldict, line, stop2, stop1))
    

    def test_dialogue(self):
        self.assertEqual(answer_query(self.fulldict, "via Chalmers"), lines_via_stops(self.fulldict, "Chalmers"))
        self.assertEqual(answer_query(self.fulldict, "between Chalmers and Östra Sjukhuset"), lines_between_stops(self.fulldict, "Chalmers", "Östra Sjukhuset"))
        self.assertEqual(answer_query(self.fulldict, "time with 6 from Chalmers to Korsvägen"), time_between_stops(self.fulldict, "6", "Chalmers" ,"Korsvägen"))
        self.assertEqual(answer_query(self.fulldict, "distance from Chalmers to Korsvägen"), distance_between_stops(self.fulldict["stops"], "Chalmers", "Korsvägen"))


if __name__ == '__main__':
    unittest.main()
