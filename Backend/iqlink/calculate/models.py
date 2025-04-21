from django.db import models


class KeySet(models.Model):
    key = models.CharField(max_length=255, unique=True)
    data = models.JSONField()

    def __str__(self):
        return self.key
    
