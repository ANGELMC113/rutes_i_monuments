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




def _calculate_angle(p1: Point,p2: Point,p3: Point)-> float:
    '''Returns an angle in degrees given a point and its neighbors'''
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

    #angle = np.arccos((np.cross(v1,v2))/(a*b)) # [0, pi]
    angle = math.acos(prod_escalar/(math.dist(p1,p2)*math.dist(p1,p3)))

    return angle*180/math.pi


def simplify_graph(G: nx.Graph, epsilon: float) -> nx.Graph:
    """Simplify the graph."""
    nodes_to_remove = set()
    for node in G.nodes:
        neighbors = G.adj[node]
        if len(neighbors) == 2: # If a node more than three nodes we can't lose it. We only have to analize once each node then.
            # If angle less than epsilon: erase node
            angle = _calculate_angle(G.nodes[node['point']], G.nodes[neighbors[0]]['point'], G.nodes[neighbors[1]]['point'])

            if angle >= 180 - epsilon:
                nodes_to_remove.add(node)
    
    G.remove_nodes_from(nodes_to_remove)
    return G



def draw_graph(G: Graph):
    """Draw the graph, but without using any map nor coordinates.
    Only recommended for testing purposes."""
    nx.draw(G, with_labels=True, font_weight='bold')
    plt.show()
