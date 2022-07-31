from django.urls import path
from . import views

from django.urls import re_path as url
from django.contrib import admin

from .views import(
	student,
	quick_appointment,
	appointment_book,
	student_support,
    appointment_student_delete
	)

urlpatterns = [
    path('', views.quick_appointment, name='quick_appointmnet'),
    path('my_appointment/', views.student, name='student'),
    path('quick_appointment/', views.quick_appointment, name='quick_appointmnet'),   
    path('update/<int:id>/', views.appointment_book,name='appointment_update'),
    path('my_appointment/delete/<int:id>/', appointment_student_delete,name='appointment_student_delete'), #delete
    


    path('ajax/load_units/', views.load_units, name='student_ajax_load_units'), #dropdown load units    
    path('ajax/load_procedures/', views.load_procedures, name='student_ajax_load_procedures'), # dropdown load procedures


    path('student_support/',views.student_support, name='student_support'),
    path('student_profile/',views.student_profile, name='student_profile'),

      
]