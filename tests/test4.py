# Generate the map corresponding to the data of the first test case.
# Important notice: 'while page < 2' has been replaced by 'while page x < 8' to generate more data.

import segments

segments_list = segments.load_segments('test3_datafile')

segments.show_segments(segments_list, 'map.png')

# Maps looks fine and has coherent routes in it (maybe som of them not, they should be checked). We clearly see some routes go thtought the highway and state roads.