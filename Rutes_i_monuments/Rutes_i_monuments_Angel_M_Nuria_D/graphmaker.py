# graphmaker.py

'''Contains functions related to graphmaking with networkx.'''


from segments import *
import networkx as nx
from networkx import Graph

import clustering


def cluster_2(segments: Segments, n_clusters: int) -> "tuple[ndarray[int], list[Point], list[tuple[int, int]]]":
    '''Like cluster in clustering.py, but returns the edges we need to make a graph.'''
    centroid_labels, centroid_coords = clustering._kmeans_centroids(segments, n_clusters)
    new_edges: Segments = []
    i = 0
    for _ in segments:
        if True: # We will remove this check after some testing is done
            if centroid_labels[i] != centroid_labels[i + 1]: # If segments joins different cluster
                new_edge = (centroid_labels[i], centroid_labels[i + 1])
                if new_edge not in new_edges:
                    new_edges.append(new_edge)
            i += 2
        #except:
            #print('failed')
    return centroid_labels, centroid_coords, new_edges


def make_graph(centroid_labels, centroid_coords, edges) -> Graph:
    """Make a graph from the segments."""
    G = Graph(edges)
    # Add Point value to each node
    return G


def simplify_graph(graph: Graph, epsilon: float) -> Graph:
    """Simplify the graph."""

    




import matplotlib.pyplot as plt


def draw_graph(G: Graph):
    nx.draw(G, with_labels=True, font_weight='bold')
    plt.show()