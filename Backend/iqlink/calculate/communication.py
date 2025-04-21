
import threading
from .calculations.best3FoM import Best3FoM
from .calculations.catwalk import Catwalk
from .calculations.calculation import Calculation
from .memory import Memory

cw = Best3FoM('keineFarbe')
finalresult = {'setup': {}, 'text': 'not running', 'fom': 0}
solver = None
t = None
datasaver = None
memory = Memory()

def save_Setup(data):
    global setup
    memory.push(data["name"], data["setup"])
    return

def load_Setup(filename):
    x = memory.pop(filename)
    return x

def load_ButtonNames():
    x = memory.pop('buttonnames')
#    print("load_ButtonNames: ", x)
    return x

def save_ButtonNames(names):
#    print("save_ButtonNames: ", names)
    memory.push('buttonnames', names)
    return

def get_Setup():
    global setup
    return setup

def set_Setup(new_value):
    global setup
    global cw
    global solver
    setup = new_value
    cw.figures.deleteFiguresAndBoard()
    try:
        cw.figures.loadSetup(setup)
    except Exception as e:
        print("Error in setup: ", e)
        result = {'status': 'error', 'message': 'Figur ' + cw.figures.nameOfFigureToBePlaced + ' passt nicht'}
        return result
    # show setup back to Frontend
    finalresult['setup'] = new_value
    solver = None
#    result = cw.figures.checkSetup()
    result = {"status": "OK", "message": ""}
    return result

def solve():
    global solver
    res = solver.solve()
    print ("Communication-solve: ", res)
    return solver.solve()

def set_Parameter(new_value):
    global parameter
    parameter = new_value

def get_Parameter():
    global parameter
    return parameter

def startCalculation():
    print("startCalculation")
    global cw
    global solver
    global finalresult
    global t
    solver = None
    t = None

    solver = Calculation(cw)
    solver.resetObjectValues()
    if t is not None and t.is_alive():
        print("Calculation is already running")
        return
    t = threading.Thread(target=solve)
    t.start()
    print("Thread started")
    waitToFinishCalculation()
    return

def breakCalculation():
    print("breakCalculation")
    global solver
    if solver is not None:
        solver.stop()
    return 

def waitToFinishCalculation():
    global t
    global solver
    t.join()
    print("Thread joined")
    finalresult = solver.sharedResult
    finalresult['text'] = f"finished, {solver.message}" 
    print("Thread done, fomProgress: ", cw.fomProgress.fomPerIteration)
#    print("Thread done, result: ", finalresult)

def get_Calculationtext(): 
    if solver is None:
        return {'text': finalresult['text'], 'fom': finalresult['fom']}    
    else:
        return {'text': solver.sharedResult['text'], 'fom': solver.sharedResult['fom']}

def get_Progress():
    global solver
    global finalresult
    if solver is None:
        return finalresult['setup']
    else:
        result = solver.sharedResult['setup']
        return result
