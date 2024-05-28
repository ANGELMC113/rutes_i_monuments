# graphmaker.py

"""Contains functions related to graphmaking with networkx."""


import math
from segments import *
from networkx import Graph
import haversine                    # type: ignore (stub file missing)
from clustering import cluster      # type: ignore
from collections import deque



def _edge_add_distance(edge: tuple[int, int], segment: Segment) -> tuple[int, int, dict[str, float]]:
    """Adds a dictionary to the edge which tells the haversine distance between its joined nodes, in kilometers."""
    distance = haversine.haversine(     # type: ignore
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


def _make_graph_from_kmeans(centroid_coords: list[Point], edges: list[tuple[int, int]], segments: Segments) -> Graph:
    """Make a graph from the segments."""
    g = Graph(edges)
    g.add_nodes_from(_nodes_with_coordinates(centroid_coords)) # type: ignore
    return g


def _calculate_angle(p1: Point, p2: Point, p3: Point) -> float:
    """Returns an angle in degrees given a point and its neighbors."""
    """
    c1 = np.array([p1.lat, p1.lon]) #node
    c2 = np.array([p2.lat, p2.lon]) # nbor1
    c3 = np.array([p3.lat, p3.lon]) # nbor2
    """
    v1 = [p2.lat - p1.lat , p2.lon -p1.lon] 
    v2 = [p3.lat - p1.lat, p3.lon - p1.lon]

    #a = np.linalg.norm(v1)
    #b = np.linalg.norm(v2)
    prod_escalar = v1[0]*v2[0] + v1[1]*v2[1]

    a = (p1.lat, p1.lon)
    b = (p2.lat, p2.lon)
    c = (p3.lat, p3.lon)

    #angle = np.arccos((np.cross(v1,v2))/(a*b)) # [0, pi]
    angle = math.acos(prod_escalar/(math.dist(a, b)*math.dist(a, c)))

    return angle*180/math.pi


def _simplify_graph(G: Graph, epsilon: float) -> Graph:
    """Simplify the graph: remove nodes connecting to edges if the angle between them is lower than epsilon."""
    nodes_to_remove: set[int] = set()
    edges_to_add : set[tuple[int]] = set()
    node_q: deque[int] = deque(G.nodes)
    while node_q:
        node = node_q.popleft()
        if node in G.nodes:
            neighbors = list(G.adj[node])
            if len(neighbors) == 2: # If a node more than three nodes we can't lose it. We only have to analize once each node.
                # If angle less than epsilon: erase node
                angle = _calculate_angle(G.nodes[node].get('point'), G.nodes[neighbors[0]].get('point'), G.nodes[neighbors[1]].get('point'))

                if angle >= 180 - epsilon:
                    nodes_to_remove.add(node)
                    edges_to_add.add((neighbors[0], neighbors[1]))
                    G.remove_node(node)
                    try:
                        node_q.remove(node)
                    except ValueError:
                        pass
                    G.add_edge(neighbors[0], neighbors[1])
            
    
    #G.remove_nodes_from(nodes_to_remove)
    #G.add_edges_from(edges_to_add)
    print("Nodos eliminados:", nodes_to_remove)
    print("Arestas puestas:", edges_to_add)

    return G


def make_graph(segments: Segments, n_clusters: int = 100) -> Graph:
    """Given some Segments, execute a K-Means clustering of "n_clusters" clusters and 
    return a graph with the simplified paths between the centroids.
    Each node has a value "Point" assigned with each coordinates.
    Each edge has a value "distance" (between the Points it joins) assigned (unit: kilometers)."""
    _, centroid_coords, edges, new_segments = cluster(segments, n_clusters)                 # type: ignore
    g = _make_graph_from_kmeans(centroid_coords, edges, new_segments)
    g = _simplify_graph(g, 40)
    return g
