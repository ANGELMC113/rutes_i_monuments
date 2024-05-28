# Test kml creation


import test7
import map_drawing


def test9() -> None:
    
    G = test7.test7()

    kmlname1 = "map_kml1.kml"
    
    map_drawing.export_kml(kmlname1, G)
    

if __name__ == "__main__":
    test9()


# Successfully exports a kml file.