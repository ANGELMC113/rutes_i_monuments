# routes.py

"""Contains functions related to route computing."""


from networkx import Graph, add_path, shortest_path
from haversine import haversine
from segments import Point, Box
from monuments import Monument, Monuments


MONUMENTS_FILE = "monuments.dat"


def _filter_monuments(box: Box) -> Monuments:
    """Get the list of monuments contained in this box."""
    ...
    # Call monuments to load monuments (use MONUMENTS_FILE global)

    # Simply analyze all monuments donwloaded and see if they are inside the list

    # Parameter filename has been erased as it will always be the same. We will have to decide wther the user can or not download monuments.

    # WHAT WILL HAPPEN IF WE TRY TO DOWNLOAD SEGMENTS TO monuments.dat  ?!?!?!?





def _approximate_point_to_centroid(G: Graph, point: Point) -> int:
    """Return the closest node inside the Graph to the given Point, based on node's Point value."""
    p1: tuple[float, float] = (point.lat, point.lon)
    
    distances_to_point: list[float] = [haversine(p1, (G.nodes[i]["point"].lat, G.nodes[i]["point"].lon)) for i in range(len(G))]    # type: ignore
    
    return  distances_to_point.index(min(distances_to_point))


def _find_shortest_paths(G: Graph, source: int, targets: list[int]) -> list[list[int]]:
    """Given a graph whose edges hava a distance related, a source node, and a list of targets nodes,
    return the list of the minimal paths to get from the source to each target."""

    return [shortest_path(G, source, node, "distance") for node in targets]     # type: ignore


def _create_tree(G: Graph, start: Point, endpoints: Monuments) -> Graph:
    """Create a tree with the minimal distance paths from start Point to each Monument in endpoints."""

    shortest_paths = _find_shortest_paths(
        G,
        _approximate_point_to_centroid(G, start),
        [_approximate_point_to_centroid(G, endpoint.location) for endpoint in endpoints]
    )

    T = Graph()
    for path in shortest_paths:
        add_path(T, path)
    
    T.add_nodes_from([(node, {"point":  G.nodes[node]["point"]}) for node in G.nodes() if node in T.nodes])     # type: ignore

    return T


def find_routes(G: Graph, box: Box, start: Point) -> Graph:
    """Find the shortest route between the starting point and all the endpoints contained in this Box."""
    return (_create_tree(G, start, _filter_monuments(box)))
