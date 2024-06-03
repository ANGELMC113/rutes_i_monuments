# monuments.py

"""Contains functions related to Monument definition and data gathering from Catalunya Medieval."""


from dataclasses import dataclass
from typing import TypeAlias, Iterator
import json
import re
import requests
import os
import time
from bs4 import BeautifulSoup
from generics import MONUMENTS_FILENAME, Point



METADATA_MONUMENTS_FILENAME = MONUMENTS_FILENAME[:-4]+".json"  # Do not modify this line
"""Default route to save the metadata of the monuments.
Do not modify the expression defining this costant."""         # If this filename differs from MONUMENTS_FILENAME, the json file may be overwritten by segments.py


TYPES: list[str] = ["militar", "civil", "religios", "altres"]

LINKS: dict[str, str] = {
    "militar":  "https://www.catalunyamedieval.es/edificacions-de-caracter-militar/",
    "civil": "https://www.catalunyamedieval.es/edificacions-de-caracter-civil/",
    "religios": "https://www.catalunyamedieval.es/edificacions-de-caracter-religios/",
    "altres": "https://www.catalunyamedieval.es/altres-llocs-dinteres/"
}

APPENDIX_TYPES: dict[str, list[str]] = {
    "militar": ["castells/", "epoca-carlina/", "muralles/", "torres/"], 
    "civil": ["cases-fortes/", "palaus/", "ponts/", "torres-colomer/"],
    "religios": ["basiliques/", "catedrals/", "ermites/", "esglesies/", "esglesies-fortificades", "monestirs/"],
    "altres": ['']
}

SUBCLASSES: dict[str, list[str]] = {
    "militar": ["castell", "epoca carlina", "muralla", "torre"],
    "civil": ["casa forta", "palau", "pont", "torre colomer"],
    "religios": ["basilica", "catedral", "ermita", "esglesia", "esglesia fortificada", "monestir"],
    "altres": ["altres"]
}
  

CONNECTION_RETRY_DELAY: int = 10
"""Time to wait before trying to connect again when a ConnectionResetError happens (in seconds)."""


@dataclass
class Monument:
    """Class to relate a Point (.location) with its monument (.name)."""
    name: str
    sublcass: str
    location: Point

Monuments: TypeAlias = list[Monument]


    
def _get_point(soup: BeautifulSoup) -> str | None:
    """Given a BeautifulSoup class object, downloaded from a specific Monument page, 
    search for the pattern which displays its coordinates."""
    scripts = soup.find_all("script") # Filter script tags
    pattern = re.compile(r"var destinations = \['([\d\.\s]+)'\];") # Pattern to search for the coordinates

    for script in scripts:
        if script.string: # Check if the script tag contains any text
            match = pattern.search(script.string) # Search for the pattern in the script text
            if match:
                coords = match.group(1)
                return coords
            

def _download_monuments(start: tuple[int, int, int], feedback: bool = True) -> None:
    """Download monuments to MONUMENTS_FILENAME, starting by the chosen indexes the matrix elements.
    Data will be downloaded from Catalunya Medieval. Needs internet connection to work."""

    x, y, z = start

    for i in range (x, len(TYPES)):                      # for every type in TYPES
        monument_type = TYPES[i]
        for j in range(y, len(APPENDIX_TYPES[monument_type])):    # for every class in this type
            subclass = SUBCLASSES[monument_type][j]
            try:
                if feedback:
                    print(f"Downloading type {monument_type}: {subclass}.")
                
                url = LINKS[monument_type] +  APPENDIX_TYPES[monument_type][j]

                response = requests.get(url)
                soup = BeautifulSoup(response.content, "html.parser")
                places = soup.find_all ("li", class_= subclass)

                if feedback:
                    print(f"{len(places)} monuments of this type have been found.")
                
                for k in range(z, len(places)):
                    try:
                        link = places[k].find("a")
                        new_url = link.get("href")
                        try:
                            new_response = requests.get(new_url)
                        except: 
                            new_response= requests.get(new_url)
                        finally:
                            soup = BeautifulSoup(new_response.content,"html.parser")
                            
                            coords = _get_point(soup)

                            if coords is not None:
                                text = (link.text).split(sep=" – ") # – U+2013                          # Maybe we split name and location

                                num_name_location = text[0].split(sep=". ")                             # Maybe location is still with name
                                num_in_subclass = num_name_location[0]                                  # Always the number, found before "."
                                name_and_location = num_name_location[1].split(sep=" / ")               # Now we separate the location from the name if no "–" was found
                                name = name_and_location[0]                                             # Always the name, found after "." and before "–" or "/" 

                                location: str = ""                                                      # Location is everything else we see after the name and before the coordinates

                                if len(name_and_location) > 1:
                                    location += name_and_location[1]
                                if len(text) > 1:
                                    location += text[1]
                                if location == "":
                                    location = "Ubicació desconeguda"
                                
                                line = (f"{monument_type}@{subclass}@{num_in_subclass}@{name}@{location}@{coords} \n")
                                
                                with open(MONUMENTS_FILENAME, "a", encoding="utf8") as file:
                                        file.write(line)
                                metadata = {
                                    "is_all_data_downloaded": False,
                                    "type_index": i,
                                    "subclass_index": j,
                                    "place_index": k
                                }
                                with open(METADATA_MONUMENTS_FILENAME, "w") as metadata_file:
                                    json.dump(metadata, metadata_file)
                                if feedback:
                                    print(f"Monument {link.text}, located at {coords} has been added.")

                            else:
                                if feedback:
                                    print(f"Monument {link.text} has not been added because its coordinates have not been found.")

                    except ConnectionResetError:
                        print(f"Connection Reset Error. Waiting {CONNECTION_RETRY_DELAY} and trying again.")
                        time.sleep(CONNECTION_RETRY_DELAY)
                        _download_monuments((i, j, k), feedback)
                z = 0

            except (ConnectionError, TimeoutError, requests.RequestException, requests.ConnectionError, requests.HTTPError, requests.ConnectTimeout) as e:
                raise ConnectionError("Connection error. Check internet connection and try again. If error persists, the server where the data is gathered from may be offline, try waiting a few hours.") from e
        y = 0

    metadata = {
        "is_all_data_downloaded": True,
        "type_index": x,
        "subclass_index": y,
        "place_index": z
    }
    with open(METADATA_MONUMENTS_FILENAME, "w") as metadata_file:
        json.dump(metadata, metadata_file)
    if feedback:
        print("All monuments' data has been gathered.")
    

def _monument_generator() -> Iterator[Monument]:
    """Returns a generator of the monuments inside MONUMENTS_FILENAME.
    MONUMENTS_FILENAME has to exist (already checked in other funcions)."""
    assert os.path.isfile(MONUMENTS_FILENAME)
    with open(MONUMENTS_FILENAME, "r", encoding="utf8") as file:
        for line in file:
            input = line.split(sep="@")

            monument_type = input[0]            # type: ignore (unused information)
            sublcass = input[1]
            num_in_subclass = input[2]          # type: ignore (unused information)
            name = input[3]
            location = input[4]                 # type: ignore (unused information)
            coords = input[5].split()

            point = Point(float(coords[0]), float(coords[1]))
            yield Monument(name, sublcass, point)


def _load_monuments() -> Monuments:
    """Load monuments from a file."""
    return list(_monument_generator())


def _read_monuments_metadata() -> tuple[bool, tuple[int, int, int]]:
    try:
        with open(METADATA_MONUMENTS_FILENAME, "r") as metadata_file:
            metadata = json.load(metadata_file)
        return metadata["is_all_data_downloaded"], (metadata["type_index"], metadata["subclass_index"], metadata["place_index"])
    except FileNotFoundError:
        raise FileNotFoundError(f"{METADATA_MONUMENTS_FILENAME} not found. To avoid having incorrect data, \
            please make sure you have not moved the .json out of the working directory. \
            If you have not removed or modified {METADATA_MONUMENTS_FILENAME}, \
            you can remove {MONUMENTS_FILENAME} and download the data again."
        )


def get_monuments(feedback: bool = True) -> Monuments:
    """
    Get all monuments in the box.
    If MONUMENTS_FILENAME exists, load monuments from the file.
    Otherwise, download monuments and save them to the file.
    """
    if not os.path.isfile(MONUMENTS_FILENAME): # File does not exist
        if feedback:
            print(f"{MONUMENTS_FILENAME} not found. Downloading monuments.")
        _download_monuments((0, 0, 0), feedback)

    else: # File exists
        if feedback:
            print(f"{MONUMENTS_FILENAME} found.")
        is_all_data_downloaded, last_downloaded_monument = _read_monuments_metadata()
        if is_all_data_downloaded:
            if feedback:
                print("All monuments' data was already gathered.")
        else:
            if feedback:
                print("There is some data missing. Downloading the missing data.")
                next_monument = (last_downloaded_monument[0], last_downloaded_monument[1], last_downloaded_monument[2] + 1)
                _download_monuments(next_monument, feedback)
    if feedback:
        print(f"Loading monuments.")
    monuments = _load_monuments()
        
    if feedback:
        print("Done: monuments loaded.")
    return monuments


if __name__ == "__main__":
    """monuments.py can be executed without parameters to download the monuments."""
    get_monuments()
