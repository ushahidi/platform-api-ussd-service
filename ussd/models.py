from django.db import models
from django.utils.dateformat import format

class Log(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=20)
    text = models.TextField()

    def __str__(self):

        return str(format(self.timestamp, 'd/m/Y H:i'))