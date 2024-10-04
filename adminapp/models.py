from django.db import models
from wardenapp.models import *

class Admintbl(models.Model):
    adminname=models.CharField(max_length=255)
    adminemail=models.EmailField()
    adminpassword=models.CharField(max_length=255)

    def __str__(self):
        return self.adminname
    
