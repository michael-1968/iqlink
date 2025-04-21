
from ..figure import Figure
from ..figuredefinition import nameToGeometry
from .strategy import Strategy
from ..helpers import angleTransformFrontendBackend
import time
from django.http import JsonResponse
from ..movements import Movements

class Catwalk(Strategy):
    def __init__(self, color):
        super().__init__()
        self.color = color

    def solutionfinder(self):
        maxIndex = len(self.allPossibleMoves) - 1
        # if self.indexOfNextMove > (maxIndex):
        #         self.indexOfNextMove = 0
        if maxIndex > 0:
            nextMove = self.nextMove()
            transformedAngles = angleTransformFrontendBackend(nextMove['rx'], nextMove['rz'])

            setupToBeShown = {
                'name': self.color, 'position': {'X': nextMove['x'], 'Y': nextMove['y']}, 'rotation': {'rotX': transformedAngles['rotX'], 'rotY': 0, 'rotZ': transformedAngles['rotZ']}
            }
            print(f'solutionfinder: {setupToBeShown}')
            self.message = str({'position': {'X': nextMove['x'], 'Y': nextMove['y']}, 'rotation': {'rotX': nextMove['rx'], 'rotZ': nextMove['rz']}})
            self.FoM = f"FoM: {nextMove['fom']} Index: {self.indexOfNextMove-1}, self.maxIndex: {maxIndex}"
#            self.indexOfNextMove += 1
            return setupToBeShown
        else:
            return {}
        
    def nextMove(self):
        maxIndex = len(self.allPossibleMoves) - 1
        if self.indexOfNextMove > (maxIndex):
                self.indexOfNextMove = 0
        returnIndex = self.allPossibleMoves[self.indexOfNextMove]
        self.indexOfNextMove += 1
        return returnIndex
    
    def retreiveAllMoves(self):
        return self.retreiveAllMovesWithGivenColor(self.color)

    def retreiveAllMovesWithGivenColor(self, color):
        self.movements = Movements(name=color)
        self.movements.resetIndexes()
        self.allPossibleMoves = []
        while True:
            mx = self.movements.nextMove()
            if mx.get('status', '') == 'finished':
                break
            x = mx['x']
            y = mx['y']
            rx = mx['rx']
            rz = mx['rz']
            figure = Figure(nameToGeometry(color), x, y, rx, rz, self.figures)
            if figure.fits():

                # Test, ob die Figur keine andere berührt:
                Ao, Ax, Ac = self.figures.board.numberOfNeededPlaces()
                figure.place()
                Bo, Bx, Bc = self.figures.board.numberOfNeededPlaces()
                FoM = self.figures.board.figureOfMerit()
                figure.unPlace()
                if (FoM == 0) or (Ao - Bo == 3):
                    pass
#                    print(f'retreiveAllPossibleMoves - futile one: {color} {x}, {y}, {rx}, {rz}  - {self.allPossibleMoves}') 
                else:
                    ix = 12 - len(self.figures.figuresToBePlaced())
                    self.fomProgress.push(ix, FoM)
#                    print(f'retreiveAllPossibleMoves - fomProgress.fomPerIteration: {12 - len(self.figures.figuresToBePlaced())}, {FoM} - {self.fomProgress.fomPerIteration}')
                    save = self.fomProgress.fomPerIteration
                    if not self.fomProgress.compare(ix, FoM):
#                        print(f'retreiveAllPossibleMoves - futile one - 2: {color} {x}, {y}, {rx}, {rz}  - {self.allPossibleMoves}') 
                        print(f'retreiveAllPossibleMoves: FoM: {FoM} - Index {ix} - Diff: {save[ix] - FoM}') 
                    else:
                        self.allPossibleMoves.append({'x': x, 'y': y, 'rx': rx, 'rz': rz, 'fom': FoM})
        return self.allPossibleMoves


