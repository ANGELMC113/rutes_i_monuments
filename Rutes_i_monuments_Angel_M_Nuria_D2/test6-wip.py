# Test clustering.cluster using test5 generated file.


import test5
import clustering
import map_drawing


def test6() -> None:

    segments = test5.test5()

    centroid_labels, centroid_coords, edges, new_segments = clustering.cluster(segments, 100)

    print(centroid_labels)          # should be an array of numbers (between 0 and 99)
    print(centroid_coords)          # should be a list of (100) points
    print(max(centroid_labels))     # should be 99
    print(min(centroid_labels))     # should be 0
    print(len(centroid_coords))     # should be 100

    mapname2 = "map2.png"

    map_drawing.export_png_map(mapname2, (new_segments, centroid_coords))


if __name__ == "__main__":
    test6()


# Effectively displays the array, the list, and the integers asked for. The predictions were correct.
# The map is properly generated and we can see there are points joined by segments.
    # Some segments seem to cross over water bodies (through impossible places, where there's no bridge), but this is not easy to fix, neither is a problematic error.