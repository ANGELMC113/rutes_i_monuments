# mapdrawing.py

'''Contains functions related to staticmap and map drawing.
Requires internet connection to work.'''


from staticmap import StaticMap, Line, CircleMarker
from networkx import Graph
from simplekml import Kml
from generics import *
from segments import *



def _map_from_segments(data: tuple[Segments, list[Point]], map: StaticMap, line_color: str, marker_color: str, line_width: int, marker_width: int) -> None:
    """Add segments and points as lines and markers respectively to the given map, using the given parameters."""
    segments, points = data
    for seg in segments:
        map.add_line(Line(((seg.start.lon, seg.start.lat), (seg.end.lon, seg.end.lat)), line_color, line_width)) # type: ignore
    for point in points:
        map.add_marker(CircleMarker((point.lon, point.lat), marker_color, marker_width)) # type: ignore



def _map_from_graph(G: Graph, map: StaticMap, line_color: str, marker_color: str, line_width: int, marker_width: int) -> None:
    """Add edges and nodes from G as lines and markers respectively to the given map, using the given parameters.
    G should have a value 'point' for each node."""
    for edge in G.edges:
        seg = Segment(start=G.nodes[edge[0]]['point'], end=G.nodes[edge[1]]['point'])
        map.add_line(Line(((seg.start.lon, seg.start.lat), (seg.end.lon, seg.end.lat)), line_color, line_width)) # type: ignore
    for node in G.nodes:
        point = G.nodes[node]['point']
        map.add_marker(CircleMarker((point.lon, point.lat), marker_color, marker_width)) # type: ignore



def export_png_map(
        filename: str,
        data: Graph | tuple[Segments, list[Point]],
        image_width: int = 1000,
        image_height: int = 1000,        
        line_color: str = 'purple',
        marker_color: str = 'orange',
        line_width: int = 2,
        marker_width: int = 10
        ) -> None:
    """Export a PNG file to route 'filename' with a map formed by the given data, using staticmap.
    The data must be a Graph where nodes have a 'point' value, or a tuple if lists with segments and points.
    Color parameters should be a standard color.
    Line and marker width's are recommended to be between 1 and 10.
    Image size should be between 500 and 5000."""

    check_file_extension(filename, ".png")

    map = StaticMap(image_width, image_height)

    specific_params = (data, map, line_color, marker_color, line_width, marker_width)
    if len(data) == 1:
        _map_from_graph(*specific_params)      # type: ignore
    else:
        _map_from_segments(*specific_params)   # type: ignore

    image = map.render() # type: ignore

    image.save(filename)
    


def export_kml(filename: str, G: Graph, width: int = 5) -> None:
    """Export the graph to a KML file.
    Width is recommended to be around 5."""
    
    check_file_extension(filename, ".kml")
    
    kml = Kml()
    
    for edge in G.edges:
        seg = Segment(start=G.nodes[edge[0]]['point'], end=G.nodes[edge[1]]['point'])
        line = kml.newlinestring(
            coords=[
                (seg.start.lon, seg.start.lat),
                (seg.end.lon, seg.end.lat)
                    ]
        )
        line.style.linestyle.color = "ff0000ff"  # Red
        line.style.linestyle.width = width

    kml.save(filename)