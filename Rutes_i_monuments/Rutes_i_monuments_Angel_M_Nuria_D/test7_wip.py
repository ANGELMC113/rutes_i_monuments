# Test graphmaking


import test5
import clustering
import graphmaker


def test7() -> None:

    segments = test5.test5()

    centroid_labels, centroid_coords, edges = graphmaker.cluster_2(segments, 100)

    G = graphmaker.make_graph(centroid_labels, centroid_coords, edges)

    print(G)
    print(G.edges)

    graphmaker.draw_graph(G)

if __name__ == "__main__":
    test7()


# RN Properly forms and displays a graph.

# WORK IN PROGRESS