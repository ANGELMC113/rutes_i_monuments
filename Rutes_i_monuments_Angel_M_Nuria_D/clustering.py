# clustering.py 

# type: ignore

"""Contains functions related to clustering."""


from sklearn.cluster import KMeans
from generics import Point, Segment, Segments



def _kmeans_cluster(segments: Segments, n_clusters: int) -> KMeans:
    """Execute a kmeans clustering of the dots joined by segments list, to find "n_clusters" centroids.
    Return a KMeans class object."""
    points: list[Point] = []
    for seg in segments:
        points.append(seg.start)
        points.append(seg.end)

    simplified_points: list[list[float]] = [[point.lat, point.lon] for point in points]

    return KMeans(n_clusters=n_clusters).fit(simplified_points)  # type: ignore


def _kmeans_centroids(segments: Segments, n_clusters: int) -> "tuple[ndarray[int], list[Point]]":
    """Execute a clustering and return two lists:
        The first one is the cluster in which each point from the initial list (index) is included.
        The second one contains the coordinates of every centroid, expressed as Points."""
    # Some things to take into account:
        # centroid_labels index corresponds to the full list of points (start and end) from each segment of the initial segments list.
        # centroid_labels maximum is "n_clusters" - 1 and its minimum is 0.
        # centroid_coords list is equal to "n_clusters".
    kmeans = _kmeans_cluster(segments, n_clusters)
    centroid_labels = kmeans.labels_
    centroid_coords = list(Point(a, b) for [a, b] in kmeans.cluster_centers_)
    return centroid_labels, centroid_coords


def cluster(segments: Segments, n_clusters: int) -> "tuple[ndarray[int], list[Point], list[tuple[int, int]], Segments]":
    """Execute a clustering to the given Segments to get the given number of clusters.
    Return a tuple with:
        an array with the cluster corresponding to each point in segments,
        a list of Points corresponding to each centroid,
        a new reduced list of segments representative of the original ones, and
        a list which tells which nodes are connected (edges in a graph)."""
    # Note that each segment corresponds to an edge.
    centroid_labels, centroid_coords = _kmeans_centroids(segments, n_clusters)
    edges: list[tuple[int, int]] = []
    new_segments: Segments = []
    i = 0
    for _ in segments:
        if centroid_labels[i] != centroid_labels[i + 1]: # If segments joins different cluster
            edge = (centroid_labels[i], centroid_labels[i + 1])                                                 # Edge between centroids (as ints)
            new_segment = Segment(centroid_coords[centroid_labels[i]], centroid_coords[centroid_labels[i + 1]]) # Segment between centroids (as Points)
            if edge not in edges:
                edges.append(edge)
            if new_segment not in new_segments: 
                new_segments.append(new_segment)
        i += 2
    return centroid_labels, centroid_coords, edges, new_segments
