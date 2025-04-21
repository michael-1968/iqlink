from django.test import TestCase
from .movements import Movements

class TestMovements(TestCase):

    def setUp(self):
        x1 = 3
        y1 = 1

    def test_basics(self):
        movement = Movements()

        self.assertEqual(movement.generateLinearMovements(6), [0, 1, 2, 3, 4, 5])
        self.assertEqual(movement.generateLinearMovements(6, 3), [3, 4, 5, 0, 1, 2])

        self.assertEqual(movement.get_allMovements()['x'], [0, 1, 2, 3, 4, 5])
        self.assertEqual(movement.get_allMovements()['y'], [0, 1, 2, 3])
        self.assertEqual(movement.get_allMovements()['rx'], [0, 180])
        self.assertEqual(movement.get_allMovements()['rz'], [0, 60, 120, 180, 240, 300])

        movement.shuffle(movement.get_allMovements()['x'])
        self.assertNotEqual(movement.get_allMovements()['x'], [0, 1, 2, 3, 4, 5])
        self.assertEqual(movement.get_allMovements()['y'], [0, 1, 2, 3])
        self.assertEqual(movement.get_allMovements()['rx'], [0, 180])
        self.assertEqual(movement.get_allMovements()['rz'], [0, 60, 120, 180, 240, 300])
        self.assertEqual(set(movement.get_allMovements()['x']), set([0, 1, 2, 3, 4, 5]))

    def test_violet(self):
        movement = Movements(name="Violet")
        self.assertEqual(movement.generateLinearMovements(6), [0, 1, 2, 3, 4, 5])
        self.assertEqual(movement.generateLinearMovements(6, 3), [3, 4, 5, 0, 1, 2])
        self.assertEqual(movement.get_allMovements()['rx'], [0])
        self.assertEqual(movement.get_allMovements()['rz'], [0, 60, 120, 180, 240, 300])

    def test_rot(self):
        movement = Movements(name="Rot")
        self.assertEqual(movement.generateLinearMovements(6), [0, 1, 2, 3, 4, 5])
        self.assertEqual(movement.generateLinearMovements(6, 3), [3, 4, 5, 0, 1, 2])
        self.assertEqual(movement.get_allMovements()['rx'], [0, 180])
        self.assertEqual(movement.get_allMovements()['rz'], [0, 60, 120, 180, 240, 300])

    def test_count(self):
        movement = Movements()
        theNextMove = movement.nextMove()
        self.assertEqual(theNextMove['x'], 0)
        self.assertEqual(theNextMove['y'], 0)
        self.assertEqual(theNextMove['rx'], 0)
        self.assertEqual(theNextMove['rz'], 0)
        for ix in range(5):
            theNextMove = movement.nextMove()
        self.assertEqual(theNextMove['x'], 5)
        self.assertEqual(theNextMove['y'], 0)
        self.assertEqual(theNextMove['rx'], 0)
        self.assertEqual(theNextMove['rz'], 0)
        theNextMove = movement.nextMove()
        self.assertEqual(theNextMove['x'], 0)
        self.assertEqual(theNextMove['y'], 1)
        self.assertEqual(theNextMove['rx'], 0)
        self.assertEqual(theNextMove['rz'], 0)
        for iy in range(4*6-6-1):
            theNextMove = movement.nextMove()
        self.assertEqual(theNextMove['x'], 5)
        self.assertEqual(theNextMove['y'], 3)
        self.assertEqual(theNextMove['rx'], 0)
        self.assertEqual(theNextMove['rz'], 0)
        theNextMove = movement.nextMove()
        self.assertEqual(theNextMove['x'], 0)
        self.assertEqual(theNextMove['y'], 0)
        self.assertEqual(theNextMove['rx'], 180)
        self.assertEqual(theNextMove['rz'], 0)
        for iy in range(4*6*2 - 4*6 - 1):
            theNextMove = movement.nextMove()
        self.assertEqual(theNextMove['x'], 5)
        self.assertEqual(theNextMove['y'], 3)
        self.assertEqual(theNextMove['rx'], 180)
        self.assertEqual(theNextMove['rz'], 0)
        theNextMove = movement.nextMove()
        self.assertEqual(theNextMove['x'], 0)
        self.assertEqual(theNextMove['y'], 0)
        self.assertEqual(theNextMove['rx'], 0)
        self.assertEqual(theNextMove['rz'], 60)
        for iy in range(4*6*2*6 - 4*6*2 - 1):
            theNextMove = movement.nextMove()
        self.assertEqual(theNextMove['x'], 5)
        self.assertEqual(theNextMove['y'], 3)
        self.assertEqual(theNextMove['rx'], 180)
        self.assertEqual(theNextMove['rz'], 300)
        theNextMove = movement.nextMove()
        self.assertEqual(theNextMove['status'], 'finished')
        self.assertEqual(theNextMove.get('status'), 'finished')

        movement.resetIndexes()
        theNextMove = movement.nextMove()
        self.assertEqual(theNextMove['x'], 0)
        self.assertEqual(theNextMove['y'], 0)
        self.assertEqual(theNextMove['rx'], 0)
        self.assertEqual(theNextMove['rz'], 0)
        for ix in range(5):
            theNextMove = movement.nextMove()
        self.assertEqual(theNextMove['x'], 5)
        self.assertEqual(theNextMove['y'], 0)
        self.assertEqual(theNextMove['rx'], 0)
        self.assertEqual(theNextMove['rz'], 0)
        self.assertEqual(theNextMove.get('status', ''), '')


