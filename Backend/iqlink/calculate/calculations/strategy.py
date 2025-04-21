from ..movements import Movements
from ..figures import Figures
from ..fomProgress import FomProgress
from ..parameter import Deltas

class Strategy:
    def __init__(self):
        self.movements = Movements()
        self.setupToBeShown = {}
        self.message = ''
        self.figures = Figures()
        self.FoM = 0
        self.allPossibleMoves = [] 
        self.indexOfNextMove = 0
#        self.fomProgress = FomProgress([2.5 for ix in range(12)])
        self.fomProgress = FomProgress(Deltas)

    def __str__(self):
        return "A Strategy-Object"

