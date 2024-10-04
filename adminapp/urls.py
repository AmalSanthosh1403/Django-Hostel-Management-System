from . import views
from django.urls import path
from django.conf.urls.static import static    #this 2 itmes are importing for assecing the uploaded files
from django.conf import settings

urlpatterns=[
    path('home',views.adminHome,name='home'),
    path('profile',views.adminProfile,name='profile'),
    path('approvewarden',views.approveWarden,name='approvewarden'),
    path('approvestudent',views.approveStudent,name='approvestudent'),
    path('processapprovel',views.processApprovel,name='processapprovel'),
    path('viewrooms/<int:hid>',views.viewRooms,name='viewrooms'),
    path('addrooms/<int:hid>',views.addRooms,name='addrooms'),
    path('roomdetails/<int:rid>',views.roomDetails,name='roomdetails'),
    path('updateroom/<int:rid>',views.updateRooms,name='updateroom'),
    path('viewallmeals',views.viewallMealsPlan,name='viewallmeals'),
    path('approvemealsplan/<int:mid>',views.approveMealsPlan,name='approvemealsplan'),
    path('rejectmealsplan/<int:mid>',views.rejectMealsPlan,name='rejectmealsplan'),
    path('mealalldetails/<int:mid>',views.mealAllDetails,name='mealalldetails'),
    path('deletestudentselectedmeal/<int:mid>/<int:sid>',views.deleteStudentSelectedMeal,name='deletestudentselectedmeal'),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)