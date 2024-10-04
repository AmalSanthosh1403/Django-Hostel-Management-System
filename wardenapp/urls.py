from . import views
from django.urls import path

urlpatterns=[
    path('wardenregistration',views.wardenRegistration,name='wardenregistration'),
    path('home',views.homePage,name='home'),
    path('profile',views.wardenProfile,name='profile'),
    path('approval',views.wardenApprovalStatus,name='approval'),
    path('reapproval',views.wardenReApproval,name='reapproval'),
    path('approvestudent',views.approveStudent,name='approvestudent'),
    path('processapproval',views.processApproval,name='processapproval'),
    path('viewallrooms/<int:hid>',views.viewAllRooms,name='viewallrooms'),
    path('wardenrooms',views.wardenRooms,name='wardenrooms'),
    path('wardenroomdetails/<int:rid>',views.wardenroomDetails,name='wardenroomdetails'),
    path('addstudent/<int:rid>',views.addStudent,name='addstudent'),
    path('removestudent/<int:rid>/<int:sid>',views.removeStudent,name='removestudent'),
    path('mealsplan',views.viewMealsPlan,name='mealsplan'),
    path('newmealsplan',views.addNewMealsPlan,name='newmealsplan'),
    path('editmealsplan/<int:mid>/<int:funcall>',views.editMealsPlan,name='editmealsplan'),
    path('deletemealsplan/<int:mid>',views.deleteMealsPlan,name='deletemealsplan'),
    path('billdate',views.billDate,name='billdate'),
    path('generateallbills',views.generateAllBills,name='generateallbills'),



]