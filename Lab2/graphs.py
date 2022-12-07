import networkx as nx
import sys

class Graph(nx.Graph):
    def __init__(self, start = None):
        super.__init__(start)
    
    def vertices(self):
        return self.nodes()
    
    def add_vertex(self, vertex):
        if vertex.isinstance(list):
            self.add_nodes_from(vertex)
        else:
            self.add_node(vertex)
    
    def __len__(self):
        return self.number_of_nodes
    
    def remove_vertex(self, vertex):
        self.remove_node(vertex)
    
    def get_vertex_value(self, vertex):
        value = self.nodes[vertex]
        return value
    
    def set_vertex_value(self, vertex, value):
        self.nodes[vertex] = value


class WeightedGraph(Graph):
    def __init__(self, start=None):
        super().__init__(start)

    def set_weight(self, vertex1, vertex2, weight):
        self[vertex1][vertex2]["weight"] = weight
    
    def get_weight(self, vertex1, vertex2):
        weight = self[vertex1][vertex2]["weight"]
        return weight


def dijkstra(graph, source, cost = lambda u,v: 1):
    unvisitedNodes = nx.Graph(graph)
    path_and_cost_dict = initialize_unvisited(graph)
    path_and_cost_dict[source]["cost"] = 0
    while unvisitedNodes:
        currentNode = None
        for node in unvisitedNodes.adj:
            if currentNode == None:
                currentNode = node
            elif path_and_cost_dict[currentNode]["cost"] > path_and_cost_dict[node]["cost"]:
                currentNode = node
        
        for nbr in unvisitedNodes.adj[currentNode]:
            currentCost = cost(graph, nbr, currentNode) + path_and_cost_dict[currentNode]["cost"]
            if currentCost < path_and_cost_dict[nbr]["cost"]:
                path_and_cost_dict[nbr]["cost"] = currentCost
                path_and_cost_dict[nbr]["path"] = path_and_cost_dict[currentNode]["path"] + [nbr]
        
        unvisitedNodes.remove_node(currentNode)
    
    return path_and_cost_dict

    #for neighbour in graph.adj[source]:
    #    currentCost = cost(source, neighbour)
    #    unvisitedNodes[neighbour]["cost"] = currentCost + unvisitedNodes[source]["cost"]
    #    unvisitedNodes[neighbour]["path"].append(neighbour)
    #    finishedDict[neighbour] = unvisitedNodes.pop(neighbour)



def initialize_unvisited(graph):
    dict = {}
    for vertex in graph.adj:
        dict[vertex] = {"cost":sys.maxsize, "path" : []}
    return dict



