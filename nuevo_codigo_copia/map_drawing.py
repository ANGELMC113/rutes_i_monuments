# mapdrawing.py

'''Contains functions related to staticmap and map drawing.
Requires internet connection to work.'''


from staticmap import StaticMap, Line, CircleMarker     # type: ignore (stub file missing)
from networkx import Graph
from simplekml import Kml                               # type: ignore (stub file missing)
from generics import *
from segments import *



def _map_from_segments(data: Segments | tuple[Segments, list[Point]], map: StaticMap, line_color: str, marker_color: str, line_width: int, marker_width: int) -> None:
    """Add segments and points as lines and markers respectively to the given map, using the given parameters."""
    if type(data) == list:
        segments = data
        points = []
    else:
        segments, points = data

    for seg in segments:                                                                                            # type: ignore
        map.add_line(Line(((seg.start.lon, seg.start.lat), (seg.end.lon, seg.end.lat)), line_color, line_width))    # type: ignore
    for point in points:                                                                                            # type: ignore
        map.add_marker(CircleMarker((point.lon, point.lat), marker_color, marker_width))                            # type: ignore


def _map_from_graph(G: Graph, map: StaticMap, line_color: str, marker_color: str, line_width: int, marker_width: int) -> None:
    """Add edges and nodes from G as lines and markers respectively to the given map, using the given parameters.
    G should have a value 'point' for each node."""
    for edge in G.edges:                                                                                            # type: ignore
        seg = Segment(start=G.nodes[edge[0]]['point'], end=G.nodes[edge[1]]['point'])                               # type: ignore
        map.add_line(Line(((seg.start.lon, seg.start.lat), (seg.end.lon, seg.end.lat)), line_color, line_width))    # type: ignore
    for node in G.nodes:                                                                                            # type: ignore
        point = G.nodes[node]['point']                                                                              # type: ignore
        map.add_marker(CircleMarker((point.lon, point.lat), marker_color, marker_width))                            # type: ignore


def export_png_map(
        filename: str,
        data: Graph | Segments | tuple[Segments, list[Point]],
        image_width: int = 1000,
        image_height: int = 1000,        
        line_color: str = 'purple',
        marker_color: str = 'orange',
        line_width: int = 2,
        marker_width: int = 10,
        feedback: bool = True
        ) -> None:
    """Export a PNG file to route 'filename' with a map formed by the given data, using staticmap.
    Be careful, if that file already exists, it gets overwritten.
    The data must be a Graph where nodes have a 'point' value, a list of segments, or a tuple if lists with segments and points.
    Color parameters should be a standard color.
    Line and marker width's are recommended to be between 1 and 10.
    Image size should be between 500 and 5000.
    Filename should be a path ending in .png, otherwise raises IOError.
    Internet connection is needed, otherwise raises ConnectionError."""
    check_file_extension(filename, ".png")

    try:
        if feedback:
            print("Creating map.")
        map = StaticMap(image_width, image_height)

        specific_params = (data, map, line_color, marker_color, line_width, marker_width)
        if type(data) == Graph:
            _map_from_graph(*specific_params)           # type: ignore
        else:
            _map_from_segments(*specific_params)        # type: ignore

        if feedback:
            print("Rendering map.")
        image = map.render()                            # type: ignore

    except RuntimeError:
        raise ConnectionError("Connection error. Check internet connection and try again. If error persists, the server where the data is gathered from may be offline, try waiting a few hours.")

    image.save(filename)
    if feedback:
        print(f"Map has been succesfully saved as {filename}.")


def export_kml(filename: str, G: Graph, width: int = 5, feedback: bool = True) -> None:
    """Export the graph to a KML file.
    Be careful, if there already exsits 'filename' file, it gets overwritten.
    Width is recommended to be around 5.
    Filename should be a path ending in .kml, otherwise raises IOError."""
    check_file_extension(filename, ".kml")
    if feedback:
        print("Creating kml.")
    kml = Kml()
    
    for edge in G.edges:                                                                        # type: ignore
        seg = Segment(start=G.nodes[edge[0]]['point'], end=G.nodes[edge[1]]['point'])           # type: ignore
        line = kml.newlinestring(                                                               # type: ignore
            coords=[
                (seg.start.lon, seg.start.lat),
                (seg.end.lon, seg.end.lat)
                    ]
        )
        line.style.linestyle.color = "ff0000ff"  # Red                                          # type: ignore
        line.style.linestyle.width = width                                                      # type: ignore

    kml.save(filename)                                                                          # type: ignore
    if feedback:
        print(f"Kml file has been successfully saved as {filename}.")
