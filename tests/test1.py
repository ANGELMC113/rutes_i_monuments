# Short test case to donwload and save the data in a file using segments.donwload_segments()
# Both outputs' data should be equal (the second one is used for test3.py)
# Important note: 'while True' was replaced by 'while page < 2' to execute these tests (from 1 to 4), in order to make the tetsting quicker.

import segments

P1 = segments.Point(40.5363713, 0.5739316671)
P2 = segments.Point(40.79886535, 0.9021482)

BOX_EBRE_FLOATS = segments.Box(P1, P2)
filename1 = "test1_datafile"
filename2 = "test2_datafile"

segments.download_segments(BOX_EBRE_FLOATS, filename1)
segments.download_segments(BOX_EBRE_FLOATS, filename2)

# We correcly download the data and place in a text file. Both files are equal.