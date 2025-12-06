# tutorial3.py

"""
Programa per mapejar una zona al voltant de Tossa de Mar,
personalitzant alguns aspectes dels mapes.
"""

import sys

# Si hem posat el working directory a rutes_i_monuments, llavors:
PATH = "./rutes_i_monuments-package/"

sys.path.append(PATH)

from rutes_i_monuments import *

# Definim la caixa i els segments
box_tossa = Box(Point(41.7128, 2.9159), Point(41.7300, 2.9416))
segments_tossa = get_segments("data/tossa.dat", box_tossa)

# Definim un graf personalitzat
graf_tossa = make_graph(segments_tossa, n_clusters=300, simplify=False)

# Definim paràmetres personalitzats
colors: dict[str, str] = {
    "line": "blue",
    "marker": "blue",
    "monument": "purple",
    "kml_lines": "ff006400" # darkgreen
}

sizes: dict[str, int] = {
    "map_width": 1500,
    "map_height": 1500,
    "line_width": 5,
    "marker": 5,
    "monument": 20,
    "kml_lines": 10,
    "kml_height": 5
}

# Veiem el mapa del graf
export_png_map("output/graf_personalitzat_tossa.png", graf_tossa, colors, sizes)

# Reduïm el mapa a les rutes a monuments, des d'un punt donat a prop de la platja de Tossa
routes_tossa = find_routes(graf_tossa, box_tossa, (Point(41.7202, 2.9335)))

# Visualitzem les rutes
export_png_map("output/rutes_personalitzat_tossa.png", routes_tossa, colors, sizes)

# Generem l'arxiu KML de les rutes per portar a Google Earth
export_kml("output/rutes_personalitzat_tossa.kml", routes_tossa, colors, sizes)