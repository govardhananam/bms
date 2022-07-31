from django import forms
from .models import Appointment, course,unit, procedure
from datetime import date
from address.forms import AddressField
from django.contrib.auth import get_user_model

User = get_user_model()



class AppointmentForm(forms.ModelForm):
    class Meta:
        model=Appointment
        date = forms.DateField(initial=date.today)
        address = AddressField()
        fields=[
            "date",
            "time_start",
            "time_end",
            "room_number",
            "appointment_with",
            "slot",
            "course",
            "unit",
            "procedure",
            "address",

        ]
    def __init__(self, *args, **kwargs):
         super().__init__(*args, **kwargs)
         

         self.fields['unit'].queryset = unit.objects.none()

         if 'course' in self.data:
            try:
                 course_id = int(self.data.get('course'))
                 self.fields['unit'].queryset = unit.objects.filter(course_id=course_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty unit queryset
         elif self.instance.pk:
            self.fields['unit'].queryset = self.instance.course.unit_set.order_by('name')

         self.fields['procedure'].queryset = unit.objects.none()
         if 'unit' in self.data:
             try:
                 unit_id = int(self.data.get('unit'))
                 self.fields['procedure'].queryset = procedure.objects.filter(unit_id=unit_id).order_by('name')
             except (ValueError, TypeError):
                 pass  # invalid input from the client; ignore and fallback to empty unit queryset
         elif self.instance.pk:
            #self.fields['vanue'].queryset = self.instance.country.city.vanue_set.order_by('name')
             self.fields['procedure'].queryset = self.instance.unit.procedure_set.order_by('name')
        

class CourseForm(forms.ModelForm):
    class Meta:
        model = procedure
        fields=[
            "course",
            "unit",
            "name",
        ]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields =[
            'profile',
            'first_name', 
            'last_name',
            'email', 
            'password',
            'course',
        ]

class GroupForm(forms.ModelForm):
    class Meta:
        model =User
        fields =[
            'course',
            'groups',
        ]