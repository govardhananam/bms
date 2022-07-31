from django.contrib import admin
#from django.contrib.auth.models import PermissionsMixin
# Register your models here.

from .models import Appointment, course, unit, procedure
from address.models import AddressField
from address.forms import AddressWidget

class TeacherAdmin(admin.ModelAdmin):
	list_display = ["date", "time_start","time_end","room_number","appointment_with","address"]
	list_filter = ('date', 'update_time')
	formfield_overrides = {AddressField: {"widget": AddressWidget(attrs={"style": "width: 300px;"})}}
'''

class CourseInline(admin.TabularInline):
	model = course

class UnitInline(admin.TabularInline):
	model =unit

class ProcedureInline(admin.TabularInline):
	model=procedure

class AppointmentInline(admin.TabularInline):
	model=Appointment

class  TeacherAdmin(admin.ModelAdmin):
	inlines =[
		CourseInline,
		UnitInline,
		ProcedureInline,
		Appointment,


]
'''


admin.site.register(Appointment, TeacherAdmin)
admin.site.register(course)
admin.site.register(unit)
admin.site.register(procedure)
