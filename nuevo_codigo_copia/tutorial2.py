# tutorial1.py

""" 
Programa per mapejar una zona al voltant de Tossa de Mar,
tot personalitzant paràmetres.
"""

from rutes_i_monuments import *

box_tossa = Box(Point(41.7128, 2.9159), Point(41.7300, 2.9416))
"""
preview_box("preview-tossa.png", box_tossa)
"""
segments_tossa = get_segments("tossa.dat", box_tossa)
"""
export_png_map("segments_tossa.png", segments_tossa)
"""
graf_tossa = make_graph(segments_tossa)

print(graf_tossa.nodes.data())

export_png_map("graf_tossa.png", graf_tossa)
