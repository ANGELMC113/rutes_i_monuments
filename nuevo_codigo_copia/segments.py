# segments.py

"""Contains functions related to segment gathering from internet
and Segment, Point and Box classes definitions.
Requires internet connection to work."""


from typing import Optional, TypeAlias, Iterator
from dataclasses import dataclass
import requests
import gpxpy
from haversine import haversine
import os.path
from generics import *



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


def _download_segments(filename: str, box_str: str, startpage: int = 0, endpage: int = -1, feedback: bool = True) -> None:
    """Download segments from internet in the box and save them to the given route file.
    maxpage should only be specified to gather less information than all the available (such as testing purposes).
    It is recommended to leave the default 'maxpage' (all pages available in the link) to gather as much information as possible.
    Set 'feedback' to True to see in the command prompt a message when each page is added and each file is saved.
    If it is interrupted before having downloaded all segments, does not save any information in 'filename'."""
    
    page = startpage
    header_filename = filename[:-4]+".txt"

    while endpage == -1 or page <= endpage:
        segments: str = ""
        try:
            url = f"https://api.openstreetmap.org/api/0.6/trackpoints?bbox={box_str}&page={page}"
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
                            
                            line = (f"{p1.latitude}, {p1.longitude}, {p1.time}, '-', {p2.latitude}, {p2.longitude}, {p2.time} \n")
                            segments += line
        
        except ConnectionError or TimeoutError or requests.RequestException or requests.ConnectionError or requests.HTTPError or requests.ConnectTimeout:
        # When there is no internet connection, none of these exceptions are catched.
            raise ConnectionError("Connection error. Check internet connection and try again. If error persists, the server where the data is gathered from may be offline, try waiting a few hours.")

        else:
            with open(filename, "a") as file:
                file.write(segments)
            with open(header_filename, "w") as header:
                header.write(f"{box_str}\n{False}\n{page}")
            if feedback: 
                print(f"Page {page} has been sorted and added.")
            page += 1

    if page > 0:
        with open(header_filename, "w") as header:
            header.write(f"{box_str}\n{True}\n{page - 1}")
        if feedback:
            print(f'{filename} has been saved with the downloaded data.')
    else:
        raise SyntaxError(f"Seems like no data was asked for. No files have been updated and {filename} has not have been created. Program has stopped to avoid working with no data.")


def _segment_generator(filename: str, max_distance_meters: int = 50) -> Iterator[Segment]:
    """Returns a generator of the segments inside "filename"
        whose distance between edges is lower than max_distance_meters.
    "filename" has to be a path (already checked in other functions)."""
    file = open(filename, 'r')
    
    for line in file:
        input = line.split(sep= ", ")

        p1 = (float(input[0]), float(input[1]))
        p2 = (float(input[4]), float(input[5]))

        if haversine(p1, p2, "m") < max_distance_meters:
            yield Segment(start= Point(*p1), end= Point(*p2))
    file.close()


def _load_segments(filename: str) -> Segments:
    """Load segments from the file.
    Filename should be a path ending in .dat, otherwise raises IOError."""
    check_file_extension(filename, ".dat")
    segment_gen = _segment_generator(filename)
    segments: Segments = [seg for seg in segment_gen]
    return segments


def read_data_header(filename: str) -> tuple[str, bool, int]:
    """Read the informationa bout the .dat file.
    Return a tuple with 3 elements:
        The first one is the string format of the box corresponding to the data the file contains.
        The bool tells if all the data has been downloaded from internet.
        The integer is the last page downloaded from internet."""    
    header_filename = filename[:-4]+".txt"
    file = open(header_filename, "r")
    header = [file.readline() for _ in range(3)]
    is_all_data_gathered = (header[1].splitlines()[0] == "True")
    return(header[0].splitlines()[0], is_all_data_gathered, int(header[2]))


def get_segments(filename: str, box: Optional[Box] = None, endpage: int = -1, feedback: bool = True) -> Segments:
    """Check the box given corresponds to this file, and download the possible missing data. Return a list of the gathered segments.
    See documentation to understand the full functionality.
    Filename should be a path ending in .dat, otherwise raises IOError.
    Internet connection is needed, otherwise raises ConnectionError."""  
    check_file_extension(filename, ".dat")
    if filename == "monuments.dat":
        raise FileExistsError("Please, do not name any file 'monuments.dat', as this filename is reserved to monument data gathering. Change filename and try again.")

    if not os.path.isfile(filename): # File does not exist
        if box is not None:
            box_str = box.get_str_format()
            if feedback:
                print(f"File {filename} not found. Downloading the new box's data.")
            _download_segments(filename, box_str, 0, endpage, feedback)
            
        else:
            raise SyntaxError(
                f"File {filename} was not found, and no box was given. \
                Please, write an available file path to load its data, \
                or give a box input to download the data.")

    else: # File exsists
        file_box_str, is_all_data_downloaded, last_downloaded_page = read_data_header(filename)
        if feedback:
            print(f"File {filename} found.")
        if box is not None:
            box_str = box.get_str_format()
            if feedback:
                print(f"Looking for box with string {box_str}")
            if box_str == file_box_str:
                if feedback:
                    print(f"File data corresponds to this box.")
                if is_all_data_downloaded:
                    if feedback:
                        print("All data was already gathered.")
            
                else:
                    if feedback:
                        print("There is some data missing. Downloading missing data.")
                    _download_segments(filename, box_str, last_downloaded_page + 1, endpage, feedback)
                    
            else:
                raise SyntaxError(
                    f"File {filename} does not correspond to the box {box_str}, it corresponds to box {file_box_str}. \
                    The execution has been stoped to avoid a possible mistake in the parameters input. \
                    In order to rewrtie {filename} with new data from a different box, please first delete the file. \
                    If you don't want to overwrite the data, leaving the box parameter empty will get this file's data."
                    )
        else:
            if feedback:
                print(f"No box given. The box corresponding to {filename} is {file_box_str}.")
    if feedback:
        print(f"Loading segments from file {filename}.")
    segments = _load_segments(filename)
    
    if feedback:
        print("Done: segments loaded.")
    return segments
