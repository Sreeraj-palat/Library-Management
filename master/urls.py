from django.urls import path
from . import views

urlpatterns = [
    path('',views.masterHome,name='master-home'),
    path('master-home/',views.masterHome,name='master-home'),
    path('master-login/',views.master_login, name='master-login'),
    path('master_logout/',views.master_logout, name='master_logout'),
    path('master-register/',views.master_registration, name='master-register'), 

    path('add_book/', views.add_book, name='add_book'),
    path('edit_book/<int:id>/', views.edit_book, name='edit_book'), 
    path('delete_book/<int:id>/', views.delete_book, name='delete_book'), 
    path('book_list/', views.book_list, name='book_list'), 

    path('student-list/', views.student_list, name='student-list'),
    path('block-student/<int:id>/', views.block_unblock_student, name='block-student'), 
]