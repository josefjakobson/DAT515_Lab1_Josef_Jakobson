import networkx as nx
import sys
import graphviz

class Graph(nx.Graph):
    def __init__(self, start = None):
        super().__init__(start)
    
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
            currentCost = cost(nbr, currentNode) + path_and_cost_dict[currentNode]["cost"]
            if currentCost < path_and_cost_dict[nbr]["cost"]:
                path_and_cost_dict[nbr]["cost"] = currentCost
                path_and_cost_dict[nbr]["path"] = path_and_cost_dict[currentNode]["path"] + [nbr]
        
        unvisitedNodes.remove_node(currentNode)
    
    return path_and_cost_dict



def initialize_unvisited(graph):
    dict = {}
    for vertex in graph.adj:
        dict[vertex] = {"cost":sys.maxsize, "path" : []}
    return dict



def visualize(graph : Graph, view='dot', name='mygraph', nodecolors=None):
    visual_graph = graphviz.Graph()
    for node in graph.vertices():
        visual_graph.node(str(node))
    for (v,w) in graph.edges():
        visual_graph.edge(str(v), str(w))
    visual_graph.render(view = True)


def view_shortest(G, source, target, cost=lambda u,v: 1):
    path = dijkstra(G, source, cost)[target]['path']
    print(path)
    colormap = {str(v): 'orange' for v in path}
    print(colormap)
    visualize(G, view='view', nodecolors=colormap)

def demo():
    G = Graph([(1,2),(1,3),(1,4),(3,4),(3,5),(3,6), (3,7), (6,7)])
    view_shortest(G, 2, 6)

if __name__ == '__main__':
    demo()


