# graphmaker.py

"""Contains functions related to graphmaking with networkx."""


import math
from collections import deque
from networkx import Graph
from generics import Point, Segments, distance
from clustering import cluster      # type: ignore


DEFAULT_N_CLUSTERS: int = 100
"""Default number of clusters to find when creating a graph."""

DEFAULT_EPSILON: int = 30
"""Default minimum angle to tolerate between the 2 edges of any node which has only two neighbours."""


def _nodes_with_coordinates(centroid_coords: list[Point]) -> list[tuple[int, dict[str, Point]]]:
    """Return a list of integers where each one has a Point related."""
    return [(i, {"point": centroid_coords[i]}) for i in range(len(centroid_coords))]


def _make_graph_from_kmeans(centroid_coords: list[Point], edges: list[tuple[int, int]]) -> Graph:
    """Make a Graph by joining the Points given, 
    where nodes are integers and each one is the index of the list of Points, where it gathers its coordinates from.
    Thus, every node has a "Point" value assigned.
    """
    g = Graph(edges)
    g.add_nodes_from(_nodes_with_coordinates(centroid_coords)) # type: ignore
    return g


def _calculate_angle(p1: Point, p2: Point, p3: Point) -> float:
    """Returns an angle in degrees given a point and its neighbors."""
    v1 = [p2.lat - p1.lat , p2.lon -p1.lon] 
    v2 = [p3.lat - p1.lat, p3.lon - p1.lon]

    dot_prod = v1[0]*v2[0] + v1[1]*v2[1]

    a = (p1.lat, p1.lon)
    b = (p2.lat, p2.lon)
    c = (p3.lat, p3.lon)

    angle = math.acos(dot_prod/(math.dist(a, b)*math.dist(a, c)))

    return angle *180 / math.pi


def _simplified_graph(G: Graph, epsilon: float) -> Graph:
    """Simplify the graph: remove nodes connecting to edges if the angle between them is lower than epsilon."""
    nodes_to_remove: set[int] = set()
    edges_to_add : set[tuple[int]] = set()
    node_q: deque[int] = deque(G.nodes)
    while node_q:
        node = node_q.popleft()
        if node in G.nodes:
            neighbors = list(G.adj[node])   # type: ignore
            if len(neighbors) == 2: # If a node more than three nodes we can't lose it. We only have to analize once each node. # type: ignore
                # If angle is less than epsilon: erase node
                angle = _calculate_angle(G.nodes[node].get("point"), G.nodes[neighbors[0]].get("point"), G.nodes[neighbors[1]].get("point"))    # type: ignore

                if angle >= 180 - epsilon:
                    nodes_to_remove.add(node)
                    edges_to_add.add((neighbors[0], neighbors[1]))  # type: ignore
                    G.remove_node(node)                             # type: ignore
                    try:
                        node_q.remove(node)
                    except ValueError:
                        pass
                    G.add_edge(neighbors[0], neighbors[1])          # type: ignore
    return G


def _weighted_edges_list(g: Graph) -> list[tuple[int, int, dict[str, float]]]:
    """Return a list in the defined format, where each tuple consists of two nodes (ints) and the distance of the edge joining them ({"distance": float})."""
    return [(n1, n2, {"distance": distance(g.nodes[n1]["point"], g.nodes[n2]["point"])}) for (n1, n2) in g.edges]     # type: ignore


def _graph_with_distances(g: Graph) -> Graph:
    """Return the same graph, having added a value "distance" to each edge, based on the haversine distance of the Points it joins."""
    g.add_edges_from(_weighted_edges_list(g))   # type: ignore
    return g


def make_graph(segments: Segments, n_clusters: int = DEFAULT_N_CLUSTERS, simplify: bool = True, epsilon: float = DEFAULT_EPSILON) -> Graph:
    """Given some Segments, execute a K-Means clustering of "n_clusters" clusters and 
    return a graph with the paths between the centroids.
    Each node has a value "Point" assigned with each coordinates.
    Each edge has a value "distance" (between the Points it joins) assigned (unit: kilometers).
    If simplify is set to True (default), nodes with 2 neighbours are erased if its edges have a "similar" angle:
        that is, if the angle between them is less than epsilon (default: 30; unit: degrees)."""
    _, centroid_coords, edges, _ = cluster(segments, n_clusters)                 # type: ignore
    g = _make_graph_from_kmeans(centroid_coords, edges)
    if simplify:
        g = _simplified_graph(g, epsilon)
    g = _graph_with_distances(g)
    return g
