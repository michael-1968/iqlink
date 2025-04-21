from django.test import TestCase
from .helpers import checkTypeOccupation, shiftAngle

class HelperTests(TestCase):

    def test_basic(self):
        self.assertEqual(1 + 1, 2)

    def test_checkTypeOccupation(self):

        self.assertEqual(checkTypeOccupation('', 'X'), True)
        self.assertEqual(checkTypeOccupation('', 'Y'), True)
        self.assertEqual(checkTypeOccupation('', 'C'), True)
        self.assertEqual(checkTypeOccupation('', 'O'), True)
        self.assertEqual(checkTypeOccupation('', ''), True)
        self.assertEqual(checkTypeOccupation('X', 'X'), False)
        self.assertEqual(checkTypeOccupation('X', 'C'), True)
        self.assertEqual(checkTypeOccupation('X', 'Y'), False)
        self.assertEqual(checkTypeOccupation('X', 'O'), False)
        self.assertEqual(checkTypeOccupation('Y', 'X'), False)
        self.assertEqual(checkTypeOccupation('Y', 'O'), False)
        self.assertEqual(checkTypeOccupation('Y', ''), True)
        self.assertEqual(checkTypeOccupation('Y', 'C'), True)
        self.assertEqual(checkTypeOccupation('C', 'X'), True)
        self.assertEqual(checkTypeOccupation('C', 'O'), False)
        self.assertEqual(checkTypeOccupation('C', ''), True)

    def test_AngleShift(self):
        self.assertEqual(shiftAngle(0, 0, 0), (1, 0))
        self.assertEqual(shiftAngle(1, 1, 60), (2, 0))
        self.assertEqual(shiftAngle(2, 2, 120), (1, 1))
        self.assertEqual(shiftAngle(3, 2, 180), (2, 2))
        self.assertEqual(shiftAngle(4, 0, 240), (3, 1))
        self.assertEqual(shiftAngle(4, 0, 300), (4, 1))

        # self.assertEqual(shiftAngle(0, 0, 0), {'x': 1, 'y': 0})
        # self.assertEqual(shiftAngle(1, 1, 60), {'x': 2, 'y': 0})
        # self.assertEqual(shiftAngle(2, 2, 120), {'x': 1, 'y': 1})
        # self.assertEqual(shiftAngle(3, 2, 180), {'x': 2, 'y': 2})
        # self.assertEqual(shiftAngle(4, 0, 240), {'x': 3, 'y': 1})
        # self.assertEqual(shiftAngle(4, 0, 300), {'x': 4, 'y': 1})