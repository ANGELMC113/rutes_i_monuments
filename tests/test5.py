# Generate the map corresponding to the data of the first test case.
# Important notice: 'while page < 8' has been replaced by 'while True' to generate more data.

import segments

P1 = segments.Point(40.5363713, 0.5739316671)
P2 = segments.Point(40.79886535, 0.9021482)

BOX_EBRE_FLOATS = segments.Box(P1, P2)

segments_list = segments.get_segments(BOX_EBRE_FLOATS, 'test5_datafile')

segments.show_segments(segments_list, 'map.png')

# Maps looks fine and has coherent routes in it (maybe som of them not, they should be checked). We clearly see some routes go thtought the highway and state roads.