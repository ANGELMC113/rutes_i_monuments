# Test kml creation


import test7_wip
import map_drawing


def test9() -> None:
    
    G = test7_wip.test7_A()

    kmlname1 = "map_kml1.kml"
    
    map_drawing.export_kml(kmlname1, G)
    

if __name__ == "__main__":
    test9()


# 

# WORK IN PROGRESS