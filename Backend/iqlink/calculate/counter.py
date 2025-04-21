# myapp/counter.py

import threading
import time

counter = 0
started = 0

def increment_counter():
    global counter
    global started
    started += 10
    while True:
        counter += 1
        time.sleep(0.01)  # Sleep for 10 milliseconds

def get_counter():
    global counter
    return counter

def set_counter(new_value):
    global counter
    counter = new_value

counter_thread = threading.Thread(target=increment_counter)
counter_thread.daemon = True
counter_thread.start()
started += 1

