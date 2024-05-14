# Use test5 generated file to check kmeans algorithm (a part of it)
# Important: an auziliar function has been created in order to return every output needed


import segments as sm
import graphmaker as gm
import staticmap


filename = "test5_datafile"

segments = sm.load_segments(filename)

centroid_labels, centroid_coords, new_segments = gm._cluster(segments, 0)

"""Show all segments in a PNG file using staticmap."""
map = staticmap.StaticMap(800, 800)
color = 'red'
width = 2
for seg in new_segments:
    map.add_line(staticmap.Line(((seg.start.lon, seg.start.lat), (seg.end.lon, seg.end.lat)), color, width)) # type: ignore
color = 'orange'
width = 10
for point in centroid_coords:
    map.add_marker(staticmap.CircleMarker((point.lon, point.lat), color, width))
image = map.render() # type: ignore
image.save('map4.png')


