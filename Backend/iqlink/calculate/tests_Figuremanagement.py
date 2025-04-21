from django.test import TestCase
from .figuredefinition import (
    Blau, Rot, Bordeaux, Orange, Dunkelgruen, Dunkelviolet, Violet,
    Gruen, Hellgruen, Gelb, Hellblau, Magenta
)
from .figure import Figure
from .figures import Figures, testdata, testdata_ohneGruen
from .movements import Movements


class FigureManagementTests(TestCase):

    def setUp(self):
        self.Anzahl = 4

    def test_basics(self):
        calculation = Figures()
        calculation.loadSetup(testdata)
        self.assertEqual(len(calculation.get_figures()), 7)
        self.assertEqual(str(calculation.get_figures()[0]), "Violet - x:1, y:1, rx:0, rz:0, Fits: False")
        self.assertEqual(str(calculation.get_figures()[1]), "Gruen - x:1, y:1, rx:180, rz:240, Fits: False")
        self.assertEqual(str(calculation.get_figures()[2]), "Rot - x:2, y:1, rx:180, rz:180, Fits: False")
        self.assertEqual(str(calculation.get_figures()[3]), "Blau - x:3, y:2, rx:180, rz:0, Fits: False")
        self.assertEqual(str(calculation.get_figures()[4]), "Magenta - x:4, y:1, rx:0, rz:-60, Fits: False")
        self.assertEqual(str(calculation.get_figures()[5]), "Orange - x:0, y:3, rx:0, rz:-60, Fits: False")
        self.assertEqual(str(calculation.get_figures()[6]), "Gelb - x:5, y:2, rx:0, rz:0, Fits: False")

    # def test_fit(self):
    #     calculation = FigureManagement()
    #     calculation.loadSetup(testdata)
    #     for figure in calculation.get_figures():
    #         self.assertEqual(figure.fits(), False)
    #         figure.place()

    def test_findAPlace(self):
        movemements =  Movements()
        calculation = Figures()
        calculation.loadSetup(testdata)
        # for figure in calculation.get_figures():
        #     self.assertEqual(figure.fits(), True)
        #     figure.place()

        dunkelgruen = Figure(Dunkelgruen, 0, 1, 0, 0, calculation)
        ix = 0
        while True:
            ix += 1
            mx = movemements.nextMove()
            if mx.get('status', '') == 'finished':
                break
            dunkelgruen.x = mx['x']
            dunkelgruen.y = mx['y']
            dunkelgruen.rx = mx['rx']
            dunkelgruen.rz = mx['rz']
            if dunkelgruen.fits():
                break
        self.assertNotEqual(ix, 289) 

    def test_Scan(self):
        calculation = Figures()
        calculation.loadSetup(testdata)
        for figure in calculation.get_figures():
            self.assertEqual(figure.fits(), False)

        dunkelgruen = Figure(Dunkelgruen, 0, 1, 0, 0, calculation)
        self.assertEqual(dunkelgruen.scan(), True)
        self.assertEqual(dunkelgruen.x, 1)
        self.assertEqual(dunkelgruen.y, 0)
        magenta = Figure(Magenta, 0, 0, 0, 0, calculation)
        self.assertEqual(magenta.scan(), True)
        self.assertEqual(magenta.x, 1)
        self.assertEqual(magenta.y, 0)

    def test_ListOfFigures(self):
        calculation = Figures()
        calculation.loadSetup(testdata_ohneGruen)
        self.assertEqual(len(calculation.get_figures()), 6)
        hellgruen = Figure(Hellgruen, 2, 3, 0, 180, calculation)
        self.assertEqual(hellgruen.fits(), True)
        self.assertEqual(len(calculation.get_figures()), 6)
        hellgruen.place()
        self.assertEqual(len(calculation.get_figures()), 7)
        hellgruen.unPlace()
        self.assertEqual(len(calculation.get_figures()), 6)


    def test_place_ListOfPlacedFigures(self):
        figuremanagement = Figures()
        self.assertEqual(set(figuremanagement.figuresToBePlaced()), set(["Rot", "Blau", "Bordeaux", "Orange", "Dunkelviolet", "Dunkelgruen", "Gruen", "Hellgruen", "Violet", "Gelb", "Hellblau", "Magenta"]))
        rot = Figure(Rot, 1, 1, 0, 0, figuremanagement)
        rot.place()
        self.assertEqual(set(figuremanagement.figuresToBePlaced()), set(["Blau", "Bordeaux", "Orange", "Dunkelviolet", "Dunkelgruen", "Gruen", "Hellgruen", "Violet", "Gelb", "Hellblau", "Magenta"]))
        blau = Figure(Blau, 0, 2, 0, 0, figuremanagement)
        blau.place()
        self.assertEqual(set(figuremanagement.figuresToBePlaced()), set(["Bordeaux", "Orange", "Dunkelviolet", "Dunkelgruen", "Gruen", "Hellgruen", "Violet", "Gelb", "Hellblau", "Magenta"]))
        orange = Figure(Orange, 5, 2, 0, 0, figuremanagement)
        orange.place()
        self.assertEqual(set(figuremanagement.figuresToBePlaced()), set(["Bordeaux", "Dunkelviolet", "Dunkelgruen", "Gruen", "Hellgruen", "Violet", "Gelb", "Hellblau", "Magenta"]))
        orange.unPlace()
        self.assertEqual(set(figuremanagement.figuresToBePlaced()), set(["Bordeaux", "Orange", "Dunkelviolet", "Dunkelgruen", "Gruen", "Hellgruen", "Violet", "Gelb", "Hellblau", "Magenta"]))
        blau.unPlace()
        self.assertEqual(set(figuremanagement.figuresToBePlaced()), set(["Blau", "Bordeaux", "Orange", "Dunkelviolet", "Dunkelgruen", "Gruen", "Hellgruen", "Violet", "Gelb", "Hellblau", "Magenta"]))




