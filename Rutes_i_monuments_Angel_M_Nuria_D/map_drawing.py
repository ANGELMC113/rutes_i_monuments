# map_drawing.py

"""Contains functions related to staticmap and map drawing.
Requires internet connection to work."""


from staticmap import StaticMap, Line, CircleMarker                     # type: ignore (stub file missing)
from networkx import Graph
from simplekml import Kml                                               # type: ignore (stub file missing)
from generics import Point, Segment, Segments, check_file_extension


DEFAULT_COLORS: dict[str, str] = {
    "line": "purple",
    "marker": "orange",
    "monument": "red",
    "kml_lines": "ff0000ff" # red
}
"""Dictionary to set colors for map and KML creation."""

DEFAULT_SIZES: dict[str, int] = {
    "map_width": 1000,
    "map_height": 1000,
    "line_width": 2,
    "marker": 10,
    "monument": 15,
    "kml_lines": 5,
    "kml_height": 15
}
"""Dictionary to set parameters relating image size, line widths, marker sizes and KML line height."""


def _check_parameters(colors: dict[str, str], sizes: dict[str, int]) -> None:
    """Check that the colors and sizes dictionaries contain all required keys.
    Raises KeyError if any paramter is mssing."""
    
    required_color_keys = {"line", "marker", "monument", "kml_lines"}
    required_size_keys = {"map_width", "map_height", "line_width", "marker", "monument", "kml_lines", "kml_height"}

    missing_color_keys = required_color_keys - colors.keys()
    missing_size_keys = required_size_keys - sizes.keys()

    if missing_color_keys or missing_size_keys:
        raise KeyError(f"There are some parameters missing in the given dictionaries. \
            Check the documentation to ensure you have properly defined the parameters.")


def _map_from_segments(data: Segments | tuple[Segments, list[Point]], map: StaticMap, colors: dict[str, str], sizes: dict[str, int]) -> None:
    """Add segments and points as lines and markers respectively to the given map, using the given parameters."""
    if type(data) == list:
        segments = data
        points = []
    else:
        segments, points = data

    for seg in segments:                                                                                                        # type: ignore
        map.add_line(Line(((seg.start.lon, seg.start.lat), (seg.end.lon, seg.end.lat)), colors["line"], sizes["line_width"]))   # type: ignore
    for point in points:                                                                                                        # type: ignore
        map.add_marker(CircleMarker((point.lon, point.lat), colors["marker"], sizes["marker"]))                                 # type: ignore


def _map_from_graph(G: Graph, map: StaticMap, colors: dict[str, str], sizes: dict[str, int]) -> None:
    """Add edges and nodes from G as lines and markers respectively to the given map, using the given parameters.
    G should have a value "point" for each node
    Nodes which contain a "monuments" value will be painted differently."""

    for edge in G.edges:                                                                                                        # type: ignore
        seg = Segment(start=G.nodes[edge[0]]["point"], end=G.nodes[edge[1]]["point"])                                           # type: ignore
        map.add_line(Line(((seg.start.lon, seg.start.lat), (seg.end.lon, seg.end.lat)), colors["line"], sizes["line_width"]))   # type: ignore
    for node in G.nodes:                                                                                                        # type: ignore
        point = G.nodes[node]["point"]                                                                                          # type: ignore
        try:                                    # If there is data about monuments
            if G.nodes[node]["monuments"]:
                map.add_marker(CircleMarker((point.lon, point.lat), colors["monument"], sizes["monument"]))                     # type: ignore
        except KeyError:                        # If there is no monument
            map.add_marker(CircleMarker((point.lon, point.lat), colors["marker"], sizes["marker"]))                             # type: ignore


def export_png_map(
        filename: str,
        data: Graph | Segments | tuple[Segments, list[Point]],
        colors: dict[str, str] = DEFAULT_COLORS,
        sizes: dict[str, int] = DEFAULT_SIZES,
        feedback: bool = True
        ) -> None:
    """Export a PNG file to route 'filename' with a map formed by the given data, using staticmap.
    Be careful, if that file already exists, it gets overwritten.
    The data must be a Graph where nodes have a "point" value, a list of segments, or a tuple of lists with segments and points.
    Filename should be a path ending in .png, otherwise raises IOError.
    Internet connection is needed, otherwise raises ConnectionError.
    Check the user guide in order to establish different color and sizes."""
    check_file_extension(filename, "png")
    _check_parameters(colors, sizes)

    try:
        if feedback:
            print("Creating map.")
        map = StaticMap(sizes["map_width"], sizes["map_height"])

        specific_params = (data, map, colors, sizes)
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


def export_kml(
        filename: str, 
        G: Graph, 
        colors: dict[str, str] = DEFAULT_COLORS, 
        sizes: dict[str, int] = DEFAULT_SIZES, 
        feedback: bool = True
    ) -> None:
    """Export the graph to a KML file.
    Be careful, if there already exsits 'filename' file, it gets overwritten.
    Width is recommended to be around 5.
    Filename should be a path ending in .kml, otherwise raises IOError."""
    check_file_extension(filename, "kml")
    _check_parameters(colors, sizes)

    if feedback:
        print("Creating kml.")
    kml = Kml()
    
    for edge in G.edges:                                                                        # type: ignore
        seg = Segment(start=G.nodes[edge[0]]["point"], end=G.nodes[edge[1]]["point"])           # type: ignore
        line = kml.newlinestring(                                                               # type: ignore
            coords=[
                (seg.start.lon, seg.start.lat, sizes["kml_height"]),
                (seg.end.lon, seg.end.lat, sizes["kml_height"])
                    ]
        )
        line.style.linestyle.color = colors["kml_lines"]                                        # type: ignore
        line.style.linestyle.width = sizes["kml_lines"]                                         # type: ignore
        line.altitudemode = "relativeToGround"                                                  # type: ignore

    kml.save(filename)                                                                          # type: ignore
    if feedback:
        print(f"KML file has been successfully saved as {filename}.")
        