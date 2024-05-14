from typing import TypeAlias
from dataclasses import dataclass
import requests
import gpxpy
from typing import Iterator
import staticmap


@dataclass
class Point:
    lat: float
    lon: float

@dataclass
class Segment:
    start: Point
    end: Point


class Box:
    bottom_left: Point
    top_right: Point

    def __init__(self, bottom_left: Point, top_right: Point) -> None:
        """Create a box class object by entering 2 points:
        bottom_left and top_right."""
        self.bottom_left = bottom_left
        self.top_right = top_right

    def get_str_format(self) -> str:
        """Return a suitable string to place inside the url.
            The string consist in all the coordinates separated by commas.
            Latitude and longitude are inverted."""
        return (
          str(self.bottom_left.lon)
        + ','
        + str(self.bottom_left.lat)
        + ','
        + str(self.top_right.lon)
        + ','
        + str(self.top_right.lat)
    )


Segments: TypeAlias = list[Segment]


def download_segments(box: Box, filename: str) -> None:
    """Download all segments in the box and save them to the file."""

    segments: str = ''

    BOX = box.get_str_format()

    page = 0

    while True:
        url = f"https://api.openstreetmap.org/api/0.6/trackpoints?bbox={BOX}&page={page}"
        response = requests.get(url)
        gpx_content = response.content.decode("utf-8")
        gpx = gpxpy.parse(gpx_content)

        if len(gpx.tracks) == 0:    # We have already got all the data
            break

        for track in gpx.tracks:
            for segment in track.segments:
                if all(point.time is not None for point in segment.points):
                    segment.points.sort(key=lambda p: p.time)  # type: ignore
                    for i in range(len(segment.points) - 1):
                        p1, p2 = segment.points[i], segment.points[i + 1]
                        
                        segments += (f'{p1.latitude}, {p1.longitude}, {p1.time}, "-", {p2.latitude}, {p2.longitude}, {p2.time} \n')
        print(f'Page {page} has been sorted and added.')
        page += 1

    with open(filename, 'w') as file:       # Open 'filename' file in write mode
        print(segments, file = file)
    file.close()


def _segment_generator(filename: str) -> Iterator[Segment]:
    """Returns a generator of all the segments inside 'filename'.
    'filename' should be a path."""
    file = open(filename, 'r')

    for line in file:
        input = line.split(sep= ", ")
        if input[0] != "\n":
            yield Segment(
                start= Point(float(input[0]), float(input[1])),
                end= Point(float(input[4]), float(input[5]))
            )
    file.close()


def load_segments(filename: str) -> Segments:
    """Load segments from the file."""
    segment_gen = _segment_generator(filename)
    segments: Segments = [seg for seg in segment_gen]
    return segments


def get_segments(box: Box, filename: str) -> Segments:
    """
    Get all segments in the box.
    If filename exists, load segments from the file.
    Otherwise, download segments in the box and save them to the file.
    """
    try:
        segments = load_segments(filename)
        print(f"File found. Loading segments from file {filename}. This box's content has been ignored.")
    except FileNotFoundError or OSError or IOError:
        try:
            print(f"File {filename} not found. Donwloading the new box's Data.")
            download_segments(box, filename)
            print(f"Loading segments from file {filename}.")
            segments = load_segments(filename)
        except:
            raise SyntaxError('There has been an unknown error. Try to check that the coordinates in the box and the name of the file are correct.')
    return segments


def show_segments(segments: Segments, filename: str, color: str = 'purple', width: int = 2) -> None:
    """Show all segments in a PNG file using staticmap.
    Color parameter should be a standard color. ... 
    Width is recommended to be between 1 and 10."""
    map = staticmap.StaticMap(800, 800)
    for seg in segments:
        map.add_line(staticmap.Line(((seg.start.lon, seg.start.lat), (seg.end.lon, seg.end.lat)), color, width)) # type: ignore
    image = map.render() # type: ignore
    image.save(filename)