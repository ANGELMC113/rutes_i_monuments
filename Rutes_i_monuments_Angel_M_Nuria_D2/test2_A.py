# Short test case to load and display the data in a file using segments.load_segments()
# Prerequisite: test1() should have been executed in order to already have 'test1_datafile'

# In test2_A, we check that the lines in the datafile are correctly read using open() function.

import segments


def test2_A() -> None:

    filename1 = "test1_datafile.dat"

    file = open(filename1, "r")
    for line in file:
        print(line)

    #segments_list = segments.load_segments(filename)
    #print(segments_list)


if __name__ == "__main__":
    test2_A()


# Lines are correctly read