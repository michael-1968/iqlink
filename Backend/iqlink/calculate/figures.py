
import json
from .figure import Figure
from .board import Board
from .helpers import normalizeAngle, angleTransformFrontendBackend, listOfFigures
from .figuredefinition import nameToGeometry

testdata = json.loads(
    '{"3": {"name": "Blau", "position": {"X": 3, "Y": 2}, "rotation": {"rotX": 180, "rotY": 0, "rotZ": 360}}, "5": {"name": "Orange", "position": {"X": 0, "Y": 3}, "rotation": {"rotX": 0, "rotY": 0, "rotZ": 60}}, "0": {"name": "Violet", "position": {"X": 1, "Y": 1}, "rotation": {"rotX": 0, "rotY": 0, "rotZ": 0}}, "1": {"name": "Gruen", "position": {"X": 1, "Y": 1}, "rotation": {"rotX": 180, "rotY": 0, "rotZ": 240}}, "6": {"name": "Gelb", "position": {"X": 5, "Y": 2}, "rotation": {"rotX": 0, "rotY": 0, "rotZ": 0}}, "4": {"name": "Magenta", "position": {"X": 4, "Y": 1}, "rotation": {"rotX": 0, "rotY": 0, "rotZ": 60}}, "2": {"name": "Rot", "position": {"X": 2, "Y": 1}, "rotation": {"rotX": 180, "rotY": 0, "rotZ": -180}}}'
    )
testdata_ohneGruen = json.loads(
    '{"2": {"name": "Blau", "position": {"X": 3, "Y": 2}, "rotation": {"rotX": 180, "rotY": 0, "rotZ": 360}}, "4": {"name": "Orange", "position": {"X": 0, "Y": 3}, "rotation": {"rotX": 0, "rotY": 0, "rotZ": 60}}, "0": {"name": "Violet", "position": {"X": 1, "Y": 1}, "rotation": {"rotX": 0, "rotY": 0, "rotZ": 0}}, "5": {"name": "Gelb", "position": {"X": 5, "Y": 2}, "rotation": {"rotX": 0, "rotY": 0, "rotZ": 0}}, "3": {"name": "Magenta", "position": {"X": 4, "Y": 1}, "rotation": {"rotX": 0, "rotY": 0, "rotZ": 60}}, "1": {"name": "Rot", "position": {"X": 2, "Y": 1}, "rotation": {"rotX": 180, "rotY": 0, "rotZ": -180}}}'
    )


class Figures():
    def __init__(self):
        self.figures = []
        self.board = Board(self)
        self.nameOfFigureToBePlaced = ''
    
    def figuresToBePlaced(self):
        returnlist = listOfFigures()
        for fx in self.figures:
            returnlist.remove(fx.name)
        return returnlist

    # note the MINUS for rotation around z-axis as the x-axis in the frontend is mirrored
    # and hence the rotation definition inverse. 
    def loadSetup(self, data):
        for ix in range(len(data)):
            name = data[str(ix)]['name']
            x = data[str(ix)]['position']['X']
            y = data[str(ix)]['position']['Y']
            rx = normalizeAngle(data[str(ix)]['rotation']['rotX'])
            rz = normalizeAngle(data[str(ix)]['rotation']['rotZ'])
            transformedAngles = angleTransformFrontendBackend(rx, rz)

            fx = Figure(nameToGeometry(name), x, y, transformedAngles['rotX'], transformedAngles['rotZ'], self)
            self.nameOfFigureToBePlaced = name
            fx.place()

#            self.figures.append(Figure(nameToGeometry(name), x, y, transformedAngles['rotX'], transformedAngles['rotZ'], self))

    def get_figures(self):
        return self.figures 
    
    def get_NamesOfAllFigures(self):
        names = []
        for ix in range(len(self.figures)):
            names.append(self.figures[ix].name)
        return names
        
    def get_SetupOfAllFigures(self):
        setup = {}
        for ix in range(len(self.figures)):
            setup[str(ix)] = self.figures[ix].get_setup()
        return setup
    
    def addFigure(self, figure):
        self.figures.append(figure)

    def removeFigure(self, figure):
        self.figures.remove(figure)
    
    def deleteFigures(self):
        self.figures = []
        return True    
    
    def deleteFiguresAndBoard(self):
        self.deleteFigures()
        self.board = Board(self)
        return True
    
    def checkSetup(self):   
        message = ''
        for fx in self.figures:
            try:
                fx.unPlace()
            finally:
                pass
            result = fx.fits()
            if result != True:
                if message != '':
                    message += ', '
                message += fx.name
            try:
                fx.place()
            finally:
                pass
        if message != '':
            return {"status": "Not OK", "message": "Problems with " + message}
        return {"status": "OK", "message": ""}
    


