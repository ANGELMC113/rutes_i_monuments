# Test graphmaking


import test7_wip
import map_drawing


def test8() -> None:

    G = test7_wip.test7_A()

    mapname3 = "map3.png"

    map_drawing.export_png_map(mapname3, G)

if __name__ == "__main__":
    test8()


# Effectively displays a map very similar to the one formed with segments.

# WORK IN PROGRESS