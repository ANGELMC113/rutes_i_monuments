# Tets routes.py

from staticmap import StaticMap, Line, CircleMarker
from segments import Point, Segment, Box, get_segments
from map_drawing import export_png_map, export_kml
from clustering import cluster
from graphmaker import _make_graph_from_kmeans
from monuments import Monument, Monuments
import routes



def test13():
    
    testing_monuments = [   
        Monument("Deltebre", Point(40.72082, 0.71721)),
        Monument("Mirador del Zigurat", Point(40.72304, 0.85995)),
        Monument("Amposta", Point(40.70718, 0.57895))
    ]

    P1 = Point(40.5363713, 0.5739316671)
    P2 = Point(40.79886535, 0.9021482)
    BOX_EBRE_FLOATS = Box(P1, P2)

    filename5 = "test_datafile5.dat"
    mapname9 = "map9.png"

    segments = get_segments(filename5, BOX_EBRE_FLOATS)
    centroid_labels, centroid_coords, edges, new_segments = cluster(segments, 100)
    G = _make_graph_from_kmeans(centroid_labels, centroid_coords, edges, new_segments)

    '''
    nodes_with_monument = routes._approximate_monuments(G, testing_monuments)
    print(nodes_with_monument)

    map = StaticMap(1000, 1000)
    line_color = "purple"
    line_width = 5
    marker_color = "orange"
    marker_width = 10
    for edge in G.edges:                                                                                            
        seg = Segment(start=G.nodes[edge[0]]['point'], end=G.nodes[edge[1]]['point'])                               
        map.add_line(Line(((seg.start.lon, seg.start.lat), (seg.end.lon, seg.end.lat)), line_color, line_width))    
    for node in G.nodes:                                                                                            
        point = G.nodes[node]['point']
        if node in nodes_with_monument:
            map.add_marker(CircleMarker((point.lon, point.lat), "red", 20))                            
        else:                                                                              
            map.add_marker(CircleMarker((point.lon, point.lat), marker_color, marker_width))  
    image = map.render()    
    image.save(mapname9)                          
    '''

    start = Point(40.75718, 0.70385)

    mapname10 = "map10.png"
    kmlname2 = "map_kml2.kml"
    T = routes._create_tree(G, start, testing_monuments)

    export_png_map(mapname10, T)

    export_kml(kmlname2, T)

if __name__ == "__main__":  
    test13()