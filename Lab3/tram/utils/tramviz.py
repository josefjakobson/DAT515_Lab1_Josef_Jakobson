# visualization of shortest path in Lab 3, modified to work with Django

from .trams import readTramNetwork
from .graphs import dijkstra
from .color_tram_svg import color_svg_network
import os
from django.conf import settings

def show_shortest(dep, dest):
    network = readTramNetwork()

    time_cost = lambda x, y : network.transition_time(x, y)
    distance_cost = lambda x,y : network.geo_distance(x, y)
    
    quickest = dijkstra(network, dep, time_cost)[dest]
    shortest = dijkstra(network, dep, distance_cost)[dest]

    timepath = 'Quickest: ' + ', '.join(quickest["path"]) + ', ' + str(quickest["cost"]) + " minutes"
    geopath = 'Shortest: ' + ', '.join(shortest["path"]) + ', ' + str(round(shortest['cost'], 2)) +' km'

    def colors(v):
        if v in shortest["path"] and v in quickest["path"]:
            return 'cyan'
        elif v in shortest["path"]:
            return 'green'
        elif v in quickest["path"]:
            return "orange"
        else:
            return "white"
            

    # this part should be left as it is:
    # change the SVG image with your shortest path colors
    color_svg_network(colormap=colors)
    # return the path texts to be shown in the web page
    return timepath, geopath
