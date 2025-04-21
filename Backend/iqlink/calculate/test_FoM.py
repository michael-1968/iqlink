from django.test import TestCase
from .figures import Figures

class FoMTests(TestCase):

    def test_basic(self):
        self.assertEqual(1 + 1, 2)

    def test_FoM(self):
        print('Start test_FoM')
        figures = Figures()
        figures.loadSetup(
            {"0": {"name": "Hellgruen", "position": {"X": 2, "Y": 0}, "rotation": {"rotX": 0, "rotY": 0, "rotZ": 0}}, "1": {"name": "Magenta", "position": {"X": 0, "Y": 2}, "rotation": {"rotX": 0, "rotY": 0, "rotZ": 240}}, "2": {"name": "Hellblau", "position": {"X": 2, "Y": 2}, "rotation": {"rotX": 0, "rotY": 0, "rotZ": 0}}, "3": {"name": "Dunkelviolet", "position": {"X": 5, "Y": 0}, "rotation": {"rotX": 0, "rotY": 0, "rotZ": -120}}, "4": {"name": "Gruen", "position": {"X": 4, "Y": 2}, "rotation": {"rotX": 0, "rotY": 0, "rotZ": 60}}, "5": {"name": "Blau", "position": {"X": 2, "Y": 1}, "rotation": {"rotX": 0, "rotY": 0, "rotZ": 0}}}
        )
        self.assertEqual(figures.get_NamesOfAllFigures(), ['Hellgruen', 'Magenta', 'Hellblau', 'Dunkelviolet', 'Gruen', 'Blau'])
        self.assertEqual(figures.board.numberOfPotentialFreePlaces_3(), 16)
        self.assertEqual(figures.board.numberOfPotentialFreePlaces_2(), 18)
        self.assertEqual(figures.board.numberOfPotentialFreePlaces_2a(), 16)
        self.assertEqual(figures.board.numberOfPotentialFreePlaces_4(), (6, 6, 8))
        self.assertEqual(figures.board.numberOfNeededPlaces(), (2, 8, 8))

    def test_FoM2(self):
        figures = Figures()
        figures.loadSetup(
            {"0": {"name": "Violet", "position": {"X": 4, "Y": 1}, "rotation": {"rotX": 0, "rotY": 0, "rotZ": 0}}, "1": {"name": "Rot", "position": {"X": 5, "Y": 3}, "rotation": {"rotX": 0, "rotY": 0, "rotZ": 0}}, "2": {"name": "Gruen", "position": {"X": 1, "Y": 0}, "rotation": {"rotX": 0, "rotY": 0, "rotZ": 60}}, "3": {"name": "Dunkelgruen", "position": {"X": 3, "Y": 2}, "rotation": {"rotX": 0, "rotY": 0, "rotZ": 180}}, "4": {"name": "Magenta", "position": {"X": 5, "Y": 0}, "rotation": {"rotX": 180, "rotY": 0, "rotZ": 120}}}
        )
        self.assertEqual(set(figures.get_NamesOfAllFigures()), set(['Dunkelgruen', 'Magenta', 'Rot', 'Violet', 'Gruen']))
        self.assertEqual(figures.board.numberOfPotentialFreePlaces_3(), 19)
        self.assertEqual(figures.board.numberOfPotentialFreePlaces_2(), 19)
        self.assertEqual(figures.board.numberOfPotentialFreePlaces_2a(), 19)
        self.assertEqual(figures.board.numberOfPotentialFreePlaces_4(), (10, 5, 6))
        self.assertEqual(figures.board.numberOfNeededPlaces(), (4, 9, 8))
        print('End test_FoM')
