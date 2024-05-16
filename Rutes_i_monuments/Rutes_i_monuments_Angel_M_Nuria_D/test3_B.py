# Test segments.get_segments() function.
# We make it get 2 different lists of segments.
# Prerequisite: test1() should have been executed in order to already have 'test2_datafile'
# Prerequisite: 'test_3datafile' should not exist before executing this test (erase it to execute again).

import segments

def test3_A() -> None:

    P1 = segments.Point(40.5363713, 0.5739316671)
    P2 = segments.Point(40.79886535, 0.9021482)
    BOX_EBRE_FLOATS = segments.Box(P1, P2)

    filename1 = "test1_datafile"
    filename3 = "test3_datafile"

    #print(segments.get_segments(BOX_EBRE_FLOATS, filename1))
    print(segments.get_segments(BOX_EBRE_FLOATS, filename3, 2, True))

if __name__ == "__main__":
    test3_A()


# Function behaves properly. Downloads if necessary (file not existing) and shows the data correctly. 'test1_datafile' and 'test3_datafile' are equal.