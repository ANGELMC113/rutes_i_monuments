# graphmaker.py

'''Contains functions related to graphmaking with networkx.'''


from segments import *
import networkx as nx
from networkx import Graph
import haversine
import matplotlib.pyplot as plt



def _edge_add_distance(edge: tuple[int, int], segment: Segment) -> tuple[int, int, dict[str, float]]:
    """Adds a dictionary to the edge which tells the haversine distance between its joined nodes."""
    distance = haversine.haversine(
        (segment.start.lat,
        segment.start.lon),
        (segment.end.lat,
        segment.end.lon)
    )
    return (edge[0], edge[1], {"distance": distance})
    

def _calculate_distances(edges: list[tuple[int, int]], segments: Segments) -> list[tuple[int, int, dict[str, float]]]:
    """Return the same list of tuples having added a dictionary in each edge, telling it's haversine distance between nodes."""
    weighted_edges: list[tuple[int, int, dict[str, float]]] = []
    for i in range(len(edges)):
        weighted_edges.append(_edge_add_distance(edges[i], segments[i]))
    return weighted_edges


def _nodes_with_coordinates(centroid_coords: list[Point]) -> list[tuple[int, dict[str, Point]]]:
    """Return a list of integers where each one has a Point related."""
    return [(i, {"point": centroid_coords[i]}) for i in range(len(centroid_coords))]


def make_graph(centroid_labels: "tuple[ndarray[int]", centroid_coords: list[Point], edges: list[tuple[int, int]], segments: Segments) -> Graph:
    """Make a graph from the segments."""
    G = Graph(_calculate_distances(edges, segments))
    G.add_nodes_from(_nodes_with_coordinates(centroid_coords)) # type: ignore
    return G


def simplify_graph(G: Graph, epsilon: float) -> Graph:
    """Simplify the graph."""
    # si un node té més de 2 arestes, no n'en pot perdre. Per tant, només ens cal analitzar cada node un cop.
    for node in G.nodes:
        if len(G.neighbors(node)) == 2:
            # Try to erase node
            # If angle less than epsilon: erase node
            # Angle is computed: 
            ...


def draw_graph(G: Graph):
    """Draw the graph, but without using any map nor coordinates.
    Only recommended for testing purposes."""
    nx.draw(G, with_labels=True, font_weight='bold')
    plt.show()