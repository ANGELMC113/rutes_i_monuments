# Test map_drawing.map_from_segments(). Download a bigger data package and use it to generate the map corresponding to it's data.


import segments
import map_drawing

def test4() -> None:

    P1 = segments.Point(40.5363713, 0.5739316671)
    P2 = segments.Point(40.79886535, 0.9021482)
    BOX_EBRE_FLOATS = segments.Box(P1, P2)

    filename4 = "test4_datafile"
    mapname1 = "map1.png"

    segments.get_segments(BOX_EBRE_FLOATS, filename4, 8, True)

    segments_list = segments.load_segments(filename4)
    map_drawing.map_from_segments(mapname1, segments_list)

if __name__ == "__main__":
    test4()


# Maps looks fine and has coherent routes in it (although some seem like are crossing lakes or are straight lines).
    # We clearly see some routes go along the highway and state roads.