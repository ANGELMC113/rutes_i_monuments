# Use test1 generated file to check kmeans algorithm (the function is not finished yet)

import segments
import graphmaker


filename = "test1_datafile"

segments_list = segments.load_segments(filename)

cluster_centers = (graphmaker.cluster(segments_list, 0)) # Currently, this function returns kmeans.cluster_centers
print(cluster_centers)

# Effectively returns a list of lists of paris of floats (a list of points)