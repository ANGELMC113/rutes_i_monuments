# mapdrawing.py

'''Contains functions related to staticmap and map drawing.
Requires internet connection to work.'''


from staticmap import StaticMap, Line, CircleMarker
from networkx import Graph
from segments import *


def map_from_segments(filename: str, segments: Segments = [], points: list[Point] = [], line_color: str = 'purple', line_width: int = 2, marker_color: str = 'orange', marker_width: int = 10) -> None:
    """Show all segments and points (if any are given in the lists) in a PNG file using staticmap.
    Color parameters should be a standard color.
    Width are recommended to be between 1 and 10."""
    map = StaticMap(800, 800)
    for seg in segments:
        map.add_line(Line(((seg.start.lon, seg.start.lat), (seg.end.lon, seg.end.lat)), line_color, line_width)) # type: ignore
    for point in points:
        map.add_marker(CircleMarker((point.lon, point.lat), marker_color, marker_width)) # type: ignore
    
    image = map.render() # type: ignore
    image.save(filename)


def map_from_graph(filename: str, G: Graph, line_color: str = 'purple', line_width: int = 2, marker_color: str = 'orange', marker_width: int = 10) -> None:
    """Given a graph where nodes have a Point value, display it in a PNG file using staticmap.
    Color parameters should be a standard color.
    Width are recommended to be between 1 and 10."""
    map = StaticMap(800, 800)
    for seg in segments:
        map.add_line(Line(((seg.start.lon, seg.start.lat), (seg.end.lon, seg.end.lat)), line_color, line_width)) # type: ignore
    for point in points:
        map.add_marker(CircleMarker((point.lon, point.lat), marker_color, marker_width)) # type: ignore