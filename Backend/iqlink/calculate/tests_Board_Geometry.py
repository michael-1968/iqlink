from django.test import TestCase
from .board import Board
from .helpers import normalizeAngle, angleTransformFrontendBackend
from .figuredefinition import (
    Figuredefinition, Blau, Rot, Bordeaux, Orange, Dunkelgruen, Dunkelviolet, Violet,
    Gruen, Hellgruen, Gelb, Hellblau, Magenta, nameToGeometry
)
from .figures import Figures

class BoardTests(TestCase):

    def setUp(self):
        self.board = Board(Figures)

    def test_initial_field(self):
        # Testet, ob das Spielfeld korrekt initialisiert wurde
        expected_field = [[{'a': [0, 60, 120, 180, 240, 300], 't': ''} for y in range(4)] for x in range(6)]
        self.assertEqual(self.board.Field(), expected_field)

    def test_number_of_opens(self):
        # Testet die Anzahl der offenen Felder
        self.assertEqual(self.board.numberOfOpens(), 6 * 4 * 6)
        self.board.closeAnglesInBoard(3, 0, 180)
        self.board.closeAnglesInBoard(4, 0, 0)
        self.board.closeAnglesInBoard(2, 0, 120)
        self.assertEqual(self.board.numberOfOpens(), 6 * 4 * 6 - 3)

    def test_normalize_angles(self):
        # Testet die Normalisierung von Winkeln
        self.assertEqual(normalizeAngle(0), 0)
        self.assertEqual(normalizeAngle(60), 60)
        self.assertEqual(normalizeAngle(120), 120)
        self.assertEqual(normalizeAngle(180), 180)
        self.assertEqual(normalizeAngle(240), 240)
        self.assertEqual(normalizeAngle(300), 300)
        self.assertEqual(normalizeAngle(360), 0)
        self.assertEqual(normalizeAngle(-60), 300)
        self.assertEqual(normalizeAngle(720), 0)
        self.assertEqual(normalizeAngle(780), 60)
        self.assertEqual(normalizeAngle(-720), 0)
        self.assertEqual(normalizeAngle(3660), 60)
#        self.assertEqual(NormalizeAnglesList([0, 60, 780]), [0, 60, 60])

        with self.assertRaises(Exception) as context:
            normalizeAngle(45)
        self.assertTrue('NormalizeAngles: The angle is of incorrect value: 45' in str(context.exception))


    def test_close(self):
        # Testet die Close-Methode
        self.board.closeAnglesInBoard(0, 0, 60)
        self.assertNotIn(60, self.board.Field()[0][0]['a'])

        with self.assertRaises(Exception) as context:
            self.board.closeAnglesInBoard(6, 0, 60)
        self.assertTrue('Board.Close: Range Error x=6' in str(context.exception))

        with self.assertRaises(Exception) as context:
            self.board.closeAnglesInBoard(0, 4, 60)
        self.assertTrue('Board.Close: Range Error y=4' in str(context.exception))

        with self.assertRaises(Exception) as context:
            self.board.closeAnglesInBoard(0, 0, 45)
        self.assertTrue('Board.Close: The angle is of incorrect value: 45' in str(context.exception))

    def test_open(self):
        # Testet die Open-Methode
        self.board.closeAnglesInBoard(1, 1, 60)
        self.assertNotIn(60, self.board.Field()[1][1]['a'])
        self.board.openAnglesInBoard(1, 1, 60)
        self.assertIn(60, self.board.Field()[1][1]['a'])

        with self.assertRaises(Exception) as context:
            self.board.openAnglesInBoard(6, 0, 120)
        self.assertTrue('Board.Open: Range Error x=6' in str(context.exception))

        with self.assertRaises(Exception) as context:
            self.board.openAnglesInBoard(0, 4, 60)
        self.assertTrue('Board.Open: Range Error y=4' in str(context.exception))

        with self.assertRaises(Exception) as context:
            self.board.openAnglesInBoard(0, 0, 45)
        self.assertTrue('Board.Open: The angle is of incorrect value: 45' in str(context.exception))

class GeometryTests(TestCase):

    def test_initial_field(self):
        # Testet, ob das Spielfeld korrekt initialisiert wurde
        self.assertEqual(Blau.__str__(), "Blau - CYX^ - 3")
        self.assertEqual(Violet.__str__(), "Violet - XCX - 4")
        self.assertEqual(Hellblau.__str__(), "Hellblau - ^XOC - 2")
        self.assertEqual(Rot.__str__(), "Rot - ^XCC - 3")
        self.assertEqual(Orange.__str__(), "Orange - ^XCX - 3")
        self.assertEqual(Gelb.__str__(), "Gelb - ^COC^ - 2")
        self.assertEqual(Dunkelgruen.__str__(), "Dunkelgruen - XOC - 2")
        self.assertEqual(Hellgruen.__str__(), "Hellgruen - XOC - 2")
        self.assertEqual(Magenta.__str__(), "Magenta - ^XOC - 2")
        self.assertEqual(Bordeaux.__str__(), "Bordeaux - ^XCX - 3")
        self.assertEqual(Dunkelviolet.__str__(), "Dunkelviolet - ^XOC - 2")
        self.assertEqual(Gruen.__str__(), "Gruen - CYX^ - 3")
        
    def test_calculate_Useage(self):
        self.assertEqual(Blau.useage(), 3)
        self.assertEqual(Violet.useage(), 4)

    def test_nameToGeometry(self):
        self.assertEqual(nameToGeometry("Blau"), Blau)
        self.assertEqual(nameToGeometry("Rot"), Rot)
        self.assertEqual(nameToGeometry("Bordeaux"), Bordeaux)
        self.assertEqual(nameToGeometry("Orange"), Orange)
        self.assertEqual(nameToGeometry("Dunkelviolet"), Dunkelviolet)
        self.assertEqual(nameToGeometry("Gruen"), Gruen)
        self.assertEqual(nameToGeometry("Dunkelgruen"), Dunkelgruen)
        self.assertEqual(nameToGeometry("Hellgruen"), Hellgruen)
        self.assertEqual(nameToGeometry("Violet"), Violet)
        self.assertEqual(nameToGeometry("Gelb"), Gelb)
        self.assertEqual(nameToGeometry("Hellblau"), Hellblau)
        self.assertEqual(nameToGeometry("Magenta"), Magenta)
        with self.assertRaises(Exception) as context:
            nameToGeometry("Schwarz")
        self.assertTrue("Figure.openAngles: Problem with definition - name:Schwarz" in str(context.exception))
        
    def test_addTypeInfoToBoard(self):
        board = Board(Figures)
        # Test: Hinzufügen eines Typs
        board.addTypeInfoToBoard(0, 0, 'X')
        self.assertIn('X', board.field[0][0]['t'])

        # Test: Hinzufügen eines weiteren Typs
        board.addTypeInfoToBoard(0, 0, 'C')
        self.assertIn('C', board.field[0][0]['t'])

        # Test: Hinzufügen eines dritten Typs (sollte fehlschlagen)
        with self.assertRaises(Exception) as context:
            board.addTypeInfoToBoard(0, 0, 'Y')
        self.assertTrue('Board.addTypeInfoToBoard: Not more than two type attributes possible' in str(context.exception))
        self.assertEqual(len(board.field[0][0]['t']), 2)

        # Test: Entfernen eines Typs
        board.removeTypeInfoFromBoard(0, 0, 'X')
        self.assertNotIn('X', board.field[0][0]['t'])

        # Test: Entfernen eines nicht vorhandenen Typs (sollte fehlschlagen)
        with self.assertRaises(Exception) as context:
            board.removeTypeInfoFromBoard(0, 0, 'X')
        self.assertTrue('Board.removeTypeInfoFromBoard: The type attribute to be removed is not there' in str(context.exception))

class HelpersTest(TestCase):
    def tests_angleTransformFrontendBackend(self):
        self.assertEqual(angleTransformFrontendBackend(0, 0), {'rotX': 0, 'rotZ': 0})
        self.assertEqual(angleTransformFrontendBackend(0, 60), {'rotX': 0, 'rotZ': -60})
        self.assertEqual(angleTransformFrontendBackend(0, 300), {'rotX': 0, 'rotZ': -300})
        self.assertEqual(angleTransformFrontendBackend(180, 60), {'rotX': 180, 'rotZ': 60})
        self.assertEqual(angleTransformFrontendBackend(180, 240), {'rotX': 180, 'rotZ': 240})
        with self.assertRaises(Exception) as context:
            angleTransformFrontendBackend(60, 60)
        self.assertTrue('AngleTransformFrontendBackend: angle is neither 0 nor 180 - angle:60' in str(context.exception))


