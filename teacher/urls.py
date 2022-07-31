from django.urls import path
from . import views

from django.urls import re_path as url
from django.contrib import admin

from .views import(
	teacher,
	teacher_appointment_list,
	appointment_delete,
	teacher_appointment_update,
    add_appointment,
    load_units,
    load_procedures,
    teacher_appointment_all,
    teacher_active_bookings,
    teacher_manage_courses,
    teacher_visualise,
    teacher_support,
    teacher_profile,
    #load_courses,
	)

'''
def teacher_active_bookings(request):
    return render(request, 'teacher_active_bookings.html')

def teacher_manage_courses(request):
    return render(request, 'teacher_manage_courses.html')

def teacher_visualise(request):
    return render(request, 'teacher_visualise.html')

def teacher_support(request):
    return render(request, 'teacher_support.html')

def teacher_profile(request):
    return render(request, 'teacher_edit_profile.html')

'''

urlpatterns = [
    path('', views.teacher, name='teacher_home'), #dashboard
    path('my_appointment/', views.teacher, name='teacher_appointment'), # dashboard
    path('list_appointment/',teacher_appointment_all, name='teacher_actions_list'), # All Bookings
    path('create_appointment/', views.teacher_appointment_list, name='teacher_appointment_list'), # Create Bookings
    path('create_appointment/delete/<int:id>/', appointment_delete,name='appointment_delete'), #delete
    path('create_appointment/update/<int:id>/', teacher_appointment_update,name='teacher_appointment_update'), # update
    path('create_appointment/add/<int:id>/',add_appointment,name='add_appointment'), # add slot not used yet
    #path('ajax/load_courses/', views.load_courses, name='ajax_load_courses'),    
    path('ajax/load_units/', views.load_units, name='ajax_load_units'), #dropdown load units    
    path('ajax/load_procedures/', views.load_procedures, name='ajax_load_procedures'), # dropdown load procedures

    path('teacher_active_bookings/',teacher_active_bookings, name='teacher_active_bookings'), # Active Bookings
    path('teacher_manage_courses/',teacher_manage_courses, name='teacher_manage_courses'), # Manage Courses
    path('teacher_visualise/',teacher_visualise, name='teacher_visualise'), # Visualise
    path('teacher_support/',teacher_support, name='teacher_support'), # Support
    path('teacher_profile/',teacher_profile, name='teacher_profile'), # Profile

      
]

