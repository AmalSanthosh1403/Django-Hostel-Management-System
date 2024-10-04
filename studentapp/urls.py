from django.urls import path
from . import views

urlpatterns=[
    path('',views.indexPage,name='indexpage'),
    path('login',views.loginPage,name='login'),
    path('registration',views.registrationnPage,name='registration'),
    path('logout',views.logoutFun,name='logout'),
    path('home',views.homePage,name='home'),
    path('myprofile',views.studentProfile,name='myprofile'),
    path('approval',views.studentApprovalStatus,name='approval'),
    path('reapproval',views.studentReApproval,name='reapproval'),  
    path('studentroomdetails',views.studentroomDetails,name='studentroomDetails'), 
    path('studentviewallrooms/<int:hid>',views.studentViewAllRooms,name='studentviewallrooms'),
    path('studentscheduledmeals',views.studentViewScheduledMeals,name='studentViewScheduledMeals'), 
    path('studentconfirmmeals/<int:mid>',views.confirmMealsPlan,name='studentconfirmmeals'),

]