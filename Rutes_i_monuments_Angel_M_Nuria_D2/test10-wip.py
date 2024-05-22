# Full testing in one shot: map Barcelona airport surroundings.


from segments import *
from map_drawing import *
from clustering import *
from graphmaker import *
from time import time


def test10() -> None:

    times: dict[str, float] = {}
    time_start = time()

    P1 = Point(41.1030, 1.5702)
    P2 = Point(41.3319, 2.21)
    BARCELONA_FLOATS = Box(P1, P2)

    datafile_name = "datafile_bcn"
    map_name1 = "map_raw_bcn.png"
    map_name2 = "map_clustered_bcn.png"
    map_name3 = "map_graph_bcn.png"
    kml_name1 = "map_kml_bcn.kml"

    segments = get_segments(BARCELONA_FLOATS, datafile_name)

    times["Getting segments"] = time() - time_start

    export_png_map(map_name1, (segments, []), 10000, 10000)

    times["Map raw segments"] = time() - time_start - times["Getting segments"]

    centroid_labels, centroid_coords, edges, new_segments = cluster(segments, 500)

    times["Clustering"] = time() - time_start - times["Map raw segments"]

    export_png_map(map_name2, (new_segments, centroid_coords), 10000, 10000)

    times["Map clustered"] = time() - time_start - times["Clustering"]

    G = make_graph(centroid_labels, centroid_coords, edges, new_segments)

    times["Making graph"] = time() - time_start - times["Map clustered"]

    export_png_map(map_name3, G, 10000, 10000)

    times["Map graph"] = time() - time_start - times["Making graph"]

    export_kml(kml_name1, G)

    times["Making kml"] = time() - time_start - times["Map graph"]

    time_end = time()

    times["Total time in seconds"] = time_end - time_start
    times["Total time in minutes"] = (time_end - time_start) / 60

    print(times)


if __name__ == "__main__":
    test10()


# Total execution may last around ten minutes. Map 1 should be simplified in map 2, similar to map 3.


""" Output: (clearly wrong!)
{'Getting segments': 1409.2220623493195, 
'Map raw segments': 1715974833.424306, 
'Clustering': 1460.132640361786, 
'Map clustered': 1715974835.4103096, 
'Making graph': 1460.1386404037476, 
'Map graph': 1715974837.3453093, 
'Making kml': 1460.4176449775696, 
'Total time in seconds': 1477.6006457805634, 
'Total time in minutes': 24.626677429676057}
(271 pages downloaded)
"""