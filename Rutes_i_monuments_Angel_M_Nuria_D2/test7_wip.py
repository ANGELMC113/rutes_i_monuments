# Test graphmaking


import test5
import clustering
import graphmaker


def test7_A() -> graphmaker.Graph:

    segments = test5.test5()

    centroid_labels, centroid_coords, edges, new_segments = clustering.cluster(segments, 100)

    G = graphmaker.make_graph(centroid_labels, centroid_coords, edges, new_segments)

    print(G)                # Output: Graph with 100 nodes and 220 edges
    print(G.edges)          # Prints a list[tuple[int, int]]
    print(G.nodes.data())   # Prints a list[tuple[int, dict['Point': Point]]]
    print(G.edges.data())   # Prints a list[tuple[int, int, dict['distance': float]]]

    return G


def test7_B(G: graphmaker.Graph):
    graphmaker.draw_graph(G)


if __name__ == "__main__":
    G = test7_A()
    test7_B(G)


# Properly forms and displays a graph.

# WORK IN PROGRESS