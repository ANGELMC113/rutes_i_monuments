# tutorial1.py

""" 
Programa per mapejar una zona al voltant de 
les ciutats costeres de la comarca de la Selva.
"""

from rutes_i_monuments import *

box_costa_selva = Box(Point(41.6578, 2.7734), Point(41.7411, 2.9481))

preview_box("preview-costa_selva.png", box_costa_selva)

quick_paths("costa_selva", box_costa_selva)
