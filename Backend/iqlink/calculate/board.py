from .helpers import checkTypeOccupation, shiftAngle, normalizeAngle
from .figuredefinition import nameToGeometry
from .parameter import FoMShare

class Board():
    def __init__(self, figures):
        self.field = [[{'a': [0, 60, 120, 180, 240, 300], 't': ''} for y in range(4)] for x in range(6)]
        # NOCH NICHT LÖSCHEN. Hier werden nur die Winkel freigegeben, die besetzt weden können. 
        # Code kann gegebenenfalls beim Untersuchen der Wirkung eines Teils verwendet werden.

        # self.field = [[{'a': [], 't': ''} for y in range(4)] for x in range(6)]
        # for iy in range(4):
        #     for ix in range(6):
        #         for ax in [0, 60, 120, 180, 240, 300]:
        #             probeX, probeY = shiftAngle(ix, iy, ax)
        #             if probeX in range(6) and probeY in range(4):
        #                 self.field[ix][iy]['a'].append(ax)
        self.figures = figures
        print("Board.__init__ aufgerufen. ")
        for ix in range(4):
            for iy in range(6):
                print(self.field[iy][ix])
            print()
    
    def Field(self):
        return self.field
    

    def numberOfOpens(self):
        zx = 0
        for ix in range(6):
            for iy in range(4):
                zx += len(self.field[ix][iy]['a'])
        return zx    
    
    def numberOfPotentialFreePlaces_3(self):
        zx = 0
        for iy in range(4):
            for ix in range(6):
                if len(self.field[ix][iy]['t']) == 0:
                    zx += 1
#                    print('numberOfPotentialFreePlaces_3 1: ', ix, iy)
                else:
                    for angle in self.field[ix][iy]['a']:
                        x, y = shiftAngle(ix, iy, angle)
                        if x in range(6) and y in range(4):
                            if "C" in (self.field[x][y]['t']) and len(self.field[x][y]['a']) == 2 and (
                                    normalizeAngle(self.field[x][y]['a'][0] + 180) in self.field[ix][iy]['a'] or  normalizeAngle(self.field[x][y]['a'][1] + 180) in self.field[ix][iy]['a']
                                ):
                                zx += 1
#                                print('numberOfPotentialFreePlaces_3 3: ', ix, iy)
                                break
                            if not "C" in (self.field[x][y]['t']): 
                                zx += 1
#                                print('numberOfPotentialFreePlaces_3 2: ', ix, iy)
                                break
        return zx
    
    def numberOfPotentialFreePlaces_2(self):
        zx = 0
        found = False
        for iy in range(4):
            for ix in range(6):
                if len(self.field[ix][iy]['t']) == 0:
                    zx += 1
#                    print('numberOfPotentialFreePlaces_2 1: ', ix, iy)
                else:
                    for angle in self.field[ix][iy]['a']:
                        x, y = shiftAngle(ix, iy, angle)
                        if x in range(6) and y in range(4):
                            for ax in self.field[x][y]['a']:
                                if normalizeAngle(ax + 180) == angle:
                                    found = True
                                    break
                        if found:
#                            print('numberOfPotentialFreePlaces_2 2: ', ix, iy)
                            zx += 1
                            found = False
                            break
        return zx

    def numberOfPotentialFreePlaces_2a(self):
        zx = 0
        found = False
        for iy in range(4):
            for ix in range(6):
                if len(self.field[ix][iy]['t']) == 0:
                    zx += 1
#                    print('numberOfPotentialFreePlaces_2 1: ', ix, iy)
                else:
                    for angle in self.field[ix][iy]['a']:
                        x, y = shiftAngle(ix, iy, angle)
                        if x in range(6) and y in range(4): 
                            for ax in self.field[x][y]['a']:
                                if (self.field[ix][iy]['t'] == 'C' and len(self.field[ix][iy]['a']) == 1 and self.field[x][y]['t'] == 'C') and len(self.field[x][y]['a']) == 1:
                                    break
                                if normalizeAngle(ax + 180) == angle:
                                    found = True 
                                    break
                        if found:
#                            print('numberOfPotentialFreePlaces_2 2: ', ix, iy)
                            zx += 1
                            found = False
                            break
        return zx

    def numberOfPotentialFreePlaces_4(self):
        Eo = 0
        Ex = 0
        Ec = 0
        for iy in range(4):
            for ix in range(6):
                if self.field[ix][iy]['t'] == '':
                    Eo += 1
                if self.field[ix][iy]['t'] == 'X':
                    Ec += 1
                if self.field[ix][iy]['t'] == 'Y':
                    Ec += 1
                if self.field[ix][iy]['t'] == 'C':
                    Ex += 1
        return Eo, Ex, Ec
    
    def numberOfNeededPlaces(self):
        Ax = 0
        Ao = 0
        Ac = 0
        for fx in self.figures.figuresToBePlaced():
            if nameToGeometry(fx).element1_type in ['X', 'Y']:
                Ax += 1
            if nameToGeometry(fx).element2_type in ['X', 'Y']:
                Ax += 1
            if nameToGeometry(fx).element3_type in ['X', 'Y']:
                Ax += 1
            if nameToGeometry(fx).element1_type in ['O']:
                Ao += 1
            if nameToGeometry(fx).element2_type in ['O']:
                Ao += 1
            if nameToGeometry(fx).element3_type in ['O']:
                Ao += 1
            if nameToGeometry(fx).element1_type in ['C']:
                Ac += 1
            if nameToGeometry(fx).element2_type in ['C']:
                Ac += 1
            if nameToGeometry(fx).element3_type in ['C']:
                Ac += 1
        return Ao, Ax, Ac


    def figureOfMerit(self):
        E = self.numberOfPotentialFreePlaces_2a()
        A = 12 - len(self.figures.figures)
        res = self.figureOfMerit_tester()
        Ao, Ax, Ac = self.numberOfNeededPlaces()
        Eo, Ex, Ec = self.numberOfPotentialFreePlaces_4()
#        print('figureOfMerit: ', res, A, E, 'A', Ao, Ax, Ac, 'E', Eo, Ex, Ec)
        R = Eo - Ao
        if E < 2*A + 2:
            return 0
        if R < 0:
            return 0
        if Ex + R - Ax < 0:
            return 0
        if Ec + R - Ac < 0:
            return 0
        return res
        return res if (Eo - Ao) + (Ex - Ax) + (Ec - Ac) >= 0 else 0
        return res if Ao <= Eo + 2 and Ax <= Ex + 2 and Ac <= Ec + 2 else 0

    def figureOfMerit_123(self):
        res = self.figureOfMerit_basic()
        E = self.numberOfPotentialFreePlaces_2a()
        A = 12 - len(self.figures.figures)
#        print('figureOfMerit: ', res, A, E)
        return res if E >= 2*A + 2 else 0
    
    # irgendein Teil: -1 Punkt.  
    def figureOfMerit_basic(self):
        zx = 0
        for ix in range(6):
            for iy in range(4):
                if len(self.field[ix][iy]['t']) > 0:
                    zx -= 1
        return zx    

    # XC, YC: 2 points, X, Y, C: 1 point 
    def figureOfMerit_tester(self):
        zx = 0
        for ix in range(6):
            for iy in range(4):
                if len(self.field[ix][iy]['t']) > 1:
                    zx -= FoMShare
                elif self.field[ix][iy]['t'] in ['X', 'Y', 'C', 'O']:
                    zx -= 1
        return zx    
        
    # XC, YC: 2 points, X, Y, C: 1 point 
    def figureOfMerit_doesnotwork(self):
        zx = 0
        for ix in range(6):
            for iy in range(4):
                if len(self.field[ix][iy]['t']) > 1:
                    zx += 2
                elif self.field[ix][iy]['t'] in ['X', 'Y', 'C']:
                    zx += 1
        return zx    

    def closeAnglesInBoard(self, x, y, angle):
        if not(x in range(6)):
            raise Exception(f"Board.Close: Range Error x={x}")
        if not(y in range(4)):
            raise Exception(f"Board.Close: Range Error y={y}")
        if not(angle in [0, 60, 120, 180, 240, 300]):
            raise Exception(f"Board.Close: The angle is of incorrect value: {angle}")
        if not(angle in self.field[x][y]['a']):
            raise Exception("Board.Close: The angle has already been removed")
        self.field[x][y]['a'].remove(angle)
        
    def openAnglesInBoard(self, x, y, angle):
        if not(x in range(6)):
            raise Exception(f"Board.Open: Range Error x={x}")
        if not(y in range(4)):
            raise Exception(f"Board.Open: Range Error y={y}")
        if not(angle in [0, 60, 120, 180, 240, 300]):
            raise Exception(f"Board.Open: The angle is of incorrect value: {angle}")
        if angle in self.field[x][y]['a']:
            raise Exception("Board.Open: The angle is already there")
        self.field[x][y]['a'].append(angle)
    
    def addTypeInfoToBoard(self, x, y, type):
        if len(self.field[x][y]['t']) >= 2:
            raise Exception(f"Board.addTypeInfoToBoard: Not more than two type attributes possible, type={type}")
        if checkTypeOccupation(self.field[x][y]['t'], type): 
            self.field[x][y]['t'] += type
        else:
            raise Exception(f"Board.addTypeInfoToBoard: The type attribute cannot be added, type={type}")

    def removeTypeInfoFromBoard(self, x, y, type):
        if not(type in self.field[x][y]['t']):
            raise Exception(f"Board.removeTypeInfoFromBoard: The type attribute to be removed is not there, type={type}")
        self.field[x][y]['t'] = self.field[x][y]['t'].replace(type, '')       

        

