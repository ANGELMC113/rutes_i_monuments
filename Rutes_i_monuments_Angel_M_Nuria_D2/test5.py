# Download all the data available for the given BOX.
# Time it using a laptop (i7 1355U CPU, 16 GB RAM) and Eduroam connection.
# Prerequisite to test time: make sure 'test5_datafile' does not exist.

import time
import segments as sm

def test5() -> sm.Segments:

    P1 = sm.Point(40.5363713, 0.5739316671)
    P2 = sm.Point(40.79886535, 0.9021482)
    BOX_EBRE_FLOATS = sm.Box(P1, P2)

    filename5 = "test5_datafile.dat"

    time_start = time.time()

    segments = sm.get_segments(BOX_EBRE_FLOATS, filename5, feedback=True)

    time_end = time.time()

    print(time_end - time_start)

    return segments

if __name__ == "__main__":
    test5()


# It seems it has downloaded all the data. 116 pages have been downloaded, lasting a total of 404 seconds.
# Executing it again, it takes 0.7 seconds to load the data.

# New execution done later lasted more: 116 pages in 2795 seconds.