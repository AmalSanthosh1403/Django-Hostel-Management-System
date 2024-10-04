from django.shortcuts import render,redirect
from django.contrib import messages

from . models import *
from adminapp.views import *


def indexPage(request):
    # try :       #if login compledt
    #     request.session['user_id']
    try:
        Studentstbl.objects.get(id=request.session['user_id'])
        return redirect('/home')
    except:
        try:
            Wardentbl.objects.get(id=request.session['warden_id'])
            return redirect('/warden/home')  
        except:
            try:
                Admintbl.objects.get(id=request.session['admin_id'])
                return redirect('/adminapp/home')  
            except:
                return render (request,'index.html')
   
def logoutFun(request):
    try:
        del request.session['user_id']
        return redirect('/')
    except:
        try:
            del request.session['warden_id']
            return redirect('/')
        except:
            try:
                del request.session['admin_id']
                return redirect('/')
            except:
                return render (request,'index.html')

def loginPage(request):
    if request.method=='POST':
        email1=request.POST.get('em')
        pass1=request.POST.get('psw')
        try : 
            request.session['user_id']=Studentstbl.objects.get(email=email1,password=pass1).id
            return redirect('/home')
        except:
            try :
                request.session['admin_id']=Admintbl.objects.get(adminemail=email1,adminpassword=pass1).id
                return redirect('/adminapp/home')
            except:
                try:
                    request.session['warden_id']=Wardentbl.objects.get(wemail=email1,wpassword=pass1).id
                    return redirect('/warden/home')
                except:
                    return render(request,'loginpage.html',{"error_msg":"Invalid Email or Password"})  #dict for showing an error msg 
    return render (request,'loginpage.html')


def registrationnPage(request):
    if request.method=='POST':
        name1=request.POST.get('nm')
        place1=request.POST.get('pl')
        email1=request.POST.get('em')
        pass1=request.POST.get('psw')
        age1=request.POST.get('age')
        phone1=request.POST.get('ph')

        # already_exist=Studentstbl.objects.filter(email=email1)  another function named already_exist declred in adminapp
        if already_exist(email1):
            return render(request,'registrationpage.html',{'error_reg':'Email Already Exists'})
        else:
            obj=Studentstbl.objects.create(
                name=name1,
                place=place1,
                age=age1,
                phone=phone1,
                email=email1,
                password=pass1,
            )
            obj.save()

            if obj:
                return redirect('/login')
            else:
                return render(request,'registrationpage.html')

    return render (request,'registrationpage.html')

def homePage(request):
    # obj=Studentstbl.objects.get(id=request.session['user_id'])

    return render(request,'homepagestudent.html')

def studentProfile(request):
    obj=Studentstbl.objects.get(id=request.session['user_id'])
    return render(request,'studentprofile.html',{'obj':obj})

def studentApprovalStatus(request):
    obj=Studentstbl.objects.get(id=request.session['user_id'])
    return render(request,'studentapproval.html',{'obj':obj})

def studentReApproval(request):
    obj=Studentstbl.objects.get(id=request.session['user_id'])
    obj.approval_request_count+=1
    obj.save()
    messages.success(request,'Approval Request sended successfully.')
    return redirect('/approval')

def studentroomDetails(request):
    studentobj=Studentstbl.objects.get(id=request.session['user_id'])
    try:
        roomobj=Roomtbl.objects.get(id=studentobj.roomOBJ.id)
        studentobjs_in_room=Studentstbl.objects.filter(roomOBJ=roomobj)
        wardenobjs=roomobj.wardenOBJ.all()
        return render(request,'studentroomDetails.html',{'obj':studentobj,'roomobj':roomobj,'studentobjs':studentobjs_in_room,'wardenobjs':wardenobjs})
    except:
        return render(request,'studentroomDetails.html')

def studentViewAllRooms(request,hid):
    # hid=request.GET.get('hid')
    hostelobj=Hosteltbl.objects.get(id=hid)
    roomobjs=Roomtbl.objects.filter(hostelOBJ=hostelobj)
    return render(request,'studentviewallrooms.html',{'hostelobj':hostelobj,'roomobjs':roomobjs})


def studentViewScheduledMeals(request):
    studentobj=Studentstbl.objects.get(id=request.session['user_id'])
    availablemealobjs=ScheduledMealdtbl.objects.filter(mealapprovel=True)
    selectedmeals=Selectedmealtbl.objects.filter(studentOBJ=studentobj)
    
    selected_planned_meal_ids = selectedmeals.values_list('plannedmealOBJ', flat=True)
    sample_dict={}
    for availablemealobj in availablemealobjs:
        if availablemealobj.id in selected_planned_meal_ids:
            sample_dict[availablemealobj]=(Selectedmealtbl.objects.get(plannedmealOBJ=availablemealobj,studentOBJ=studentobj))
        else:   
            sample_dict[availablemealobj]=None
    # print(sample_dict)
    return render(request,'studentviewmealsplan.html',{'studentobj':studentobj,'sample_dict':sample_dict})


def confirmMealsPlan(request,mid):
    studentobj=Studentstbl.objects.get(id=request.session['user_id'])
    mealobj=ScheduledMealdtbl.objects.get(id=mid)
    breakfastobjs=mealobj.breakfastOBJS.all
    lunchobjs=mealobj.lunchOBJS.all
    dinnerobjs=mealobj.dinnerOBJS.all
    try:
        confirmedmealobj=Selectedmealtbl.objects.get(plannedmealOBJ=mealobj,studentOBJ=studentobj)   # students selected meal plan done 
        confirmedBreakfast=confirmedmealobj.breakfastOBJ.all
        confirmedLunch=confirmedmealobj.lunchOBJ.all
        confirmedDinner=confirmedmealobj.dinnerOBJ.all
        total=confirmedmealobj.price
    except:
        confirmedBreakfast=None
        confirmedLunch=None
        confirmedDinner=None
        total=0

    if request.method=="POST":
        selected_breakfast=request.POST.getlist('allbreakfast')
        selected_lunch=request.POST.getlist('alllunch')
        selected_dinner=request.POST.getlist('alldinner')

        breakfasts=Breakfasttbl.objects.filter(id__in=selected_breakfast)
        lunchs=Lunchtbl.objects.filter(id__in=selected_lunch)
        dinners=Dinnertbl.objects.filter(id__in=selected_dinner)

        #amount
        Btotal=breakfasts.values_list('dishprice', flat=True)   # values_list gives a list with combination of tuples, flat=True is used to remove the tuple
        Ltotal=lunchs.values_list('dishprice', flat=True)   
        Dtotal=dinners.values_list('dishprice', flat=True)   
        # print(Btotal,sum(Btotal),Ltotal,Dtotal)
        total_sum=sum(Btotal)+sum(Ltotal)+sum(Dtotal)

        newselectedmeal,created=Selectedmealtbl.objects.get_or_create(plannedmealOBJ=mealobj,studentOBJ=studentobj)
        if not created:
            if breakfasts:
                newselectedmeal.breakfastOBJ.set(breakfasts)
            else:
                newselectedmeal.breakfastOBJ.clear()
            if lunchs:
                newselectedmeal.lunchOBJ.set(lunchs)
            else:
                newselectedmeal.lunchOBJ.clear()
            if dinners:
                newselectedmeal.dinnerOBJ.set(dinners)
            else:
                newselectedmeal.dinnerOBJ.clear()
        else:
            
            newselectedmeal.plannedmealOBJ=mealobj
            newselectedmeal.breakfastOBJ.set(breakfasts)
            newselectedmeal.lunchOBJ.set(lunchs)
            newselectedmeal.dinnerOBJ.set(dinners)
            newselectedmeal.studentOBJ=studentobj
        
        newselectedmeal.status=True
        newselectedmeal.price=total_sum
        newselectedmeal.save()
        messages.success(request, "Successfully Mess Submitted for "+str(mealobj.date))
        return redirect('/studentscheduledmeals')

    return render(request,'confirm_meal.html',
                  {'mealobj':mealobj,'breakfastobjs':breakfastobjs,'lunchobjs':lunchobjs,'dinnerobjs':dinnerobjs,
                   'confirmedBreakfast':confirmedBreakfast,
                   'confirmedLunch':confirmedLunch,
                   'confirmedDinner':confirmedDinner,
                   'currenttotal':total
                   })

