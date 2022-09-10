from django.urls import path
from . import views

urlpatterns = [
    
    path('student-home/',views.student_home,name='student-home'),
    path('student-login/',views.student_login, name='student-login'),
    path('student_logout/',views.student_logout, name='student_logout'),
    path('student-register/',views.student_registration, name='student-register'), 
    
]