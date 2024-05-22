# segments.py

"""Contains functions related to segment gathering from internet
and Segment, Point and Box classes definitions.
Requires internet connection to work."""


from typing import TypeAlias
from dataclasses import dataclass
import requests
import gpxpy
from typing import Iterator


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


def download_segments(box: Box, filename: str, maxpage: int = -1, feedback: bool = True) -> None:
    """Download segments from internet in the box and save them to the given route file.
    maxpage should only be specified to gather less information than all the available (such as testing purposes).
    It is recommended to leave the default 'maxpage' (all pages available in the link) to gather as much information as possible.
    Set 'feedback' to True to see in the command prompt a message when each page is added and each file is saved.
    If it is interrupted before having downloaded all segments, does not save any information in 'filename'."""

    BOX = box.get_str_format()

    page = 0

    file = open(filename, "w")

    while page != maxpage:
        try:
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
                            
                            line = (f'{p1.latitude}, {p1.longitude}, {p1.time}, "-", {p2.latitude}, {p2.longitude}, {p2.time} \n')
                            file.write(line)
        
        except ConnectionError or TimeoutError:
            raise ConnectionError("Connection error. Check internet connection and try again. If error persists, the server where the data is gathered from may be offline, try waiting a few hours.")

        else:
            if feedback: 
                print(f'Page {page} has been sorted and added.')
            page += 1

   
    file.close()
    if feedback:
        print(f'{filename} has been saved with the downloaded data.')


def _segment_generator(filename: str) -> Iterator[Segment]:
    """Returns a generator of all the segments inside 'filename'.
    'filename' should be a path."""
    file = open(filename, 'r')

    for line in file:
        input = line.split(sep= ", ")
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


def get_segments(box: Box, filename: str, maxpage: int = -1, feedback: bool = True) -> Segments:
    """Get all segments in the box.
    If filename exists, load segments from the file.
    Otherwise, download 'maxpage' number of pages of segments in the box and save them to the file.
    'maxpage' should only be set for time limitations or testing purposes."""
    try:
        segments = load_segments(filename)
        if feedback:
            print(f"File found. Loading segments from file {filename}. This box's content has been ignored.")
    except FileNotFoundError or OSError or IOError:
        try:
            if feedback:
                print(f"File {filename} not found. Downloading the new box's data.")
            download_segments(box, filename, maxpage, feedback)
            if feedback:
                print(f"Loading segments from file {filename}.")
            segments = load_segments(filename)
        except:
            raise SyntaxError('There has been an unknown error. Try to check that the coordinates in the box and the name of the file are correct. Ensure you have a stable internet connection.')
# no internet conenction should rise a specific error
    return segments

