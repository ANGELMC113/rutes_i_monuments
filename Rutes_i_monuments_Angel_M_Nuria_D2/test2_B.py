# Short test case to load and display the data in a file using segments.load_segments()
# Prerequisite: test1() should have been executed in order to already have 'test1_datafile'

# In test2_B, we ensure 

import segments


def test2_B() -> None:

    filename1 = "test1_datafile.dat"

    #file = open(filename, "r")
    #for line in file:
        #print(line)

    segments_list = segments.load_segments(filename1)
    print(segments_list)


if __name__ == "__main__":
    test2_B()


# Data is correctly loaded and placed into a list of segments.