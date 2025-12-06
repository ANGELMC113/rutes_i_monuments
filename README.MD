# Rutes i Monuments

Aquest programa permet visualitzar sobre un mapa les rutes de cotxes i senderistes i les posicions de monuments històrics d'interès. Ho fa mitjançant algorismes de grafs i de *clustering*, i a partir de dades accessibles públicament.

És una solució a un problema proposat a l'assignatura d'Algorísmia i Programació II (AP2) del Grau en Ciència i Enginyeria de Dades (GCED) de la Universitat Politècnica de Catalunya (UPC). Podeu veure el [repositori del professorat](https://github.com/jordi-petit/ap2-rutes-i-monuments-2024).

Específicament, el programa permet:
- Obtenir les rutes dels senderistes en una regió geogràfica
- Inferir un mapa (un graf) a partir de les rutes
- Obtenir les coordenades de monuments medievals
- Trobar rutes òptimes per arribar a monuments medievals en el graf inferit
- Visualitzar els mapes resultants en 2D i 3D

Podeu consultar els tutorials i la guia d'usuari a [docs/users/user_guide.md](./docs/users/user_guide.md).

També podeu accedir a la informació per a desenvolupadors, sobre el disseny del programa i la presa de decisions ([docs/developers/design_and_decisions.mc](./docs/developers/design_and_decisions)), i el testing ([docs/developers/tests.md](./docs/developers/tests.md)).

## Fonts

Les dades dels segments i els mapes s'han extret d'[OpenStreetMap](https://www.openstreetmap.org/copyright), una plataforma *open source* de mapes molt important.

Les dades dels monuments s'han extret de [Catalunya Medieval](https://www.catalunyamedieval.es/), una pàgina creada Ricard Ballo i Montserrat Tañá amb imformació bastant completa sobre monuments medievals a Catalunya.

## Autors

Implementació del conjunt del programa:

- Nuria Díaz
- Ángel Morales (angelmoralescirera@proton.me)

Context de la pràctica i algunes funcions bàsiques:

- Jordi Cortadella
- Pau Fernández
- Laia Mogas
- Jordi Petit

Universitat Politècnica de Catalunya, 2024
