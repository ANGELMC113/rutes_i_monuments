# Short test case to donwload and save the data in a file using segments.donwload_segments()
# Both outputs' data should be equal (the second one is used for test3.py)


import segments

def test1() -> None:

    P1 = segments.Point(40.5363713, 0.5739316671)
    P2 = segments.Point(40.79886535, 0.9021482)
    BOX_EBRE_FLOATS = segments.Box(P1, P2)

    filename1 = "test1_datafile"
    filename2 = "test2_datafile"

    segments.download_segments(BOX_EBRE_FLOATS, filename1, 2, True)
    segments.download_segments(BOX_EBRE_FLOATS, filename2, 2, False)

if __name__ == "__main__":
    test1()


# Correctly downloads the data and places in a text file. Both files are equal. We only get feedback for the first one.