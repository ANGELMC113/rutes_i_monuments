# Try to find a way to filter long segments


import segments
import map_drawing

def test1() -> None:

    P1 = segments.Point(40.5363713, 0.5739316671)
    P2 = segments.Point(40.79886535, 0.9021482)
    BOX_EBRE_FLOATS = segments.Box(P1, P2)

    filename6 = "test_datafile6.dat"
    mapname5 = "map5.png"

    sm = segments.get_segments(filename6, BOX_EBRE_FLOATS, 1)
    map_drawing.export_png_map(mapname5, (sm, []))


if __name__ == "__main__":
    test1()


# First execution: page 0: no straight lines found
    # "test_datafile6.txt" has been modified to download only page 1
    # How? Simply erase segments from the datafile anc change True to False and 0 to 1 in the "test_datafile.6.txt"