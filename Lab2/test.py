import networkx as nx
import graphs

graph = nx.Graph()

graph.add_weighted_edges_from([("a","b", 7), ("a","c", 9), ("a","f", 14), ("b","c", 10), ("b","d", 15), ("c","f", 2), ("c","d", 11), ("d","e", 6), ("f","e", 9)])

print(graphs.dijkstra(graph, "a", graphs.WeightedGraph.get_weight))