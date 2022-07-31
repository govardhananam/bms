from enum import unique
from django.db import models
from django.conf import settings
from datetime import date
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField
from address.models import AddressField
from easy_select2 import select2_modelform


class course(models.Model):
	class Meta:
		unique_together =[('c_id', 'name')]
	c_id = models.IntegerField(null=True,blank=True)
	name= models.CharField(max_length=255)
	
	def __str__(self):
		return self.name
		

class unit(models.Model):
	class Meta:
		unique_together =[('u_id', 'name')]
	u_id = models. IntegerField(null=True, blank= True)
	course= models.ForeignKey(course, on_delete=models.CASCADE)
	name = models.CharField(max_length=255)


	def __str__(self):
		return self.name
		

class procedure(models.Model):
	course= models.ForeignKey(course, on_delete=models.CASCADE)
	unit=models.ForeignKey(unit, on_delete=models.CASCADE)
	name=models.CharField(max_length=255)

	def __str__(self):
		return self.name

# Database creation for teacher appointment.
class Appointment(models.Model):
	#class Meta:
		#unique_together =['date','time_start','time_end','room_number','appointment_with'] #enable if you wanna enforce single appointment for the teacher end
	user=models.ForeignKey(settings.AUTH_USER_MODEL,blank=True, null=True,on_delete=models.DO_NOTHING)
	date=models.DateField(null=True, blank=True)
	time_start=models.TimeField(auto_now=False, auto_now_add=False,null=True, blank=True)
	time_end=models.TimeField(auto_now=False, auto_now_add=False,null=True, blank=True)
	room_number=models.CharField(max_length=50)
	appointment_with=models.CharField(max_length=50,blank=True)
	update_time=models.DateField(auto_now=True, auto_now_add=False)
	frist_time=models.DateField(auto_now=False, auto_now_add=True)
	slot=models.IntegerField(default=1)
	address=AddressField(on_delete=models.CASCADE, null=True, blank=True)
	#address2 =AddressField(related_name='+', blank=True, null=True)
	#Foreign Keys
	course=models.ForeignKey(course, on_delete=models.SET_NULL, null=True)
	unit=models.ForeignKey(unit, on_delete=models.SET_NULL, null=True)
	procedure= models.ForeignKey(procedure, on_delete=models.SET_NULL, null=True)
	
	#show filled in admin panel
	def __str__(self):
		return self.date
	def __str__(self): 
		return self.time_start
	def __str__(self): 
		return self.time_end
	def __str__(self): 
		return self.room_number
	def __str__(self): 
		return self.appointment_with
	
	

