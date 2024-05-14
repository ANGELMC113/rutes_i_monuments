# Short test case to load and display the data in a file using segments.load_segments() (having previously downloaded the data)
# We first check that the lines are correctly read, then we check that our function's output format is correct

import segments

filename = "test1_datafile"

file = open(filename, 'r')
for line in file:
    print(line)

segments_list = segments.load_segments(filename)
print(segments_list)

# Data is correctly displayed