from django.db import models
from django.utils import timezone
# from studentapp.models import *

class Hosteltbl(models.Model):
    hname=models.CharField(max_length=255)
    hphone=models.IntegerField()
    hemail=models.EmailField()

    def __str__(self):
        return self.hname
    
    
class Wardentbl(models.Model):
    wname=models.CharField(max_length=255)
    wplace=models.CharField(max_length=255)
    wage=models.IntegerField()
    wphone=models.IntegerField()
    wemail=models.EmailField()
    wpassword=models.CharField(max_length=255)
    wapproval=models.BooleanField(default=False)
    approval_request_count=models.IntegerField(default=1)

    def __str__(self):
        return self.wname
        # return self.wname + " " + self.wplace
    
class Roomtbl(models.Model):
    students_count_choice=((1,'1 Student'),(2,'2 Students'),(3,'3 Students'))
    bed_count_choice=((1,'1 Bed'),(2,'2 Beds'),(3,'3 Beds'))
    ROOM_STATUS_CHOICE=(('Fully Occupied','Fully Occupied'),('Partially Occupied','Partially Occupied'),('Vacant','Vacant'))

    roomid=models.IntegerField()
    students_count=models.IntegerField(choices=students_count_choice,default=1)
    beds_count=models.IntegerField(choices=bed_count_choice,default=1)
    room_photo=models.FileField(upload_to='roomphotos',null=True)
    students_current_count=models.IntegerField(default=0,null=True)
    room_status=models.CharField(max_length=100,choices=ROOM_STATUS_CHOICE,default='Vacant')
    created_at=models.DateTimeField(default=timezone.now)
    updated_at=models.DateField(auto_now=True)

    hostelOBJ=models.ForeignKey(Hosteltbl,on_delete=models.DO_NOTHING,null=True)
    wardenOBJ=models.ManyToManyField(Wardentbl)

    def __str__(self):
        return str(self.roomid)
    


# MESS MANAGEMENT  -  Unique for all hostels

# class Dishtbl(models.Model):
#     DISH_SECTION=(('breakfast','breakfast'),('lunch','lunch'),('dinner','dinner'))

#     dish_section=models.CharField(max_length=250,choices=DISH_SECTION)
#     dishname=models.CharField(max_length=255)
#     dishprice=models.IntegerField()

#     def __str__(self):
#         return self.dishname
 
class Breakfasttbl(models.Model):
    dishname=models.CharField(max_length=255)
    dishprice=models.IntegerField()
    def __str__(self):
        return self.dishname

class Lunchtbl(models.Model):
    dishname=models.CharField(max_length=255)
    dishprice=models.IntegerField()
    def __str__(self):
        return self.dishname

class Dinnertbl(models.Model):
    dishname=models.CharField(max_length=255)
    dishprice=models.IntegerField()
    def __str__(self):
        return self.dishname


class ScheduledMealdtbl(models.Model):
    date=models.DateField(unique=True,null=True)
    mealapprovel=models.BooleanField(default=False)
    breakfastOBJS=models.ManyToManyField(Breakfasttbl,related_name='breakfastobjs')
    lunchOBJS=models.ManyToManyField(Lunchtbl,related_name='lunchobjs')
    dinnerOBJS=models.ManyToManyField(Dinnertbl,related_name='dinnerobjs')
    def __str__(self):
        return str(self.date)
    
class Selectedmealtbl(models.Model):
    plannedmealOBJ=models.ForeignKey(ScheduledMealdtbl,null=True,on_delete=models.CASCADE,related_name='plannedmealobj')
    breakfastOBJ=models.ManyToManyField(Breakfasttbl,related_name='breakfastobj')
    lunchOBJ=models.ManyToManyField(Lunchtbl,related_name='lunchobj')
    dinnerOBJ=models.ManyToManyField(Dinnertbl,related_name='dinnerobj')
    price=models.IntegerField(default=0)
    status=models.BooleanField(default=False)
    bill_generated_status=models.BooleanField(default=False)
    
    studentOBJ=models.ForeignKey('studentapp.Studentstbl',null=True,on_delete=models.DO_NOTHING,related_name='selectedstudent')
    def __str__(self):
        return str(self.studentOBJ.name + " - " + str(self.plannedmealOBJ.date))

class Billtbl(models.Model):
    studentOBJ=models.ForeignKey('studentapp.Studentstbl', on_delete=models.CASCADE, related_name='bills')
    start_date=models.DateField()
    end_date=models.DateField()
    total_amount=models.DecimalField(max_digits=10, decimal_places=2)
    bill_number=models.CharField(max_length=20, unique=True, blank=True)  # Unique bill number
    generated_on=models.DateTimeField(auto_now_add=True)
    generated_by=models.ForeignKey(Wardentbl,on_delete=models.DO_NOTHING,related_name='generated_bill_generated')

    def save(self, *args, **kwargs):
        # Generate a unique bill number
        if not self.bill_number:
            self.bill_number = f"BILL-{self.student.name}-{self.start_date.strftime('%Y%m%d')}-{self.end_date.strftime('%Y%m%d')}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"BILL-{self.student.name}-{self.start_date.strftime('%Y%m%d')}-{self.end_date.strftime('%Y%m%d')}"