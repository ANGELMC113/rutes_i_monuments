from dataclasses import dataclass
from typing import TypeAlias
from bs4 import BeautifulSoup
import requests
import pickle
import os
import time

@dataclass
class Point:
    lat: float
    lon: float
  
@dataclass
class Monument:
     name: str
     location: Point

Monuments: TypeAlias = list[Monument]

FILENAME = "monuments.dat"
HEADER_FILENAME = "monuments.txt"


TYPES: list[str] = ["militar", "civil", "religios", "altres"]

LINKS: dict[str, str] = {
    "militar":  "https://www.catalunyamedieval.es/edificacions-de-caracter-militar/",
    "civil": "https://www.catalunyamedieval.es/edificacions-de-caracter-civil/",
    "religios": "https://www.catalunyamedieval.es/edificacions-de-caracter-religios/",
    "altres": "https://www.catalunyamedieval.es/altres-llocs-dinteres/"
}

LINK_TYPES: dict[str, list[str]] = {
    "militar": ["castells/", "epoca-carlina/", "muralles/", "torres/"], 
    "civil": ["cases-fortes/", "palaus/", "ponts/", "torres-colomer/"],
    "religios": ["basiliques/", "catedrals/", "ermites/", "esglesies/", "esglesies-fortificades", "monestirs/"],
    "altres": ['']
}

PLACE_TYPES: dict[str, list[str]] = {
    "militar": ["castell", "epoca carlina", "muralla", "torre"],
    "civil": ["casa forta", "palau", "pont", "torre colomer"],
    "religios": ["basilica", "catedral", "ermita", "esglesia", "esglesia fortificada", "monestir"],
    "altres": ["altres"]
}

def _save_monuments(monuments:Monuments, filename:str) -> None:
    """Save monuments into a file"""
    with open (filename, 'w') as file:
            print(monuments, file=file)
    file.close
    
    #pickle_out = open(filename, "wb")
    #pickle.dump(monuments, pickle_out)
    #pickle_out.close()


def _get_coordenates(coords) -> Point:
    try:
        lat_d = coords[0]
        lat_deg = float(coords[1])
        lat_min = float(coords[2])
        lat_sec = float(coords[3])

        lon_d = coords[4]
        lon_deg = float(coords[5])
        lon_min = float(coords[6])
        lon_sec = float(coords[7])

        lat = lat_deg + lat_min/60 + lat_sec/3600
        lon = lon_deg + lon_min/60 + lon_sec/3600

        return Point(lat, lon)
    except ValueError:
        return None

def _get_point(soup: BeautifulSoup) -> Point:       # type: ignore
    list_points = soup.find_all('p')

    for p in list_points:
        text = p.get_text().split()
        for i, loc in enumerate(text):
            if loc == "Localització" or loc == "Localització:" :

                #if len(text[i+1:])<6:
                #     return None
                return (_get_coordenates(text[i+1:]))
            
def _download_monuments(start: int, feedback: bool = True) -> None:
    """Download monuments to FILENAME, starting by the chosen index for ..."""

    for i, link_type in enumerate(LINK_TYPES):
            for subclass in link_type[1]:
    
                monuments: str = ""

                response = requests.get(link_type[0] + subclass)
                soup = BeautifulSoup(response.content, "html.parser")
                places = soup.find_all ("li", class_= PLACE_TYPES[i])
                for place in places:
                    try:
                        link = place.find("a")
                        new_url = link.get("href")
                        try:
                            new_response = requests.get(new_url)
                        except: 
                            new_response= requests.get(new_url)
                        finally:
                            soup = BeautifulSoup(new_response.content,"html.parser")
                            point = _get_point(soup)

                            if point is not None:
                                line = (f"{link.text}, {point} \n")
                                monuments += line
    
                    except ConnectionResetError:
                        time.sleep(5)
                        pass

                with open (FILENAME, "a") as file:
                    file.write(monuments)
                with open(HEADER_FILENAME, "w") as header:
                    header.write(f"{False}\n{i}")
                if feedback:
                    print(f"Monument {i} has been sorted and added.")
                    
    with open(HEADER_FILENAME, "w") as header:
        header.write(f"{False}\n{i}")
    if feedback:
        print("All monuments' data has been gathered.")

     
                


def _load_monuments() -> Monuments:
    """Load monuments from a file."""
    assert os.path.exists(FILENAME)
    with open (FILENAME, 'r' ) as file:
         
    pickle_in = open(FILENAME, "rb")
    monuments = pickle.load(pickle_in)
    return monuments


def get_monuments() -> Monuments:
    """
    Get all monuments in the box.
    If filename exists, load monuments from the file.
    Otherwise, download monuments and save them to the file.
    """
    # Check if monuments are downloaded using the header file, then proceed to download only if necessary
    if not os.path.isfile(FILENAME):
        _download_monuments()
        
    return _load_monuments()




get_monuments()




"""
for i, link_type in enumerate(LINK_TYPES):
    for subclass in link_type[1]:
        response = requests.get(link_type[0] + subclass)
        soup = BeautifulSoup(response.content, "html.parser")
        places = soup.find_all ("li", class_= PLACE_TYPES[i])
        for place in places:
            link = place.find("a")
            links += f"{(link.get("href"), link.text)} \n"
            fecha = place.find('span', {'class' : 'localitzacio'})
            print(next)


        with open (filename, 'w') as file:
            print(links, file=file)
        file.close
"""

'''
ermites = soup.find_all("li", class_="ermita")
for ermita in ermites:
    link = ermita.find("a")
    print(link.get("href"), link.text)
'''