# Use test5 generated file to check kmeans algorithm (a part of it)

import segments as sm
import graphmaker as gm
import staticmap


filename = "test5_datafile"

segments = sm.load_segments(filename)

centroid_labels, centroid_coords = gm._kmeans_centroids(segments, 0)
print(centroid_labels)
print(centroid_coords)
print(max(centroid_labels))
print(min(centroid_labels))
print(len(centroid_coords))

# Effectively returns the array of labels (related cluster) of each point and the Points corresponding to the centroid of each cluster.


"""Show all segments in a PNG file using staticmap."""
map = staticmap.StaticMap(800, 800)
color = 'purple'
width = 2
for seg in segments:
    map.add_line(staticmap.Line(((seg.start.lon, seg.start.lat), (seg.end.lon, seg.end.lat)), color, width)) # type: ignore
color = 'orange'
width = 10
for point in centroid_coords:
    map.add_marker(staticmap.CircleMarker((point.lon, point.lat), color, width))
image = map.render() # type: ignore
image.save('map3.png')

# Effectively displays a map with routes and some dots. These dots are close to the routes, and most of the times 'contained in them' (apparently)
