
from .parameter import InitialFomProgress

class FomProgress():
    def __init__(self, deltas):
#        self.fomPerIteration = [0.0 for ix in range(12)] 
        self.load()
        self.deltas = deltas
        
    def push(self, iteration, fom):
        if iteration < 0 or iteration > 11:
            raise Exception(f"FomProgress.push: Range Error iteration={iteration}")
        if fom < self.fomPerIteration[iteration]:
            self.fomPerIteration[iteration] = fom
        return
    
    def compare(self, iteration, fom):
        return fom <= self.fomPerIteration[iteration] + self.deltas[iteration]
    
    def load(self):
        self.fomPerIteration = InitialFomProgress

#        [0.0, 0.0, 0.0, 0.0, -13.3,  -15.45, -17.6, -20.6,  -22.75, -24.05, -25.35, -25.8]



