from dataclasses import dataclass
from typing import TypeAlias
from bs4 import BeautifulSoup
import requests
import pickle
import os
from segments import *


@dataclass
class Point:
    lat: float
    lon: float
  
class Monument:
     name: str
     location: Point



filename = 'archive1.txt'
Monuments: TypeAlias = list[Monument]

militar =  "https://www.catalunyamedieval.es/edificacions-de-caracter-militar/"
civil = "https://www.catalunyamedieval.es/edificacions-de-caracter-civil/"
religios = "https://www.catalunyamedieval.es/edificacions-de-caracter-religios/"
altres = "https://www.catalunyamedieval.es/altres-llocs-dinteres/"

links_types: list[tuple[str, list[str]]] = [
                                            [militar, ["castells/", "epoca-carlina/", "muralles/", "torres/"]], 
                                            [civil, ["cases-fortes/", "palaus/", "ponts/", "torres-colomer/"]],
                                            [religios, ["basiliques/", "catedrals/", "ermites/", "esglesies/", "esglesies-fortificades", "monestirs/"]],
                                            [altres, ['']]
                                        ]

place_types: list[list[str]] = [
                                ["castell", "epoca carlina", "muralla", "torre"],
                                ["casa forta", "palau", "pont", "torre colomer"],
                                ["basilique", "catedral", "ermita", "esglesia", "esglesia fortificada", "monestir"],
                                ["altres"]
                                ]

def save_monuments (monuments:Monuments, filename:str) -> None:
    """Save monuments into a file"""
    pickle_out = open(filename, "wb")
    pickle.dump(monuments, pickle_out)
    pickle_out.close()


def _get_coordenates(coords):
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

def _get_monuments(soup: str):
    list_points = soup.find_all('p')

    for p in list_points:
        text = p.get_text().split()
        for i, loc in enumerate(text):
            if loc == "Localització" or loc == "Localització:" :

                if len(text[i+1:])<6:
                     return None
                return (_get_coordenates(text[i+1:]))
            
def download_monuments()->Monuments:
    monuments: Monuments = []

    for i, link_type in enumerate(links_types):
            for subclass in link_type[1]:
                response = requests.get(link_type[0] + subclass)
                soup = BeautifulSoup(response.content, "html.parser")
                places = soup.find_all ("li", class_= place_types[i])
                for place in places:
                    link = place.find("a")
                    new_url = link.get("href")
                    new_response = requests.get(new_url)
                    soup = BeautifulSoup(new_response.content,"html.parser")
                    point = _get_monuments(soup)
                    print(link.text)
                    print (point)
                    if point is not None:
                        if len(monuments)>50:
                            break
                        monuments.append(Monument(link.text, point))
                    print (monuments)
    save_monuments(monuments, filename)
    return monuments            
                


def load_monuments(filename: str) -> Monuments:
    """Load monuments from a file."""
    assert os.path.exists(filename) #, f'Error: {filename} does not exist'

    pickle_in = open(filename, "rb")
    monuments = pickle.load(pickle_in)
    return monuments

def get_monuments(filename: str) -> Monuments:
    """
    Get all monuments in the box.
    If filename exists, load monuments from the file.
    Otherwise, download monuments and save them to the file.
    """
    path = os.getcwd() + "/" + filename
    
    if os.path.exists(path):
        return load_monuments(filename)

    else:
        return download_monuments(filename)

