from sklearn.cluster import KMeans
from segments import *
#import networkx as nx
from networkx import Graph


def _kmeans_cluster(segments: Segments, clusters: int) -> KMeans:
    """Execute a kmeans clustering of the dots joined by segments list, to find a number 'clusters' of centroids.
    Return a KMeans class object."""
    points: list[Point] = []
    for seg in segments:
        points.append(seg.start)
        points.append(seg.end)

    simplified_points: list[list[float]] = [[point.lat, point.lon] for point in points]

    return KMeans(n_clusters=100).fit(simplified_points)  # type: ignore


def _kmeans_centroids(segments: Segments, clusters: int) -> "tuple[ndarray[int], list[Point]]":
    """
    Return two lists:
        The first one is the group in which each point (index) is included.
            Notice: index corresponds to the full list of points (start and end) contained in every segment of segments lits.
            Notice: the maxium is 'clusters - 1' and the minium is 0.
        The second one contains the coordinates of every centroid, expressed Points.
            Notice: the lenght of the second list is 'clusters'."""
    kmeans = _kmeans_cluster(segments, clusters)
    centroid_labels = kmeans.labels_
    centroid_coords = list(Point(a, b) for [a, b] in kmeans.cluster_centers_)
    return centroid_labels, centroid_coords


def _cluster(segments: Segments, clusters: int) -> "tuple[ndarray[int], list[Point], Segments]":
    """Execute a clustering to the given Segments in the given number of clusters.
    Return a tuple of:
        an array with the cluster corresponding to each point in segments
        a list of Points corresponding to each centroid
        a new reduced list of segments representative of the original ones."""
    centroid_labels, centroid_coords = _kmeans_centroids(segments, 0)
    new_segments: Segments = []
    i = 0
    for _ in segments:
        try:
            if centroid_labels[i] != centroid_labels[i + 1]: # If segments joins different cluster
                new_segment = Segment(centroid_coords[centroid_labels[i]], centroid_coords[centroid_labels[i + 1]]) # Segment between centroids
                if new_segment not in new_segments: 
                    new_segments.append(new_segment)
            i += 2
        except:
            print('failed')
    return centroid_coords, centroid_coords, new_segments
    

def make_graph(segments: Segments, clusters: int) -> Graph:
    """Make a graph from the segments."""


def simplify_graph(graph: Graph, epsilon: float) -> Graph:
    """Simplify the graph."""

    