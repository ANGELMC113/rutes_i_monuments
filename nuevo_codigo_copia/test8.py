# Test graphmaking


import test7
import map_drawing


def test8() -> None:

    G = test7.test7()

    mapname4 = "map4.png"

    map_drawing.export_png_map(mapname4, G)

if __name__ == "__main__":
    test8()


# Effectively displays a map very similar to the one formed with segments.

# WORK IN PROGRESS