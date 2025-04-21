
import random
from .parameter import InitialListOfFigures
                      # ['Rot', 'Gelb', 'Violet', 'Magenta', 'Hellblau', 'Gruen', 'Dunkelgruen', 'Orange', 'Bordeaux', 'Dunkelviolet', 'Blau', 'Hellgruen']
OriginalListOfFigures = ["Rot", "Blau", "Bordeaux", "Orange", "Dunkelviolet", "Dunkelgruen", "Gruen", "Hellgruen", "Violet", "Gelb", "Hellblau", "Magenta"]
OptimizedListOfFigures = InitialListOfFigures
#["Rot", "Hellblau", "Bordeaux", "Magenta", "Violet", "Blau", "Dunkelgruen", "Orange", "Dunkelviolet", "Gruen", "Hellgruen", "Gelb"]
ListOfFigures = OptimizedListOfFigures
#print ("ListOfFigures-Init: ", NewListOfFigures)

def shuffleListOfFigures():
#    print ("shuffleListOfFigures: ", NewListOfFigures)
    last_8_elements = NewListOfFigures[4:]
    random.shuffle(last_8_elements)
#    print ("shuffleListOfFigures: ", NewListOfFigures)
    NewListOfFigures[4:] = last_8_elements
#    print ("shuffleListOfFigures: ", NewListOfFigures)


def listOfFigures():
    returnlist = ListOfFigures.copy()
#    print("ListOfFigures: ", returnlist)
    return returnlist

def normalizeAngle(angle):
    if angle in [0, 60, 120, 180, 240, 300]:
        return angle
    if angle < 0:
        angle = angle + 360 + (-angle // 360)*360
    if angle >= 360:
        angle = angle - (angle // 360)*360
    if not(angle in [0, 60, 120, 180, 240, 300]):
        raise Exception(f"NormalizeAngles: The angle is of incorrect value: {angle}")
    return angle

def angleTransformFrontendBackend(rotx, rotz):
    rx = rotx
    if (normalizeAngle(rotx)) == 0:
        rz = -rotz
    elif (normalizeAngle(rotx)) == 180:          
        rz = rotz
    else:
        raise Exception(f"AngleTransformFrontendBackend: angle is neither 0 nor 180 - angle:{rotx}")
    return {'rotX': rx, 'rotZ': rz}

def checkTypeOccupation(type1, type2):
    if (type1 == '') or (type2 == ''):
        return True
    if type1 == 'X' and type2 == 'C':
        return True
    if type1 == 'C' and type2 == 'X':
        return True
    if type1 == 'Y' and type2 == 'C':
        return True
    if type1 == 'C' and type2 == 'Y':
        return True
    return False
    
def shiftAngle(x, y, angle):
    x1 = x
    y1 = y
    offset = 0
    if y % 2 == 1:
        offset = 1
    if angle == 0: 
        x1 = x + 1 
        y1 = y + 0
    elif angle == 60: 
        x1 = x + 0 + offset
        y1 = y - 1
    elif angle == 120: 
        x1 = x - 1 + offset
        y1 = y - 1
    elif angle == 180: 
        x1 = x - 1 
        y1 = y + 0
    elif angle == 240: 
        x1 = x - 1 + offset
        y1 = y + 1
    elif angle == 300: 
        x1 = x + 0 + offset
        y1 = y + 1
    else:
        raise Exception(f'Figure.probe: Problem with angle - angle:{angle}')
    return x1, y1
