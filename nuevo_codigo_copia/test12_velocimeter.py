# Test to try to get an approach to compute the speed of a list of given segments (directly from a downloaded datafile)


from haversine import *
from segments import *
from map_drawing import *


MAX_SPEED = 21 # meters per second


def _segment_generator2(filename: str) -> Iterator[tuple[Segment, float]]:
    """Returns a generator of all the segments inside 'filename'.
    'filename' has to be a path (already checked in other functions).
    Each Segment has its distance related."""
    file = open(filename, 'r')
    
    header = file.readline() # Ignore header,  # type: ignore

    for line in file:
        input = line.split(sep= ", ")

        p1 = (float(input[0]), float(input[1]))
        p2 = (float(input[4]), float(input[5]))

        d = haversine(p1, p2, "m")

        yield (
            Segment(start= Point(*p1), end= Point(*p1)),
            d
        )
    file.close()


def test12():
    P1 = Point(40.5363713, 0.5739316671)
    P2 = Point(40.79886535, 0.9021482)
    BOX_EBRE_FLOATS = Box(P1, P2)

    filename6 = "test_datafile5.dat"

    sm = list(_segment_generator2(filename6))

    distances: list[float] = []

    for e in sm:
        distances.append(e[1])


    print(f"Distància màxima: {max(distances)}")
    print(f"Distància mínima: {min(distances)}")
    print(f"Segments: {len(distances)} = {len(sm)}")

    
    # There don't cause problems
    MAXIMUM_SAFE_VALUE = 8 # Previous: 7
    expected_distances = [d for d in distances if 0 < d < MAXIMUM_SAFE_VALUE]
    print(f"Segments normals: {len(expected_distances)}")

    expected_sm = [e[0] for e in sm if 0 < e[1] < MAXIMUM_SAFE_VALUE]    
    mapname8 = "map11.png"
    export_png_map(mapname8, (expected_sm, []), line_color="purple")
    
    # These should not cause problems
    big_distances = [d for d in distances if MAXIMUM_SAFE_VALUE <= d < 50]
    print(f"Segments grans: {len(big_distances)}") 

    big_sm = [e[0] for e in sm if MAXIMUM_SAFE_VALUE <= e[1] < 50]    
    mapname6 = "map12.png"
    export_png_map(mapname6, (big_sm, []), line_color="red", line_width=10) 


    # These are totally unneeded:
    very_big_distances = [d for d in distances if d >= 50]
    print(f"Segments abismals: {len(very_big_distances)}")  

    very_big_sm = [e[0] for e in sm if e[1] >= 50]    
    mapname7 = "map13.png"
    export_png_map(mapname7, (very_big_sm, []), line_color="pink", line_width=10)

    




if __name__ == "__main__":
    test12()