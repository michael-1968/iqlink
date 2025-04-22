from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
import math

from django.http import JsonResponse
from .counter import get_counter, set_counter
from .counter import started, counter 
from .communication import get_Setup, set_Setup, get_Progress, set_Parameter, get_Parameter, get_Calculationtext
from .communication import startCalculation, breakCalculation, save_Setup, load_Setup, load_ButtonNames, save_ButtonNames
from .helpers import get_git_version

def show_counter(request):
    return JsonResponse({"counter": get_counter(), "started": started})

def index(request):
    return render(request, 'calculate/index.html')

@csrf_exempt
def update_counter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        new_value = data.get('new_value', None)
        if new_value is not None and not (math.isnan(new_value)):
            # Update the counter or perform any other logic
            set_counter(new_value)
            return JsonResponse({"status": "success", "new_counter": get_counter()})
        else:
            return JsonResponse({"status": "error", "message": "Invalid data"})
    return JsonResponse({"status": "error", "message": "Invalid request method"})

def sendInfo(request):
    return JsonResponse({"Setup": get_Setup(), "Parameter": get_Parameter(), "Counter": get_counter()})

def sendCalculationProgress(request):
    return JsonResponse(get_Progress())

def sendCalcluationText(request):
    return JsonResponse({"calculationtext": get_Calculationtext()['text'], "status": get_Calculationtext()['fom']})

def setupLoadButtonnames(request):
#    print("setupLoadButtonnames")
    return JsonResponse(load_ButtonNames())

@csrf_exempt
def setupSaveButtonnames(request):
#    print("setupSaveButtonnames")
    if request.method == 'POST':
        data = json.loads(request.body)
#        print("setupSaveButtonnames: ", data)
        save_ButtonNames(data)    
    return JsonResponse({"status": "saved", "message": "none"}) 

def setupLoad(request):
    filename = request.GET.get('filename', None)
    x = load_Setup(filename)
    print("setupLoad 1: ", filename)
    print("setupLoad 2: ", x)
    return JsonResponse(load_Setup(filename))

def version(request):
    return JsonResponse({"version": get_git_version()})

@csrf_exempt
def startOrPauseCalculation(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print("startOrPauseCalculation:", data)
        cmd = data.get('cmd', None)
        if cmd == "run":
            startCalculation()
        elif cmd == "pause":
            breakCalculation()
            return JsonResponse({"status": "error", "message": "Invalid data"})
    return JsonResponse(data)

# Backend to receive the setup data
@csrf_exempt
def setupReceive(request):
    if request.method == 'POST':
        data = json.loads(request.body)
    resultOfCheck = set_Setup(data)
#    print("setupReceive: ", resultOfCheck)
    return JsonResponse(resultOfCheck)

@csrf_exempt
def setupSave(request):
    if request.method == 'POST':
        data = json.loads(request.body)
    save_Setup(data)    
    return JsonResponse({"status": "saved", "message": "none"}) 

@csrf_exempt
def receiveCalculationParameter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
    set_Parameter(data)    
    return JsonResponse(data)

