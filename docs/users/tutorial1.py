# tutorial1.py

"""
Programa per mapejar una zona al voltant de
les ciutats costeres de la comarca de la Selva.
"""

import sys

# Si hem posat el working directory a rutes_i_monuments, llavors:
PATH = "./rutes_i_monuments-package/"

sys.path.append(PATH)

from rutes_i_monuments import *


# Definim la caixa
box_costa_selva = Box(Point(41.6578, 2.7734), Point(41.7411, 2.9481))

# Veiem l'àrea definida
preview_box("output/preview-costa_selva.png", box_costa_selva)

# Generem el mapa dels camins
quick_paths("data/costa_selva", "output/mapa_costa_selva", box_costa_selva)

# Generem les rutes als monuments des d'un punt d'inici
quick_routes("data/costa_selva", "output/rutes_costa_selva", box_costa_selva, Point(41.70088, 2.83788))