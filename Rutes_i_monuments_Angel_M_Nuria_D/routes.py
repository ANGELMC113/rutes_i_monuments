# routes.py

"""Contains functions related to route computing."""


from networkx import Graph, add_path, shortest_path, NetworkXNoPath     # type: ignore
from generics import Point, Box, distance
from monuments import Monuments, get_monuments



def _filter_monuments(box: Box) -> Monuments:
    """Get the list of monuments contained in this box."""
    return [
        mon for mon in get_monuments() if (
            box.bottom_left.lat < mon.location.lat < box.top_right.lat
            and
            box.bottom_left.lon < mon.location.lon < box.top_right.lon
        )
    ]


def _approximate_point_to_node(G: Graph, point: Point) -> int:
    """Return the closest node inside the Graph to the given Point, based on node's Point value."""
    
    distances_to_point: list[float] = {i: distance(point, G.nodes[i]["point"]) for i in G.nodes}    # type: ignore
    
    return min(distances_to_point, key=distances_to_point.get)                                      # type: ignore


def _approximate_and_add_monuments_to_nodes(G: Graph, endpoints: Monuments) -> dict[int, list[str]]:
    """Return a dictionary of the nodes which now correspond to a Monument. Its value is a list of the names of the Monuments it holds."""
    
    nodes_with_monuments: dict[int, list[str]] = {}
    for endpoint in endpoints:
        closest_node = _approximate_point_to_node(G, endpoint.location)
        if closest_node not in nodes_with_monuments:
            nodes_with_monuments[closest_node] = [endpoint.name]
        else:
            nodes_with_monuments[closest_node].append(endpoint.name)
    return nodes_with_monuments


def _find_shortest_paths(G: Graph, source: int, targets: list[int], feedback: bool = True) -> list[list[int]]:
    """Given a graph whose edges hava a distance related, a source node, and a list of targets nodes,
    return the list of the minimal paths to get from the source to each target."""
    
    shortest_paths: list[list[int]] = []
    for node in targets:
        try:
            path = shortest_path(G, source, node, "distance") # type: ignore
            shortest_paths.append(path) # type: ignore
        except NetworkXNoPath:
            if feedback:
                print(f"No path found from the starting node to node {node}. Some monuments are not reachable.")
    return shortest_paths
   

def _create_tree(G: Graph, start: Point, endpoints: Monuments, feedback: bool = True) -> Graph:
    """Create a tree with the minimal distance paths from start Point to each Monument in endpoints.
    This tree will have a value "point" for every node with its coordinates, 
        and each leaf will have a value "monuments" with the list of its contained monuments' names."""

    nodes_with_monuments = _approximate_and_add_monuments_to_nodes(G, endpoints)

    if len(nodes_with_monuments) == 0:
        raise ValueError("There seem no be no monuments inside this Box. Program has stopped.")

    shortest_paths = _find_shortest_paths(
        G,
        _approximate_point_to_node(G, start),
        nodes_with_monuments.keys(),             # type: ignore
        feedback
    )

    T = Graph()
    for path in shortest_paths:
        add_path(T, path)
    
    T.add_nodes_from([(node, {"point":  G.nodes[node]["point"]}) for node in G.nodes() if node in T.nodes])                            # type: ignore
    T.add_nodes_from([(node, {"monuments": nodes_with_monuments[node]}) for node in nodes_with_monuments.keys() if node in T.nodes])   # type: ignore

    return T


def find_routes(G: Graph, box: Box, start: Point, feedback: bool = True) -> Graph:
    """Find the shortest route between the starting point and all the endpoints contained in this Box."""
    monuments_in_box = _filter_monuments(box)
    if feedback:
        print(f"There are {len(monuments_in_box)} in this box.")
        print(f"These are the monuments and their locations (in latitude - longitude format):")
        for monument in monuments_in_box:
              print(f"{monument.name} ({monument.sublcass}) at {monument.location.lat}, {monument.location.lon}")
            
        print("Creating the tree.")
    T = (_create_tree(G, start, monuments_in_box, feedback))
    if feedback:
        print("These are the nodes which contain the reachable monuments:")
        for node in T.nodes: # type: ignore
            try:
                if T.nodes[node]["monuments"]:
                    print(f"Node at {T.nodes[node]['point'].lat}, {T.nodes[node]['point'].lon} contains monuments: {T.nodes[node]['monuments']}" )  # type: ignore
            except KeyError:
                pass
    return T
    