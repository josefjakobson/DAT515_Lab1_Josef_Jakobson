import unittest
from tramdata import *

TRAM_FILE = './tramnetwork.json'

class TestTramData(unittest.TestCase):

    def setUp(self):
        with open(TRAM_FILE, encoding="utf-8") as trams:
            tramdict = json.loads(trams.read())
            self.stopdict = tramdict['stops']
            self.linedict = tramdict['lines']

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
                lineset.append(line.split("\n", 1)[0])
            

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
            if i % 2 == 0:
                stopset.append([" ".join(stop[:-1]) for stop in [trimmed.split() for trimmed in list[i+1]]]) 
            
        i = 0
        for line in self.linedict:
            self.assertIn(stopset[i], line, msg="not in linedict")
            i += 1
            



    # add your own tests here


if __name__ == '__main__':
    unittest.main()
