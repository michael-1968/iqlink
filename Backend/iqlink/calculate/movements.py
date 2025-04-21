import random


MAX_MOVEMENTS_X = 6
MAX_MOVEMENTS_Y = 4
MAX_ROTATIONS_X = 2
MAX_ROTATIONS_Z = 6
ROTATION_ANGLE_X = 180
ROTATION_ANGLE_Z = 60

class Movements():
    def __init__(self, startvalueX=0, startvalueY=0, name = ""):
        self.movementsX = self.generateLinearMovements(MAX_MOVEMENTS_X, startvalueX)
        self.movementsY = self.generateLinearMovements(MAX_MOVEMENTS_Y, startvalueY)
        if name == "Violet":
            self.rotationsX = [ix*ROTATION_ANGLE_X for ix in self.generateLinearMovements(1)]
        else:
            self.rotationsX = [ix*ROTATION_ANGLE_X for ix in self.generateLinearMovements(MAX_ROTATIONS_X)]
        self.rotationsZ = [ix*ROTATION_ANGLE_Z for ix in self.generateLinearMovements(MAX_ROTATIONS_Z)]

        self.indexMX = 0
        self.indexMY = 0
        self.indexRX = 0
        self.indexRZ = 0
        self.status = 'zeroed'

    def generateLinearMovements(self, number, startvalue=0):
        return list(range(startvalue, number)) + list(range(0, startvalue))
    
    def resetIndexes(self):
        self.indexMX = 0
        self.indexMY = 0
        self.indexRX = 0
        self.indexRZ = 0
        self.status = 'zeroed'
    
    def get_allMovements(self):
        return {
            'x': self.movementsX, 
            'y': self.movementsY, 
            'rx': self.rotationsX, 
            'rz': self.rotationsZ, 
        }

    def shuffle(self, object):
        random.shuffle(object)
    
    def nextMove(self):
        if self.status == 'finished':
            return {'status': 'finished'}
        recent = {
            'x': self.movementsX[self.indexMX], 
            'y': self.movementsY[self.indexMY], 
            'rx': self.rotationsX[self.indexRX], 
            'rz': self.rotationsZ[self.indexRZ], 
        }        
        if (self.indexMX >= MAX_MOVEMENTS_X - 1):
            self.indexMX = 0
            if (self.indexMY >= MAX_MOVEMENTS_Y - 1):
                self.indexMY = 0
                if (self.indexRX >= len(self.rotationsX) - 1):
                    self.indexRX = 0
                    if (self.indexRZ >= MAX_ROTATIONS_Z - 1):
                        self.indexRZ = 0
                        self.status = 'finished'
                    else:
                        self.indexRZ += 1
                else:
                    self.indexRX += 1
            else:
                self.indexMY += 1
        else:
            self.indexMX += 1
        return recent
