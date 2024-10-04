from django.shortcuts import render,redirect
from django.contrib import messages
from django.urls import reverse
from . models import *
from studentapp.models import *
from adminapp.views import already_exist

def wardenRegistration(request):
    if request.method=='POST':
        name1=request.POST.get('nm')
        place1=request.POST.get('pl')
        email1=request.POST.get('em')
        pass1=request.POST.get('psw')
        age1=request.POST.get('age')
        phone1=request.POST.get('ph')

        # already_exist=Studentstbl.objects.filter(email=email1)  another function named already_exist declred in adminapp
        if already_exist(email1):
            return render(request,'wardenregistrationpage.html',{'error_reg':'Email Already Exists'})
        else:
            obj=Wardentbl.objects.create(
                wname=name1,
                wplace=place1,
                wage=age1,
                wphone=phone1,
                wemail=email1,
                wpassword=pass1,
            )
            obj.save()

            if obj:
                return redirect('/login')
            else:
                return render(request,'wardenregistrationpage.html')

    return render (request,'wardenregistrationpage.html')

def homePage(request):
    return render(request,'homepagewarden.html')

def wardenProfile(request):
    obj=Wardentbl.objects.get(id=request.session['warden_id'])
    return render(request,'wardenprofile.html',{'obj':obj})

def wardenApprovalStatus(request):
    obj=Wardentbl.objects.get(id=request.session['warden_id'])
    return render(request,'wardenapproval.html',{'obj':obj})

def wardenReApproval(request):
    obj=Wardentbl.objects.get(id=request.session['warden_id'])
    obj.approval_request_count+=1
    obj.save()
    messages.success(request,'Approval Request sended successfully.')
    return redirect('/warden/approval')

def approveStudent(request):
    obj=Wardentbl.objects.get(id=request.session['warden_id'])
    studentobjs=Studentstbl.objects.filter(sapproval=False)
    return render(request,'approvalstuden_wardent.html',{'studentobjs':studentobjs,'obj':obj})

def processApproval(request):
    studentid=request.GET.get('sid')
    studentobj=Studentstbl.objects.get(id=studentid)
    studentobj.sapproval=True
    studentobj.save()
    return redirect('/warden/approvestudent')

def viewAllRooms(request,hid):
    wardenobj=Wardentbl.objects.get(id=request.session['warden_id'])
    hostelobj=Hosteltbl.objects.get(id=hid)
    try:

        warden_room=Roomtbl.objects.filter(wardenOBJ=wardenobj).first()
        roomobjs=Roomtbl.objects.filter(hostelOBJ=hostelobj)
        
        return render(request,'viewallrooms.html',{'roomobjs':roomobjs,'hostelobj':hostelobj})
    except:
        return render(request,'viewallrooms.html')
    

def wardenRooms(request):
    wardenobj=Wardentbl.objects.get(id=request.session['warden_id'])
    try:
        
        myroomobjs=Roomtbl.objects.filter(wardenOBJ=wardenobj)
        # myroomobjs=Roomtbl.objects.filter(hostelOBJ=warden_room.hostelOBJ,wardenOBJ=wardenobj)
        
        # return render(request,'wardenrooms.html',{'roomobjs':myroomobjs,'hostelobj':warden_room.hostelOBJ})
        return render(request,'wardenrooms.html',{'roomobjs':myroomobjs})
    except:
        return render(request,'wardenrooms.html')
    
def wardenroomDetails(request,rid):
    roomobj=Roomtbl.objects.get(id=rid)
    wardenobjs=Wardentbl.objects.all()
    studentobjs=Studentstbl.objects.filter(roomOBJ=roomobj)
    return render(request,'wardenroomdetails.html',{'roomobj':roomobj,'wardenobjs':wardenobjs,'studentobjs':studentobjs})

def addStudent(request,rid):
    roomobj=Roomtbl.objects.get(id=rid)
    if request.method=='POST':
        selected_students_id=request.POST.getlist('selected_students')
        for sid in selected_students_id:
            studentobj=Studentstbl.objects.get(id=sid)
            studentobj.roomOBJ=roomobj
            studentobj.allocation_status=True
            studentobj.save()
            roomobj.students_current_count+=1
        if roomobj.students_current_count==roomobj.students_count:
            roomobj.room_status='Fully Occupied'
        else:
            roomobj.room_status='Partial Occupied'
        roomobj.save()
        wardenroomDetails_url=reverse('wardenroomdetails',kwargs={'rid':rid})
        return redirect(wardenroomDetails_url)
    
    studentobjs=Studentstbl.objects.filter(allocation_status=False,sapproval=True)
    return render(request,'addstudent.html',{'studentobjs':studentobjs})

def removeStudent(request,rid,sid):
    studentobj=Studentstbl.objects.get(id=sid)
    roomobj=Roomtbl.objects.get(id=rid)
    studentobj.roomOBJ=None
    studentobj.allocation_status=False
    studentobj.save()

    roomobj.students_current_count-=1
    if roomobj.students_current_count==0:
        roomobj.room_status='Vacant'
    else:
        roomobj.room_status='Partial Occupied'
    roomobj.save()
    try :
        request.session['warden_id']
        wardenroomDetails_url=reverse('wardenroomdetails',kwargs={'rid':rid})
        return redirect(wardenroomDetails_url)
    except:
        request.session['admin_id']
        roomdetails_url=reverse('roomdetails',kwargs={'rid':rid})
        return redirect(roomdetails_url)
    
#Meals......
#  
def viewMealsPlan(request):
    availablemealobjs=ScheduledMealdtbl.objects.all()
    return render(request,'mealsplan.html',{'availablemealobjs':availablemealobjs})

def addNewMealsPlan(request):
    breakfastobjs=Breakfasttbl.objects.all()
    lunchobjs=Lunchtbl.objects.all()
    dinnerobjs=Dinnertbl.objects.all()

    if request.method=='POST':
        newdate=request.POST.get('newdate')
        selected_breakfast=request.POST.getlist('allbreakfast')
        selected_lunch=request.POST.getlist('alllunch')
        selected_dinner=request.POST.getlist('alldinner')
        # print(newdate)
        if ScheduledMealdtbl.objects.filter(date=newdate):
            messages.success(request, "Selected date already scheduled.")
            return redirect('/warden/mealsplan')
        breakfasts=Breakfasttbl.objects.filter(id__in=selected_breakfast)
        lunchs=Lunchtbl.objects.filter(id__in=selected_lunch)
        dinners=Dinnertbl.objects.filter(id__in=selected_dinner)

        newplan=ScheduledMealdtbl.objects.create(
            date=newdate,
        )
        newplan.save()
        newplan=ScheduledMealdtbl.objects.get(date=newdate)
        newplan.breakfastOBJS.set(breakfasts)
        newplan.lunchOBJS.set(lunchs)
        newplan.dinnerOBJS.set(dinners)
        newplan.save()
        messages.success(request, "New meals scheduled for "+str(newplan.date))
        return redirect('/warden/mealsplan')
    
    return render(request,'addnewmeal.html',{'breakfastobjs':breakfastobjs,'lunchobjs':lunchobjs,'dinnerobjs':dinnerobjs})

def deleteMealsPlan(request,mid):
    mealobj=ScheduledMealdtbl.objects.get(id=mid)
    mealobj.delete()
    return redirect('/warden/mealsplan')


def editMealsPlan(request,mid,funcall):
    mealobj=ScheduledMealdtbl.objects.get(id=mid)
    breakfastobjs=Breakfasttbl.objects.all()
    lunchobjs=Lunchtbl.objects.all()
    dinnerobjs=Dinnertbl.objects.all()
    selectedmealsobjs=Selectedmealtbl.objects.filter(plannedmealOBJ=mealobj)

    if request.method=="POST":
        selected_breakfast=request.POST.getlist('allbreakfast')
        selected_lunch=request.POST.getlist('alllunch')
        selected_dinner=request.POST.getlist('alldinner')

        breakfasts=Breakfasttbl.objects.filter(id__in=selected_breakfast)
        lunchs=Lunchtbl.objects.filter(id__in=selected_lunch)
        dinners=Dinnertbl.objects.filter(id__in=selected_dinner)

        if breakfasts:
            mealobj.breakfastOBJS.set(breakfasts)
        else:
            mealobj.breakfastOBJS.clear()
        if lunchs:
            mealobj.lunchOBJS.set(lunchs)
        else:
            mealobj.lunchOBJS.clear()
        if dinners:
            mealobj.dinnerOBJS.set(dinners)
        else:
            mealobj.dinnerOBJS.clear()
        mealobj.save()
        messages.success(request, "Meals updated for "+str(mealobj.date))
        return redirect('/warden/mealsplan')

    return render(request,'editmeal.html',{'mealobj':mealobj,
                                           'breakfastobjs':breakfastobjs,'lunchobjs':lunchobjs,'dinnerobjs':dinnerobjs,
                                           'funcall':funcall,'selectedmealsobjs':selectedmealsobjs})



def studentsBillAmount(selected_meals):
    student_bills={}
    for meal in selected_meals:
        if not meal.bill_generated_status:
            student = meal.studentOBJ
            if student not in student_bills:
                student_bills[student] = 0    
            student_bills[student] += meal.price
    return student_bills

def billDate(request):

    if request.method=='POST':
        startdate=request.POST.get('startdate')
        enddate=request.POST.get('enddate')
        print(startdate,enddate)

        studentmealobjs=Selectedmealtbl.objects.filter(plannedmealOBJ__date__range=(startdate,enddate))
        print(studentmealobjs)

        studentsbilldetails=studentsBillAmount(studentmealobjs)
        print(studentsbilldetails)

        return render(request,'bill_date.html',{'startdate':startdate,'enddate':enddate,'studentsbilldetails':studentsbilldetails})

    return render(request,'bill_date.html')

def generateAllBills(request):
    # return render(request,'bill_date.html')
    
    """
    This view handles generating bills for all students.
    """
    if request.method == 'POST':
        startdate = request.POST.get('startdate')
        enddate = request.POST.get('enddate')

        # Fetch selected meals in the date range
        studentmealobjs = Selectedmealtbl.objects.filter(plannedmealOBJ__date__range=(startdate, enddate))
        studentsbilldetails = studentsBillAmount(studentmealobjs)
        
        # Generate bills for all students
        for student, amount in studentsbilldetails.items():
            # Logic to generate a bill for each student
            # Update the bill generation status in your database model
            print(f"Generating bill for {student} with amount {amount}")
            # Example update: student.update(bill_generated_status=True) or create a Bill record

        return redirect('bill_date') 
    return redirect('bill_date')  # Redirect back to the bill date form if not a POST request
