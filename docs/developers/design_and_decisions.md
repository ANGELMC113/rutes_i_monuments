# Informació de desenvolupament de Rutes i Monuments

Com de costum, és recomanable tenir un bon nivell d'anglès per programar. A més, els docstrings i els identificadors també s'han escrit en anglès.

### Aspectes generals

`feedback: bool` és un paràmetre que trobem al llarg de tot el programa. Sempre fa el mateix, i sempre està per defecte establert a True en el mòdul `generics.py`. Escriu a la consola de comandes uns missatges que donen una idea a l'usuari sobre què està fent el programa. És recomanable deixar el `feedback` activat, però podem establir `DEFAULT_FEEDBACK` a `False` i es desactivarà a tot arreu.

### Estructura del programa

El programa consta de 8 mòduls: generics, segments, map_drawing, clustering, graphmaker, monuments, routes i rutes_i_monuments. Tot seguit es resumeix què fa cadascun.

#### `generics.py`

Conté les definicions de `Point`, `Segment`, `Segments` i `Box`, estableix el valor de `DEFAULT_FEEDBACK` i dues funcions genèriques, per donar un error si una extensió d'un arxiu és incorrecta i per retornar la distància entre dos objectes de la classe `Point`.

`Box` conté una funció que retorna els punts que la defineixen com un string. Aquest string té invertit el format (és longitud - latitud) i serveix per la web des d'on es descarreguen els segments. Aquest mateix string es desa al .json de cada arxiu de segments per identificar-lo. A l'apartat de presa de decisions s'entra en detall respecte d'això.

També conté el nom de l'arxiu on es desaran les dades dels monuments.

#### `segments.py`

Conté les funcions necessàries per descarregar i carregar segments. Els segments es desen a arxius .dat, i cadascun és una línia. Es generen segments de dos punts a partir dels segments descarregats de la web, de múltiples punts, després de filtrar les dades. A l'apartat de presa de decisions s'entra en detall respecte d'això. La funció `get_segments()` és l'única que necessita l'usuari, ja que s'encarrega de decidir què s'ha de fer i donar un error si cal. Protegeix l'arxiu establert a `generics.py` per desar els monuments.

#### `map_drawing.py`

Conté les funcions que exporten arxius png i KML de les dades. L'usuari té accés a `export_kml()` i `export_png_map()`. Aquesta segona crida una altra funció segons les dades que ha donat l'usuari: graf, segments o tupla de segments i punts. Està pensada per permetre generar mapes diversos i no estar limitada només a grafs, ja que no hi ha problema amb treballar amb segments. L'entrada de punts permet passar els centroides i comprovar com el graf és igual que el mapa generat a partir de centroides i els segments que els uneixen. Això, en principi, no ho hauria de demanar l'usuari.

#### `clustering.py`

Llibreria enfocada a `graphmaker.py`, conté les funcions que permeten fer l'agrupament de punts. La funció `cluster()` no està pensada per ser usada per l'usuari ja que, a la pràctica, fer el graf és més simple d'entendre, alhora que més útil, i en essència per l'usuari, seran el mateix. Bàsicament, l'usuari ha de fer directament el graf sense demanar res a `clustering.py`.

#### `graphmaker.py`

Conté les funcions que permeten fer el graf inicial a partir dels segments i les constants que s'han col·locat, per defecte, pel nombre de clusters i per l'angle mínim entre les arestes d'un node amb dos veïns. La funció `make_graph()` s'encarrega de cridar les altres, segons toqui, per fer-ho tot.

#### `monuments.py`

S'encarrega de la descàrrega i càrrega dels monuments. La funció `get_monuments()` crida a les altres i dona errors, segons toca. També es defineixen els tipus de monuments i els enllaços que s'accediran de Catalunya Medieval. Funciona d'una forma similar a `segments.py`, també desa les dades a un arxiu .dat. Una diferència és que la funció no està pensada per usada, ja que no és paràmetre de cap altra funció. El que sí que pot fer l'usuari és executar `monuments.py` per descarregar les dades dels monuments, procés que és bastant lent.

#### `routes.py`

Conté les funcions que permeten crear l'arbre de les rutes a partir d'un graf i una caixa. La funció `find_routes()` crida a les altres segons toca. Es filtren els monuments de l'arxiu usant `get_monuements()`, s'aproximen als nodes del graf, s'aproxima el punt inicial i s'afegeixen valors als nodes amb monuments per poder-los distingir.

#### `rutes_i_monuments.py`

Ajunta totes les funcions pensades per a l'usuari i n'afegeix algunes més, de simples.

## Presa de decisions

### Descàrrega de dades

Descarregar els segments i els monuments pot ser bastant lent. Segons la mida de la `Box`, les característiques de l'ordinador on executem el programa i la qualitat de la connexió a internet, pot prendre bastants minuts. Encara que el programa estigui pensat per calcular rutes per anar a peu per senderistes, que normalment no seran massa llargues, s'ha de tractar que descarregar les dades es faci un sol cop.

Per aquest motiu, els documents on es desen les dades, els .dat, estan protegits, com s'ha explicat anteriorment. S'ha fet que cada arxiu .dat estigui acompanyat d'un arxiu .json amb metadades.

Aquest arxiu a part té diverses utilitats que ajuden a l'usuari a no perdre el control de les dades.

En el cas dels segments, desen 3 variables: les coordenades de la `Box` (en format longitud, latitud), un booleà que indica si s'han acabat de descarregar les dades d'OpenStreetMap i un natural que indica la última pàgina descarregada.

En el cas dels monuments, desen el mateix booleà i tres nombres que són els índexs de l'últim monument descarregat.

Aquestes metadades permeten diverses comprovacions. D'una banda, si l'usuari fa un `get_segments()` (on un paràmetre sempre haurà de ser un arxiu .dat), el programa mai hauria de sobreescriure les dades si aquest arxiu ja existeix. Es poden donar diferents casuístiques segons els paràmetres que passem:

- Donem un `filename` que no existeix i no donem `Box`: salta error perquè no es pot saber què volem descarregar.
- Donem un `filename` que no existeix i sí que donem una `Box`: el programa genera un nou arxiu .dat, que a partir d'ara serà exclusiu per aquesta `Box`. Segueix el procés de descarregar i carregar les dades.
- Donem un filaneme que ja existeix, i una `Box` que no correspon: salta error perquè aquest `filename` no es correspon a la caixa i no permetem que l'usuari pugui sobreescriure sense voler les dades del .dat.
- Donem un `filename` que ja existeix i la seva `Box` corresponent (exactament la mateixa): el programa segueix amb la càrrega / descàrrega de les dades de l'arxiu.
- Donem un `filename` que ja existeix i no donem cap `Box`: el programa segueix amb la càrrega / descàrrega de les dades.

D'aquesta manera, no permetem que un arxiu .dat contingui dades de caixes diferents o sigui esborrat pel programa. Si l'usuari vol canviar les dades d'un arxiu .dat, haurà d'esborrar-lo manualment (a través de la terminal o de l'explorador d'arxius).

Tant pels segments com pels monuments la descàrrega / càrrega de dades és automàtica. Sempre es mirarà si el booleà del .json està a True, i si no és així, es cridarà a la funció corresponent, passant l'índex del primer element que cal descarregar.

Això permet parar la descàrrega i seguir-la després, cosa que fa el programa resistent a situacions on es pugui perdre la connexió a internet. Però, per tal que això funcioni, és important que l'arxiu .dat es vagi escrivint a poc a poc. És per això que els segments es descarreguen pàgina a pàgina i els monuments un per un.

Pels segments es fa el següent procés: descarregar la pàgina, ordenar els segments segons temps, eliminar els que tenen "temps negatiu" (més avall s'entra en detalls), apuntar els segments al .dat i, per últim, actualitzar el .json amb el nombre d'aquesta pàgina. És quan no queden elements per descarregar que hem arribat a l'última pàgina i, per tant, hem acabat i s'estableix el booleà del .json a True.

Pels monuments es descarrega la pàgina de cadascun i es busquen les seves coordenades. Certament, descarregar els monuments així és molt lent, perquè s'ha d'accedir a al voltant de tres mil urls, probablement hi ha mètodes més eficients.

És important destacar que aquesta protecció no es dona amb els altres arxius: els mapes .png i els .kml se sobreescriuen quan demanem fer l'exportació. En conjunt, això permet executar el programa tants cops com vulguem, sense haver de descarregar les dades cada cop, i sense generar imatges semblants entre si.

### Filtre de les dades

Les dades descarregades, en mapejar-les, donen resultats diversos: veiem línies rectes que travessen el rectangle de banda a banda, algunes que uneixen punts molt llunyans, etc. Això, es pot traslladar al graf, cosa que resulta en arestes que es creuen, sense haver-hi cap node, fet que no és coherent a un mapa. En la immensa majoria dels casos la solució és tan senzilla com limitar la longitud dels segments inicials, dels que descarreguem. Al nostre programa es comprova amb `haversine()` que la distància d'un segment és menor a 50 metres (valor assignat a una constant a `segments.py`) abans de carregar-lo. És un valor, generalment parlant, arbitrari, però és difícil acotar-lo perquè els segments tenen comportaments impredictibles: a vegades són molt petits i es generen en dècimes de segon, i a vegades ocupen kilòmetres. Igualment, perdre un segment amb una longitud de 50 metres normalment no causarà problemes perquè per allà on passi segurament passaren altres segments.

Aquest filtre no suposa una diferència notable en el temps que triga el programa en carregar les dades, perquè el seu cost és lineal, i per això no s'ha mogut a la descàrrega. L'avantatge és que podem canviar la distància màxima sense haver de tornar a descarregar res.

A part d'aquest filtre, a l'hora de descarregar s'eliminen els segments on el temps del punt final és anterior al temps del punt inicial (cosa que implica que hi ha algun error).