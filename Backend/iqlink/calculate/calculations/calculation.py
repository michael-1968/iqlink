import time
import random
from ..figuredefinition import nameToGeometry
from ..figure import Figure

class Calculation:
    sharedResult = {'setup': {}, 'text': 'messagetext', 'fom': 43}
    message = ''
    numberOfObjects = 0
    numberOfOpenObjects = 0
    maxFoM = 0
    stopIt = False
    startTime = time.time()

    def __init__(self, strategy):
        self.strategy = strategy
        self.sumOfMoves = 0
        self.color = ''
        self.ID = random.randint(0, 1000)
        Calculation.numberOfObjects += 1
        Calculation.numberOfOpenObjects += 1

    def stop(self):
        Calculation.stopIt = True

    def resetObjectValues(self):
        Calculation.message = ''
        Calculation.numberOfObjects = 0
        Calculation.numberOfOpenObjects = 0
        Calculation.maxFoM = 0
        Calculation.startTime = time.time()
        Calculation.stopIt = False

    def saveCurrentResult(self, nextMove, number, time):
        if nextMove['fom'] > Calculation.maxFoM:
            Calculation.maxFoM = nextMove['fom']
        message = f"'Colors': {self.strategy.figures.get_NamesOfAllFigures()}"
        FoM = f"FoM: {nextMove['fom']:.1f}, Time: {round(time)}, Nr of Figures: {12-number}, Trials: {Calculation.numberOfObjects}, Objects: {Calculation.numberOfOpenObjects}"# Index: {self.indexOfNextMove-1}, self.maxIndex: {maxIndex}"
        Calculation.sharedResult = {'setup': self.strategy.figures.get_SetupOfAllFigures(), 'text': message, "fom": FoM}
        return

    def get_currentResult(self):
        return Calculation.sharedResult
    
    def calculateTheColorSequence(self, figuresequence):
        color_and_fom = []
        for cx in figuresequence:
            moves = self.strategy.retreiveAllMovesWithGivenColor(cx)
            fom = 0
            for mx in moves:
                fom += mx['fom']
            color_and_fom.append({'color': cx, 'fom': fom})
#        print("shuffleTheColorSequence: ", color_and_fom)
        sorted_colors = sorted(color_and_fom, key=lambda move: move['fom'], reverse=True)
        colors = [item['color'] for item in sorted_colors]
#        print("shuffleTheColorSequence: vorher  ", figuresequence)
#        print("shuffleTheColorSequence: nachher ", colors)
        return colors

    def solve(self):
        if self.strategy.figures.figuresToBePlaced() == []:
            print(f"return - ID {self.ID}, Color: {self.color}, solved")
            print("SOLVED")
            Calculation.numberOfOpenObjects -= 1
            Calculation.message = "solved"
            return "solved"
        
        if Calculation.stopIt:
            print(f"return - ID {self.ID}, Color: {self.color}, stopped")
            print("STOPPED")
            Calculation.message = "stopped"
            return "stopped"
        figuresToBePlaced = self.strategy.figures.figuresToBePlaced()
        figuresToBePlaced = self.calculateTheColorSequence(figuresToBePlaced)
        for colors in figuresToBePlaced:
            self.color = colors
#            print(f"Solve - #: {Calculation.numberOfOpenObjects}, setup: {self.strategy.figures.get_SetupOfAllFigures()}")
            moves = self.strategy.retreiveAllMovesWithGivenColor(self.color)
            for mx in moves:
                x = mx['x']
                y = mx['y']
                rx = mx['rx']
                rz = mx['rz']
                figure = Figure(nameToGeometry(self.color), x, y, rx, rz, self.strategy.figures)
                figure.place() 
                self.saveCurrentResult(mx, len(self.strategy.figures.figuresToBePlaced()), (time.time() - Calculation.startTime))

                innerCalculation = Calculation(self.strategy)
                res = innerCalculation.solve()
                if res == "stopped":
                    return "stopped"
                if res == "solved":
                    print(self.ID, "SOLVED")
                    return "solved"

                figure.unPlace() 
                
        Calculation.numberOfOpenObjects -= 1
        Calculation.message = "No Solution"
        return "No Solution"

    def __str__(self):
        return "The Calculation-Object"

