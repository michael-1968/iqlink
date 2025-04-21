from django.test import TestCase
from .figures import Figures
from .calculations.calculation import Calculation
from .calculations.best3FoM import Best3FoM
from .helpers import listOfFigures, shuffleListOfFigures

class OptimierungenAlsTests(TestCase):

    def Xtest_Optimierung(self):
        for ix in range(100):
            shuffleListOfFigures()
            cw = Best3FoM('keineFarbe')
            cw.figures.deleteFiguresAndBoard()
            # Problem 61:
            cw.figures.loadSetup(
                {"0": {"name": "Gruen", "position": {"X": 4, "Y": 3}, "rotation": {"rotX": 180, "rotY": 0, "rotZ": 0}}, "1": {"name": "Hellgruen", "position": {"X": 4, "Y": 2}, "rotation": {"rotX": 0, "rotY": 0, "rotZ": 120}}, "2": {"name": "Magenta", "position": {"X": 1, "Y": 1}, "rotation": {"rotX": 360, "rotY": 0, "rotZ": -60}}, "3": {"name": "Dunkelviolet", "position": {"X": 0, "Y": 1}, "rotation": {"rotX": 180, "rotY": 0, "rotZ": -60}}, "4": {"name": "Hellblau", "position": {"X": 0, "Y": 3}, "rotation": {"rotX": 180, "rotY": 0, "rotZ": -60}}}
            )
    #        self.assertEqual(cw.figures.get_NamesOfAllFigures(), ['Hellgruen', 'Magenta', 'Hellblau', 'Dunkelviolet', 'Gruen', 'Blau'])

            solver = Calculation(cw)
            solver.resetObjectValues()

            res = solver.solve()
            print ("Communication-solve 1: ", ix, listOfFigures(), res, solver.numberOfObjects)

            cw.figures.deleteFiguresAndBoard()
            # Geschwindigkeitstest 2:
            cw.figures.loadSetup(
                {"0": {"name": "Blau", "position": {"X": 5, "Y": 3}, "rotation": {"rotX": 0, "rotY": 0, "rotZ": 180}}, "1": {"name": "Rot", "position": {"X": 4, "Y": 2}, "rotation": {"rotX": 180, "rotY": 0, "rotZ": 60}}, "2": {"name": "Gelb", "position": {"X": 2, "Y": 3}, "rotation": {"rotX": 180, "rotY": 0, "rotZ": 120}}, "3": {"name": "Orange", "position": {"X": 2, "Y": 0}, "rotation": {"rotX": 180, "rotY": 0, "rotZ": 0}}, "4": {"name": "Dunkelgruen", "position": {"X": 1, "Y": 2}, "rotation": {"rotX": 0, "rotY": 0, "rotZ": 180}}}            )
            solver = Calculation(cw)
            res = solver.solve()
            print ("Communication-solve: ", ix, listOfFigures(), res, solver.numberOfObjects)

            with open('results.txt', 'a') as file:
                file.write(f"{listOfFigures()} - {res} - {solver.numberOfObjects}\n")


        # Geschwindigkeitstest:
        # cw.figures.loadSetup(
        #     {"0": {"name": "Hellgruen", "position": {"X": 4, "Y": 0}, "rotation": {"rotX": 180, "rotY": 0, "rotZ": 180}}, "1": {"name": "Blau", "position": {"X": 5, "Y": 3}, "rotation": {"rotX": 0, "rotY": 0, "rotZ": 180}}, "2": {"name": "Rot", "position": {"X": 4, "Y": 2}, "rotation": {"rotX": 180, "rotY": 0, "rotZ": 60}}, "3": {"name": "Gelb", "position": {"X": 2, "Y": 3}, "rotation": {"rotX": 180, "rotY": 0, "rotZ": 120}}, "4": {"name": "Orange", "position": {"X": 2, "Y": 0}, "rotation": {"rotX": 180, "rotY": 0, "rotZ": 0}}}
        # )
