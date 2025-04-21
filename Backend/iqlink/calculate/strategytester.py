from .calculations.best3FoM import Best3FoM
from .calculations.catwalk import Catwalk

cw = Catwalk('Dunkelviolet')
setup = {}

def get_Setup():
    global setup
    return setup

def set_Setup(new_value):
    global setup
    global cw
    setup = new_value
    cw.figures.deleteFiguresAndBoard()
    cw.figures.loadSetup(setup)
    cw.retreiveAllMoves()

def set_Parameter(new_value):
    global parameter
    parameter = new_value

def get_Parameter():
    global parameter
    return parameter

def get_Calculationtext():
    return {'text': cw.message, "fom": cw.FoM}

def get_Progress():
    finalSetup = setup.copy()
    finalSetup[len(finalSetup)+1] = cw.solutionfinder()
    return finalSetup

