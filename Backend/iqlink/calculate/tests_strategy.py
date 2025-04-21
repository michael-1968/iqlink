from django.test import TestCase


from .calculations.catwalk import Catwalk
from .figures import testdata_ohneGruen

class TestsCatwalk(TestCase):

    def setUp(self):
        self.catwalk = Catwalk('Gruen')
        self.setup = testdata_ohneGruen
        self.catwalk.figures.deleteFiguresAndBoard()
        self.catwalk.figures.loadSetup(self.setup)
        # for fx in self.catwalk.figures.get_figures():
        #     fx.place()

    def test_basic(self):
        self.assertEqual(str(self.catwalk), "A Strategy-Object")

    def test_solutionfinder(self):
        self.catwalk.retreiveAllMoves()
        self.assertEqual(len(self.catwalk.figures.get_figures()), 6)
        response = self.catwalk.solutionfinder()
        self.assertEqual(response['name'], 'Gruen')
        self.assertEqual(response['position']['X'], 1)
        self.assertEqual(response['rotation']['rotZ'], 0)
        self.assertEqual(str(response), "{'name': 'Gruen', 'position': {'X': 1, 'Y': 3}, 'rotation': {'rotX': 180, 'rotY': 0, 'rotZ': 0}}")

