# Short test case to donwload and save the data in a file using segments.donwload_segments()
# Both outputs' data should be equal (the second one is used for test3.py)
# It shoudl also create two .txt files containing the box string, True, and the last page downloaded (1).


import segments

def test1() -> None:

    P1 = segments.Point(40.5363713, 0.5739316671)
    P2 = segments.Point(40.79886535, 0.9021482)
    BOX_EBRE_FLOATS = segments.Box(P1, P2)

    filename1 = "test_datafile1.dat"
    filename2 = "test_datafile2.dat"

    segments.get_segments(filename1, BOX_EBRE_FLOATS, 2)
    segments.get_segments(filename2, BOX_EBRE_FLOATS, 2)

if __name__ == "__main__":
    test1()


# Correctly downloads the data and places in a text file. Both files are equal.
# The auciliar header files are correct.