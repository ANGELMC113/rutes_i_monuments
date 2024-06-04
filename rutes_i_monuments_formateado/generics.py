# generics.py

"""Contains transversal defined constants and functions."""


from dataclasses import dataclass
from typing import TypeAlias
from haversine import haversine  # type: ignore (stub file missing)


MONUMENTS_FILENAME = "monuments.dat"  # Changing this filename can cause problems if the new filename (or METADATA_MONUMENTS_FILENAME) already exists
"""Default route to save the monuments' data."""

DEFAULT_FEEDBACK: bool = True
"""Establish the default feedback for all functionalities which use it.
Feedback consists on messages being printed on the command prompt when some processes are completed."""


@dataclass
class Point:
    lat: float
    lon: float


@dataclass
class Segment:
    start: Point
    end: Point


Segments: TypeAlias = list[Segment]


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
            + ","
            + str(self.bottom_left.lat)
            + ","
            + str(self.top_right.lon)
            + ","
            + str(self.top_right.lat)
        )


def check_file_extension(filename: str, extension: str) -> None:
    """Checks if filename is of the desired extension.
    Raises IOError if it's incorrect.
    The extension should be given without the point (for example, "dat")."""
    file_and_extension = filename.split(".")
    if len(file_and_extension) < 2 or file_and_extension[1] != extension:
        raise IOError(
            f"The format of the given file is incorrect. Filename should finish in {extension}"
        )


def distance(a: Point, b: Point, unit: str = "km") -> float:
    """Return the haversine distance between the given points.
    Units can be changed as stated by haversine documentation (for example, "m" sets the unit to meters).
    """
    return haversine((a.lat, a.lon), (b.lat, b.lon), unit)  # type: ignore
