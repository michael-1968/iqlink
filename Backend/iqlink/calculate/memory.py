
from .models import KeySet
from django.db import transaction, OperationalError
import time

class Memory():
    def __init__(self):
        self.dataStore = {}

    def retry_on_lock(func):
        def wrapper(*args, **kwargs):
            retries = 5
            while retries > 0:
                try:
                    return func(*args, **kwargs)
                except OperationalError as e:
                    if 'database is locked' in str(e):
                        retries -= 1
                        time.sleep(0.1)  # Wait for 100ms before retrying
                    else:
                        raise
            raise OperationalError("Max retries reached: database is locked")
        return wrapper
    

    @retry_on_lock
    def push(self, key, data_set):
#        print("Memory.push: ", key, data_set)
        with transaction.atomic():
            KeySet.objects.update_or_create(
                key=key,
                defaults={'data': data_set}
            )
        return 
    
    def pop(self, key):
        try:
            with transaction.atomic():
                entry = KeySet.objects.select_for_update().get(key=key)
                print("Memory.pop: ", key, entry.data)
                return entry.data
        except KeySet.DoesNotExist:
            print("Memory.pop: DoesNotExist", key)
            return None
        
    
    def numberOfEntries(self):
        with transaction.atomic():
            return KeySet.objects.count()


