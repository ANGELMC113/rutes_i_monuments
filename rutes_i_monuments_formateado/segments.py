# segments.py

"""Contains functions related to segment gathering from internet
and Segment, Point and Box classes definitions.
Requires internet connection to work."""


from typing import Optional, Iterator
import json
import requests
import gpxpy
import os.path
from generics import (
    MONUMENTS_FILENAME,
    Point,
    Segment,
    Segments,
    Box,
    check_file_extension,
    distance,
    DEFAULT_FEEDBACK,
)


SEGMENT_MAX_LENGHT_METERS: int = 50
"""Max distance between points used to load the segments. This value allows to filter the data, by erasing semgents wich are too long."""


def _download_segments(
    filename: str,
    box_str: str,
    startpage: int = 0,
    endpage: int = -1,
    feedback: bool = DEFAULT_FEEDBACK,
) -> None:
    """Download segments from internet in the box and save them to the given route file.
    maxpage should only be specified to gather less information than all the available (such as testing purposes).
    It is recommended to leave the default 'maxpage' (all pages available in the link) to gather as much information as possible.
    Set 'feedback' to True to see in the command prompt a message when each page is added and each file is saved.
    If it is interrupted before having downloaded all segments, does not save any information in 'filename'.
    """

    page = startpage
    metadata_filename = filename[:-4] + ".json"

    while endpage == -1 or page <= endpage:
        segments: str = ""
        try:
            url = f"https://api.openstreetmap.org/api/0.6/trackpoints?bbox={box_str}&page={page}"
            response = requests.get(url)
            gpx_content = response.content.decode("utf-8")
            gpx = gpxpy.parse(gpx_content)

            if len(gpx.tracks) == 0:  # We have already got all the data
                break

            for track in gpx.tracks:
                for segment in track.segments:
                    if all(point.time is not None for point in segment.points):
                        segment.points.sort(key=lambda p: p.time)  # type: ignore
                        for i in range(len(segment.points) - 1):
                            p1, p2 = segment.points[i], segment.points[i + 1]

                            line = f"{p1.latitude}, {p1.longitude}, {p1.time}, '-', {p2.latitude}, {p2.longitude}, {p2.time} \n"
                            segments += line

        except (
            ConnectionError,
            TimeoutError,
            requests.RequestException,
            requests.ConnectionError,
            requests.HTTPError,
            requests.ConnectTimeout,
        ) as e:
            raise ConnectionError(
                "Connection error. Check internet connection and try again. If error persists, the server where the data is gathered from may be offline, try waiting a few hours."
            ) from e

        else:
            with open(filename, "a") as file:
                file.write(segments)
            with open(metadata_filename, "w") as metadata:
                json.dump(
                    {
                        "box_str": box_str,
                        "is_all_data_gathered": False,
                        "last_page": page,
                    },
                    metadata,
                )
            if feedback:
                print(f"Page {page} has been sorted and added.")
            page += 1

    if page > 0:
        with open(metadata_filename, "w") as metadata:
            json.dump(
                {
                    "box_str": box_str,
                    "is_all_data_gathered": True,
                    "last_page": page - 1,
                },
                metadata,
            )
        if feedback:
            print(f"{filename} has been saved with the downloaded data.")
    else:
        raise SyntaxError(
            f"Seems like no data was asked for. No files have been updated and {filename} has not have been created. Program has stopped to avoid working with no data."
        )


def _segment_generator(
    filename: str, max_distance_meters: int = SEGMENT_MAX_LENGHT_METERS
) -> Iterator[Segment]:
    """Returns a generator of the segments inside "filename"
        whose distance between points is lower than max_distance_meters.
    "filename" has to exist (already checked in other functions)."""
    assert os.path.isfile(filename)
    file = open(filename, "r")

    for line in file:
        input = line.split(sep=", ")

        p1 = Point(float(input[0]), float(input[1]))
        p2 = Point(float(input[4]), float(input[5]))

        if distance(p1, p2, "m") < max_distance_meters:
            yield Segment(p1, p2)
    file.close()


def _load_segments(filename: str) -> Segments:
    """Load segments from the file.
    Filename should be a path ending in .dat, otherwise raises IOError."""
    check_file_extension(filename, "dat")
    return list(_segment_generator(filename))


def _read_metadata(filename: str) -> tuple[str, bool, int]:
    """Read the informationa bout the .dat file.
    Return a tuple with 3 elements:
        The first one is the string format of the box corresponding to the data the file contains.
        The bool tells if all the data has been downloaded from internet.
        The integer is the last page downloaded from internet."""
    metadata_filename = filename[:-4] + ".json"
    with open(metadata_filename, "r") as file:
        metadata = json.load(file)
    return metadata["box_str"], metadata["is_all_data_gathered"], metadata["last_page"]


def get_segments(
    filename: str,
    box: Optional[Box] = None,
    endpage: int = -1,
    feedback: bool = DEFAULT_FEEDBACK,
) -> Segments:
    """Check the box given corresponds to this file, and download the possible missing data. Return a list of the gathered segments.
    See documentation to understand the full functionality.
    Filename should be a path ending in .dat, otherwise raises IOError.
    Internet connection is needed, otherwise raises ConnectionError."""
    check_file_extension(filename, "dat")
    if filename == MONUMENTS_FILENAME:
        raise FileExistsError(
            f"Please, do not name any file {MONUMENTS_FILENAME}, as this filename is reserved to monument data gathering. Change filename and try again."
        )

    if not os.path.isfile(filename):  # File does not exist
        if box is not None:
            box_str = box.get_str_format()
            if feedback:
                print(f"File {filename} not found. Downloading the new box's data.")
            _download_segments(filename, box_str, 0, endpage, feedback)

        else:
            raise SyntaxError(
                f"File {filename} was not found, and no box was given. \
                Please, write an available file path to load its data, \
                or give a box input to download the data."
            )

    else:  # File exsists
        try:
            file_box_str, is_all_data_downloaded, last_downloaded_page = _read_metadata(
                filename
            )
        except FileNotFoundError:
            metadata_filename = filename[:-4] + ".json"
            raise FileNotFoundError(
                f"{metadata_filename} not found. To avoid having incorrect data, \
                please make sure you have not moved the .json out of the working directory. \
                If you have not removed or modified {metadata_filename}, \
                you can remove {filename} and download the data again using the same filename."
            )
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
                        print(
                            "There is some data missing. Downloading the missing data."
                        )
                    _download_segments(
                        filename, box_str, last_downloaded_page + 1, endpage, feedback
                    )

            else:
                raise SyntaxError(
                    f"File {filename} does not correspond to the box {box_str}, it corresponds to box {file_box_str}. \
                    The execution has been stoped to avoid a possible mistake in the parameters input. \
                    In order to rewrtie {filename} with new data from a different box, please first delete the file. \
                    If you don't want to overwrite the data, leaving the box parameter empty will get this file's data."
                )
        else:
            if feedback:
                print(
                    f"No box given. The box corresponding to {filename} is {file_box_str}."
                )
    if feedback:
        print(f"Loading segments from file {filename}.")
    segments = _load_segments(filename)
    if feedback:
        print("Done: segments loaded.")
    return segments
