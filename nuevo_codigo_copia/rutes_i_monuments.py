# rutes_i_monuments.py

"""Gathers all modules to allow the client access to every needed functionality.
Documentation from all modules is avaliable at the README.md."""


from segments import Point, Segment, Segments, Box, get_segments, read_data_header      # type: ignore
from map_drawing import export_png_map, export_kml
from graphmaker import Graph, make_graph
from routes import find_routes


DEFAULT_FEEDBACK: bool = True
"""Establish the default feedback for all functionalities which use it.
Feedback consist on messages being printed on the command prompt when some processes are completed."""


def preview_box(filename: str, box: Box, feedback: bool = DEFAULT_FEEDBACK) -> None:
    """Export file "filename" with a map of the rectangle defined in the given Box.
    "filename" must be a path ending in .png."""
    lat_0 = box.bottom_left.lat
    lon_0 = box.bottom_left.lon
    lat_1 = box.top_right.lat
    lon_1 = box.top_right.lon
    sides: Segments = [
        Segment(box.bottom_left, Point(lat_1, lon_0)),
        Segment(box.bottom_left, Point(lat_0, lon_1)),
        Segment(Point(lat_1, lon_0), box.top_right),
        Segment(Point(lat_0, lon_1), box.top_right)
    ]
    export_png_map(filename, (sides, []), feedback=feedback)


def quick_graph(filename: str, box: Box, n_clusters: int = 100, feedback: bool = DEFAULT_FEEDBACK) -> Graph:
    """Automatically get the segments needed, execute a clustering of "n_clusters" and return a Graph from it."""
    segments = get_segments(filename+".dat", box, feedback=feedback)
    G = make_graph(segments, n_clusters)
    return G


def quick_paths(filename: str, box: Box, n_clusters: int = 100, feedback: bool = DEFAULT_FEEDBACK) -> None:
    """Automatically get the data needed and generate a map and a kml with the simplified paths available.
    This includes executing the clustering (of given "n_clusters" number of clusters) and making the graph.
    "filename" should not have any extension: it should be plain text."""
    G = quick_graph(filename, box, n_clusters, feedback)
    export_png_map((filename+".png"), G)
    export_kml((filename+".kml"), G)

'''
def quick_routes(filename: str, box: Box, start: Point, n_clusters: int = 100, feedback: bool = DEFAULT_FEEDBACK) -> None:
    """Automatically get the data needed and generate a map and a kml with the routes to each monument.
    This includes executing the clustering (of given "n_clusters" number of clusters) and making the graph.
    "filename" should not have any extension: it should be plain text."""
    G = find_routes(quick_graph(filename, box, n_clusters, feedback=feedback), box, start)
    export_png_map((filename+".png"), G)
    export_kml((filename+".kml"), G)
'''