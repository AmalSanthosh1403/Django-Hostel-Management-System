from django.shortcuts import render,redirect
from django.contrib import messages
from django.urls import reverse
from .models import *
from studentapp.models import *
from wardenapp.models import *
from django.contrib.auth.models import User


def already_exist(email1):
    if Studentstbl.objects.filter(email=email1) or Admintbl.objects.filter(adminemail=email1) or Hosteltbl.objects.filter(hemail=email1) or Wardentbl.objects.filter(wemail=email1) or User.objects.filter(email=email1):
        return True
    else:
        return False

def adminHome(request):
    obj=Admintbl.objects.get(id=request.session['admin_id'])
    # hostelobjs=Hosteltbl.objects.all()
    return render(request,'homepageadmin.html')

def adminProfile(request):
    obj=Admintbl.objects.get(id=request.session['admin_id'])
    return render(request,'adminprofile.html',{'obj':obj})

def approveWarden(request):
    obj=Admintbl.objects.get(id=request.session['admin_id'])
    wardenobjs=Wardentbl.objects.filter(wapproval=False)
    return render(request,'approvalwarden.html',{'wardenobjs':wardenobjs,'obj':obj})

def approveStudent(request):
    obj=Admintbl.objects.get(id=request.session['admin_id'])
    studentobjs=Studentstbl.objects.filter(sapproval=False)
    return render(request,'approvalstudent.html',{'studentobjs':studentobjs,'obj':obj})

def processApprovel(request):
    try:
        wardenid=request.GET.get('wid')
        wardenobj=Wardentbl.objects.get(id=wardenid)
        wardenobj.wapproval=True    
        wardenobj.save()
        return redirect('/adminapp/approvewarden')
    except:
        studentid=request.GET.get('sid')
        studentobj=Studentstbl.objects.get(id=studentid)
        studentobj.sapproval=True
        studentobj.save()
        return redirect('/adminapp/approvestudent')
    
# def addHostel(request):
#         if request.method=="POST":
#         roomno=request.POST.get('roomno')
#         students=request.POST.get('students_count')
#         beds=request.POST.get('beds_count')
#         roomphoto=request.FILES.get('roomphoto')
#         if Roomtbl.objects.filter(roomid=roomno):
#             messages.success(request,'Failed...Room number already exists')
#             return redirect('/adminapp/addrooms')
#         newroomobj=Roomtbl.objects.create(
#             roomid=roomno,
#             students_count=students,
#             beds_count=beds,
#             room_photo=roomphoto,
#             hostel=hostelobj
#         )
#         if newroomobj:
#             newroomobj.save()
#             messages.success(request,'Room created!...')
#             return redirect('/adminapp/addrooms')
#         else:
#             messages.success(request,'Failed...')
#             return redirect('/adminapp/addrooms')

#     return render(request,'addrooms.html')


def viewRooms(request,hid):
    # request.session['hostel_id']=request.GET.get('hid')
    hostelobj=Hosteltbl.objects.get(id=hid)
    roomobjs=Roomtbl.objects.filter(hostelOBJ=hostelobj)
    return render(request,'viewrooms.html',{'hostelobj':hostelobj,'roomobjs':roomobjs})

def addRooms(request,hid):
    if request.method=="POST":
        hostelobj=Hosteltbl.objects.get(id=hid)
    
        roomno=request.POST.get('roomno')
        students=request.POST.get('students_count')
        beds=request.POST.get('beds_count')
        roomphoto=request.FILES.get('roomphoto')
        if Roomtbl.objects.filter(roomid=roomno):
            messages.success(request,'Failed...Room number already exists')
            return redirect('/adminapp/addrooms')
        newroomobj=Roomtbl.objects.create(
            roomid=roomno,
            students_count=students,
            beds_count=beds,
            room_photo=roomphoto,
            hostelOBJ=hostelobj
        )
        if newroomobj:
            newroomobj.save()
            messages.success(request,'Room created!...')
            return redirect('/adminapp/addrooms')
        else:
            messages.success(request,'Failed...')
            return redirect('/adminapp/addrooms')

    return render(request,'addrooms.html')

def roomDetails(request,rid):
    roomobj=Roomtbl.objects.get(id=rid)
    wardenobjs=Wardentbl.objects.all()
    studentobjs=Studentstbl.objects.filter(roomOBJ=roomobj)
    return render(request,'roomdetails.html',{'roomobj':roomobj,'wardenobjs':wardenobjs,'studentobjs':studentobjs})

def updateRooms(request,rid):
    if request.method=='POST':
        totalstu=request.POST.get('totalstu')
        totalbed=request.POST.get('totalbed')
        selected_wardens_id=request.POST.getlist('allwarden')
        selected_wardens_objs=Wardentbl.objects.filter(id__in=selected_wardens_id)
        roomimg=request.FILES.get('roomimg')

        roomobj=Roomtbl.objects.get(id=rid)

        roomobj.students_count=totalstu
        roomobj.beds_count=totalbed
        if selected_wardens_objs:
            roomobj.wardenOBJ.set(selected_wardens_objs)
        else:
            roomobj.wardenOBJ.clear() 
        if roomimg:
            roomobj.room_photo=roomimg
        roomobj.save()
        messages.success(request, "Room details updated successfully.")

        roomDetails_url=reverse('roomdetails',kwargs={'rid':rid})
        return redirect(roomDetails_url)
    
def viewallMealsPlan(request):
    availablemealobjs=ScheduledMealdtbl.objects.all()
    return render(request,'admin_mealsplan.html',{'availablemealobjs':availablemealobjs})

def approveMealsPlan(request,mid):
    mealobj=ScheduledMealdtbl.objects.get(id=mid)
    mealobj.mealapprovel=True
    mealobj.save()
    return redirect('/adminapp/viewallmeals')

def rejectMealsPlan(request,mid):
    mealobj=ScheduledMealdtbl.objects.get(id=mid)
    mealobj.delete()
    return redirect('/adminapp/viewallmeals')

def mealAllDetails(request,mid):
    mealobj=ScheduledMealdtbl.objects.get(id=mid)
    breakfastobjs=Breakfasttbl.objects.all()
    lunchobjs=Lunchtbl.objects.all()
    dinnerobjs=Dinnertbl.objects.all()
    selectedmealsobjs=Selectedmealtbl.objects.filter(plannedmealOBJ=mealobj)

    # if request.method=="POST":


    #     selected_breakfast=request.POST.getlist('allbreakfast')
    #     selected_lunch=request.POST.getlist('alllunch')
    #     selected_dinner=request.POST.getlist('alldinner')

    #     breakfasts=Breakfasttbl.objects.filter(id__in=selected_breakfast)
    #     lunchs=Lunchtbl.objects.filter(id__in=selected_lunch)
    #     dinners=Dinnertbl.objects.filter(id__in=selected_dinner)

    #     if breakfasts:
    #         mealobj.breakfastOBJS.set(breakfasts)
    #     else:
    #         mealobj.breakfastOBJS.clear()
    #     if lunchs:
    #         mealobj.lunchOBJS.set(lunchs)
    #     else:
    #         mealobj.lunchOBJS.clear()
    #     if dinners:
    #         mealobj.dinnerOBJS.set(dinners)
    #     else:
    #         mealobj.dinnerOBJS.clear()
    #     mealobj.save()
    #     messages.success(request, "Meals updated for "+str(mealobj.date))
    #     return redirect('/warden/mealsplan')

    return render(request,'mealalldetailsl.html',{'mealobj':mealobj,
                                                'breakfastobjs':breakfastobjs,'lunchobjs':lunchobjs,'dinnerobjs':dinnerobjs,
                                                'selectedmealsobjs':selectedmealsobjs})

def deleteStudentSelectedMeal(request,mid,sid):
    mealobj=ScheduledMealdtbl.objects.get(id=mid)
    studentobj=Studentstbl.objects.get(id=sid)
    sudent_selectedmealsobj=Selectedmealtbl.objects.get(plannedmealOBJ=mealobj,studentOBJ=studentobj)
    sudent_selectedmealsobj.delete()
    try: 
        request.session['admin_id']
        meal_alldetails_url=reverse('mealalldetails',kwargs={'mid':mid})
        # return redirect(meal_alldetails_url)
    except:
        meal_alldetails_url=reverse('editmealsplan',kwargs={'mid':mid,'funcall':1})
    return redirect(meal_alldetails_url)