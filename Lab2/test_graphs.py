import random

from hypothesis import given, strategies as st
import graphs

smallints = st.integers(min_value=0, max_value=10)
twoints = st.tuples(smallints, smallints).filter(lambda x:x[0]>x[1])
st_edge_list = st.lists(twoints)


@given(st_edge_list)
def test_if_nodes_exist_if_edge_exists(edges):
    g = graphs.Graph()
    g.add_edges_from(edges)
    nodes = list(g.nodes())
    for node in nodes:
        assert node in g


@given(st_edge_list)
def test_neighbours(edges):
    g = graphs.Graph()
    g.add_edges_from(edges)
    for edge in edges:
        assert edge[1] in g[edge[0]] and edge[0] in g[edge[1]]


@given(st_edge_list)
def test_shortest_path(edges):
    g = graphs.Graph()
    g.add_edges_from(edges)
    nodes = list(g.nodes())
    for node in nodes:
        goal = nodes[random.randrange(len(nodes))]
        path = graphs.dijkstra(g, node)[goal]["path"]
        pathBack = graphs.dijkstra(g, goal)[node]["path"]
        if goal in path and node in pathBack:
            assert set(path) == set(pathBack)


def start_test():
    test_if_nodes_exist_if_edge_exists()
    test_neighbours()
    test_shortest_path()

if __name__ == '__main__':
    start_test()