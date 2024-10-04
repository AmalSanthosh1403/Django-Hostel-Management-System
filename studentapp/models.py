from django.db import models
from wardenapp.models import Roomtbl

class Studentstbl(models.Model):
    name=models.CharField(max_length=255)
    place=models.CharField(max_length=255)
    age=models.IntegerField()
    phone=models.IntegerField()
    email=models.EmailField()
    password=models.CharField(max_length=255)
    sapproval=models.BooleanField(default=False)
    approval_request_count=models.IntegerField(default=1)
    allocation_status=models.BooleanField(default=False)
    roomOBJ=models.ForeignKey(Roomtbl,on_delete=models.DO_NOTHING,related_name='students',null=True)
    def __str__(self):
        return self.name

    