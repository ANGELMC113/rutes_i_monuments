# Rutes i monuments

Aquest projecte és una implementació de la pràctica homònima d'AP2 del GCED. El programa us permet:

- Obtenir les rutes dels senderistes en una regió geogràfica.
- Inferir un mapa (un graf) a partir de les rutes.
- Obtenir les coordenades de monuments medievals.
- Trobar rutes òptimes per arribar a monuments medievals en el graf inferit.
- Visualitzar els mapes resultants en 2D i 3D. 

La informació d'aquest README s'ha distribuït segons el vostre interès pel projecte.
- Manual d'usuari: funcionalitats del programa, com es fa servir...
- Informació per a *developers*: presa de decisions, testing...


## Manual d'usuari

És necessari tenir connexió a internet per fer servir el programa.

Com a pas previ a qualsevol execució de codi, assegureu-vos que us trobeu al directori del projecte, on es troba aquest arxiu README.md, i feu servir la comanda `cd` per arribar-hi (podeu trobar més informació a [Wikipedia](https://en.wikipedia.org/wiki/Cd_(command))).


...
DEFAULT_FEEDBACK a main.py indica si volem que els programa ens vagi actualitzant conforme s'executa. Podem establir-la a False per desactivar els missatges a la consola.
...

...
Els colors disponibles per fer exportar mapes en PNG són els del mòdul Pillow.
https://stackoverflow.com/questions/54165439/what-are-the-exact-color-names-available-in-pils-imagedraw
...



### Instal·lació

És necessari tenir instalades 8 llibreries. Podeu consultar-les a `requirements.txt`.

Per instal·lar-les, podeu fer servir la comanda `python -m pip install -r requirements.txt`.

## Informació de desenvolupament

Com de costum, és recomanable tenir un bon nivell d'anglès per programar. A més, els docstrings i els identificadors també s'han escrit en anglès.

### Testing
...




## Autors

Implementació del conjunt del programa:

- Ángel Morales
- Nuria Díaz

Context de la pràctica i algunes funcions bàsiques:

- Laia Mogas
- Jordi Cortadella
- Pau Fernández
- Jordi Petit

Universitat Politècnica de Catalunya, 2024