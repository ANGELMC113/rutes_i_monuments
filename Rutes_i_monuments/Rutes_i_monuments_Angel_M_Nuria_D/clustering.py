# clustering.py

'''Contains functions related to clustering.'''


from sklearn.cluster import KMeans
from segments import *


def _kmeans_cluster(segments: Segments, n_clusters: int) -> KMeans:
    """Execute a kmeans clustering of the dots joined by segments list, to find 'n_clusters' centroids.
    Return a KMeans class object."""
    points: list[Point] = []
    for seg in segments:
        points.append(seg.start)
        points.append(seg.end)

    simplified_points: list[list[float]] = [[point.lat, point.lon] for point in points]

    return KMeans(n_clusters=n_clusters).fit(simplified_points)  # type: ignore


def _kmeans_centroids(segments: Segments, n_clusters: int) -> "tuple[ndarray[int], list[Point]]":
    """
    Execute a clustering and
    return two lists:
        The first one is the group in which each point (index) is included.
            Notice: index corresponds to the full list of points (start and end) contained in every segment of segments lits.
            Notice: the maxium is 'clusters - 1' and the minimum is 0.
        The second one contains the coordinates of every centroid, expressed as Points.
            Notice: the lenght of the second list is equal to 'clusters'."""
    kmeans = _kmeans_cluster(segments, n_clusters)
    centroid_labels = kmeans.labels_
    centroid_coords = list(Point(a, b) for [a, b] in kmeans.cluster_centers_)
    return centroid_labels, centroid_coords


def cluster(segments: Segments, n_clusters: int) -> "tuple[ndarray[int], list[Point], Segments]":
    """Execute a clustering to the given Segments in the given number of clusters.
    Return a tuple with:
        an array with the cluster corresponding to each point in segments
        a list of Points corresponding to each centroid
        a new reduced list of segments representative of the original ones."""
    centroid_labels, centroid_coords = _kmeans_centroids(segments, n_clusters)
    new_segments: Segments = []
    i = 0
    for _ in segments:
        try: # We will remove this check after some testing is done
            if centroid_labels[i] != centroid_labels[i + 1]: # If segments joins different cluster
                new_segment = Segment(centroid_coords[centroid_labels[i]], centroid_coords[centroid_labels[i + 1]]) # Segment between centroids
                if new_segment not in new_segments: 
                    new_segments.append(new_segment)
            i += 2
        except:
            print('failed')
    return centroid_labels, centroid_coords, new_segments