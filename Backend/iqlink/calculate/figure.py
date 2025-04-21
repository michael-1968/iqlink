from .movements import Movements
from .helpers import normalizeAngle, angleTransformFrontendBackend, checkTypeOccupation, shiftAngle

class Figure():
    def __init__(self, definition, x, y, rotX, rotZ, figures):
        self.definition = definition
        self.name = definition.Name
        self.x = x
        self.y = y
        self.rotX = rotX
        self.rotZ = rotZ
        self.figures = figures
        self.message = ''
        self.movements = Movements(name=self.name)
           
    # checks all possible moves
    def scan(self):
        while True:
            nextMove = self.movements.nextMove()
            self.x = nextMove['x']
            self.y = nextMove['y']  
            self.rotX = nextMove['rx']  
            self.rotZ = nextMove['rz']  
            if self.fits():
                return True
            if nextMove.get('status', '') == 'finished':
                break
        return False
    
    # flips 60deg with 300deg and 120deg with 240deg to rotate the 
    # figure-object along its x-axis. Uses self.rotZ. 
    def angleModifyForFlip(self, angle):
        if self.rotX == 180:
            if angle == 60:
                return 300
            if angle == 300:
                return 60
            if angle == 120:
                return 240
            if angle == 240:
                return 120
        return angle
    
    # modifies the angle of the figure-object accordingly with
    # (1) the rotation around the z-axis, using self.rotZ
    # then (2) the rotation around the x-axis, using self.rotX
    def modifyAngle(self, angle, offset=0):
        return normalizeAngle(self.angleModifyForFlip(normalizeAngle(angle)) + self.rotZ + offset)

    
    # returns coordinates of angled elements 1 and 3  
    # does not modify the coordinates of the figure-object
    def probe(self, angle):
        return shiftAngle(self.x, self.y, angle)
    
    def reverseAngleList(self, angles):
        returnarray = [0, 60, 120, 180, 240, 300]
        for ix in angles:
            returnarray.remove(ix)
        return returnarray
    
    # Delivers the free angles of the elements of the figure. 
    # The angles are offset with the rotation of the figure. 
    def openAngles(self, element):
        type = self.definition.get()[element].get('Type')
        if type == 'C' or type == 'Y':
            returnlist = self.definition.get()[element].get('Open', '')
            returnlist = [self.modifyAngle(ax) for ax in returnlist]
            return returnlist # NormalizeAnglesList(returnlist)
        if type == 'O':
            return []
        if type == 'X':
            connectionangle = 0 if element == "Element1" else 180
            return self.reverseAngleList(
                [self.modifyAngle(self.definition.get()[element].get('Angle', connectionangle), offset=180)]
            )
        raise Exception(f'Figure.openAngles: Problem with definition - type:{type}')
    
    # delivers a list with elements of the form {'x': 2, 'y': 4, 'a': [120, 180], 't': 'C'}
    def listOfRequiredOpens(self):
        listToReturn = []
        angle = self.definition.get()['Element1'].get('Angle', 0)
        x1, y1 = self.probe(self.modifyAngle(angle))
        need = self.reverseAngleList(self.openAngles("Element1"))
        tp = self.definition.get()['Element1'].get('Type')
        listToReturn.append({'x': x1, 'y': y1, 'a': need, 't': tp})
        need = self.reverseAngleList(self.openAngles("Element2"))
        tp = self.definition.get()['Element2'].get('Type')
        listToReturn.append({'x': self.x, 'y': self.y, 'a': need, 't': tp})
        need = self.reverseAngleList(self.openAngles("Element3"))
        angle = self.definition.get()['Element3'].get('Angle', 180)
        x1, y1 = self.probe(self.modifyAngle(angle))
        tp = self.definition.get()['Element3'].get('Type')
        listToReturn.append({'x': x1, 'y': y1, 'a': need, 't': tp})
        return listToReturn
    
    def fits(self):
        list_requiredOpens = self.listOfRequiredOpens()
        for ix in range(3):
            neededOpens = list_requiredOpens[ix]['a']
            x = list_requiredOpens[ix]['x']
            y = list_requiredOpens[ix]['y']
            if (x > 5) or (x < 0) or (y > 3) or (y < 0):
                self.message = f'Figure.fits: out of board, x={x}, y={y}, n={self.name}'
                return False
            if not(set(neededOpens)).issubset(self.figures.board.Field()[x][y]['a']):
                self.message = f'Figure.fits: occupied, x={x}, y={y}, a={neededOpens}, n={self.name}'
                return False
            if not checkTypeOccupation(
                self.figures.board.Field()[x][y]['t'], 
                list_requiredOpens[ix]['t']
                ):
                self.message = f"Figure.fits: type occupied, x={x}, y={y}, board={self.figures.board.Field()[x][y]['t']}, figure={list_requiredOpens[ix]['t']}"
                return False
        return True

    # occupies the space on the boad
    # on unfit placement, the method runs into an exception raised by addTypeInfoToBoard and closeAnglesInBoard
    def place(self):
        list_requiredOpens = self.listOfRequiredOpens()
#        print("list_requiredOpens: ", list_requiredOpens)
        for ix in range(3):
            x = list_requiredOpens[ix]['x']
            y = list_requiredOpens[ix]['y']
            self.figures.board.addTypeInfoToBoard(x, y, list_requiredOpens[ix]['t'])    
            for jx in list_requiredOpens[ix]['a']:
                self.figures.board.closeAnglesInBoard(x, y, jx)
        self.figures.addFigure(self)

    # Un-occupies the space on the boad 
    def unPlace(self):
        list_requiredOpens = self.listOfRequiredOpens()
        for ix in range(3):
            x = list_requiredOpens[ix]['x']
            y = list_requiredOpens[ix]['y']
            self.figures.board.removeTypeInfoFromBoard(x, y, list_requiredOpens[ix]['t'])    
            for jx in list_requiredOpens[ix]['a']:
                self.figures.board.openAnglesInBoard(x, y, jx)
        self.figures.removeFigure(self)        

    # Returns the json-like setup string of the figure-object for the frontend
    # note the adaption to the angles due to different orientation of the x-axis in the frontend
    def get_setup(self):
        setupToBeShown = {}
        transfomedAngles = angleTransformFrontendBackend(self.rotX, self.rotZ)
        setupToBeShown = {
            'name': self.name, 'position': {'X': self.x, 'Y': self.y}, 'rotation': {'rotX': transfomedAngles['rotX'], 'rotY': 0, 'rotZ': transfomedAngles['rotZ']}
            }
        return setupToBeShown

    def __str__(self):
        returnstring = (
            f"{self.name} - x:{self.x}, y:{self.y}, rx:{self.rotX}, rz:{self.rotZ}, Fits: {self.fits()}"
        )
        return returnstring
