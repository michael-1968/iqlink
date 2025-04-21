# myapp/urls.py

from django.urls import path
from .views import show_counter, index, update_counter, receiveCalculationParameter
from .views import sendInfo, sendCalculationProgress, sendCalcluationText, setupReceive
from .views import startOrPauseCalculation, setupSave, setupLoad, setupLoadButtonnames, setupSaveButtonnames

urlpatterns = [

    path('counter/', index, name='index'),
    path('counter/get/', show_counter, name='show_counter'),
    path('counter/update/', update_counter, name='update_counter'),  
    path('calculation/info/', sendInfo, name='sendInfo'),  
    path('calculation/progress/', sendCalculationProgress, name='sendCalculationProgress'),  
    path('calculation/text/', sendCalcluationText, name='sendCalcluationText'),  
    path('calculation/', startOrPauseCalculation, name='startOrPauseCalculation'),  
    path('calculation/parameter/', receiveCalculationParameter, name='receiveCalculationParameter'),  
    path('setup/receive/', setupReceive, name='setupReceive'),  
    path('setup/save/', setupSave, name='setupSave'),  
    path('setup/load/', setupLoad, name='setupLoad'),  
    path('setup/load/buttonnames/', setupLoadButtonnames, name='setupLoadButtonnames'),  
    path('setup/save/buttonnames/', setupSaveButtonnames, name='setupSaveButtonnames'),  

]
