# Make segments.py load 2 different lists of segments.
# Notice that test2_datafile should already exist, but test3_datafile should not exist at the beginning of this test

import segments

P1 = segments.Point(40.5363713, 0.5739316671)
P2 = segments.Point(40.79886535, 0.9021482)

BOX_EBRE_FLOATS = segments.Box(P1, P2)
filename2 = "test2_datafile"
filename3 = "test3_datafile"

print(segments.get_segments(BOX_EBRE_FLOATS, filename2))
print(segments.get_segments(BOX_EBRE_FLOATS, filename3))

# Function behaves properly. Downloads if necessary (file not eaxisting) and shows the data correctly.