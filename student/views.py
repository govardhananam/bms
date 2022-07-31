from django.contrib.auth import get_user_model
from django.db.models.fields import NullBooleanField
from django.http.response import JsonResponse
from django.views.generic import TemplateView
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404,redirect
from teacher.models import Appointment, course, unit, procedure
from teacher.forms import AppointmentForm, ProfileForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.db.models import Q
from django.core import serializers
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.conf import settings
from django. template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from address.models import AddressField
import json
from datetime import datetime, date, time
from django.utils import timezone
import easy_date
from django.db import transaction, DatabaseError
from django.db.models import DateTimeField, ExpressionWrapper, F



User = get_user_model()




#function to check the form input validity

def is_valid_filter_parameters(param):
    return param != '' and param is not None




@login_required
def quick_appointment(request):
    global appointments, c, u, p
    appointments ={}
    group_name=Group.objects.all().filter(user = request.user)# get logged user grouped name
    group_name=str(group_name[0]) # convert to string

    #filter rendering
    if "Student" == group_name and request.method =="POST":
        user_name=request.user.get_full_name()
        #a= request.user.course.all()
        a = request.user.course.first()
        b = request.user.course.last()
       
        

        #distinct view
        appointment_list = Appointment.objects.all().order_by("-user").distinct("user","time_start","time_end","date","room_number", "appointment_with")#.filter(Q(date__gte = date.today()) & Q(time_start__gte=t))
         
        #view based on course selected 
        appointment_list = appointment_list.filter(Q(course__name__contains=a) | Q(course__name__contains=b),date__gte = date.today()).order_by('-date', '-time_start')

        #ordering view
        appointment_list = appointment_list.reverse()

        #datetime filter
        appointment_list= appointment_list.annotate(my_dt=ExpressionWrapper(F('date')+F('time_start'),output_field=DateTimeField())).filter(my_dt__gte=datetime.now())
        
        

        
        t_list =appointment_list.filter(appointment_with='')

        appointment_list = t_list
      
        #form Input
        course_details= request.POST.get('course')
        unit_details= request.POST.get('unit')
        procedure_details= request.POST.get('procedure')
        location_details=request.POST.get('address')
        date_details=request.POST.get('date')
        timestart_details=request.POST.get('time_start')
        timeend_details=request.POST.get('time_end') 

        
 
        
        #filters 
        if is_valid_filter_parameters(course_details): #course
            c = course.objects.filter(id=course_details)
            for course_d in c:
                c= course_d.name
            appointment_list= appointment_list.filter(course__name__contains=c)
                
        if is_valid_filter_parameters(unit_details): #unit
            u = unit.objects.filter(id=unit_details)
            for unit_d in u:
                u= unit_d.name 
            appointment_list= appointment_list.filter(unit__name__contains=u)
                
        if is_valid_filter_parameters(procedure_details): #procedure
            p = procedure.objects.filter(id=procedure_details)
            for procedure_d in p:
                p= procedure_d.name
            appointment_list= appointment_list.filter(procedure__name__contains=p)    


        if is_valid_filter_parameters(location_details): #address
            appointment_list= appointment_list.filter(address__formatted__contains=location_details)

        if is_valid_filter_parameters(date_details): #date
            date_formatted = easy_date.convert_from_string(date_details, '%d/%m/%Y', '%Y-%m-%d',date)
            appointment_list= appointment_list.filter(date__gte=date_formatted)
    


        if is_valid_filter_parameters(timestart_details): #time
            if is_valid_filter_parameters(timeend_details):
                appointment_list= appointment_list.filter(time_start__gte=timestart_details, time_end__lte=timeend_details)

           
        #search start
        q=request.GET.get("q")
        if q:
            appointment_list=appointment_list.filter(user__first_name__icontains=q)
        else:
            appointment_list = appointment_list
        # search end




        add_list = Appointment.objects.all().order_by('-address').values_list('address__formatted', flat=True).distinct()
        courseobj = course.objects.all()
        unitobj = unit.objects.all()
        procobj = procedure.objects.all()


      
            
        appointments={
            "query":appointment_list,
            "course":courseobj,
            "unit":unitobj,
            "procedure":procobj,
            "user_name":user_name,
            "address": add_list,
        }


        return render(request, 'student_quick_appointmnet.html', appointments)

        #original/initial render
    elif "Student" == group_name:
        user_name=request.user.get_full_name()
        

        #a = (User.objects.all().filter(email=request.user.email).order_by().values('course__name').first())
        a = request.user.course.first()
        
        b = request.user.course.last()
        
        
        
        #a = User.objects.all().values_list('course__name')
        #print(a)      
         
        #t = datetime.now().time().strftime("%I:%M %p").replace('AM', 'am').replace('PM', 'pm')

        #d = date.today()
        
        
     
        #distinct view
        appointment_list = Appointment.objects.all().order_by("-date").distinct("user","time_start","time_end","date","room_number", "appointment_with")#.filter(Q(date__gte = date.today()) & Q(time_start__gte=t))
         

        ##view based on course selected 
        appointment_list =appointment_list.filter(Q(course__name__contains=a) | Q(course__name__contains=b),date__gte = date.today()).order_by('-date', '-time_start')

        #ordering view
        appointment_list = appointment_list.reverse()


        #datetime condition
        appointment_list= appointment_list.annotate(my_dt=ExpressionWrapper(F('date')+F('time_start'),output_field=DateTimeField())).filter(my_dt__gte=datetime.now()) #tz=timezone.utc






        '''
        qs1= appointment_list.filter(appointment_with=user_name)

        qs1 = qs1.defer('appointment_with')

        #print(qs1)
        


        qs2 = appointment_list.filter(appointment_with='')
        qs2 = qs2.defer('appointment_with')
        diff_qs = qs2.difference(qs1)

        print(diff_qs)        '''

        #returing only empty obj for pagination support
        t_list =appointment_list.filter(appointment_with='')

        appointment_list = t_list
        

        

        add_list = Appointment.objects.all().order_by('-address').values_list('address__formatted', flat=True).distinct()
        courseobj = course.objects.all()
        unitobj = unit.objects.all()  #filter(course__name__contains=a)
        procobj = procedure.objects.all()



           
        q=request.GET.get("q")#search start
        if q:
            appointment_list=appointment_list.filter(procedure__name__contains=q)
        else:
            appointment_list = appointment_list# search end



        
        #pagination
        page = request.GET.get('page', 1)
        paginator = Paginator(appointment_list, 5)
        try:
            appointment_list = paginator.page(page)
        except PageNotAnInteger:
            appointment_list = paginator.page(1)
        except EmptyPage:
            appointment_list = paginator.page(paginator.num_pages)
       
        


        appointments= {
            "query": appointment_list,
            "user_name":user_name,
            "course":courseobj,
            "unit":unitobj,
            "procedure":procobj,
            "address": add_list,
            
        }
        return render(request, 'student_quick_appointmnet.html', appointments)
    
    else:
        return redirect('/')









#This section for my bookings
@login_required
def student(request):
    group_name=Group.objects.all().filter(user = request.user)# get logged user grouped name
    group_name=str(group_name[0]) # convert to string
    if "Student" == group_name:
        username = request.user.email
        user_name= username.rpartition('@')[0]
        #Getting all Post and Filter By Logged UserName
        appointment_list = Appointment.objects.all().order_by("-id").filter(appointment_with=username)
        
         #pagination
        page = request.GET.get('page', 1)
        paginator = Paginator(appointment_list, 5)
        try:
            appointment_list = paginator.page(page)
        except PageNotAnInteger:
            appointment_list = paginator.page(1)
        except EmptyPage:
            appointment_list = paginator.page(paginator.num_pages)


        q=request.GET.get("q")#search start
        if q:
            appointment_list=appointment_list.filter(user__first_name__icontains=q)
        else:
            appointment_list = appointment_list# search end


        appointments= {
            "query": appointment_list,
            "user_name":user_name,    
        }
        return render(request, 'student.html', appointments )
    else:
        return redirect('/')






@login_required
def appointment_book(request, id):#activate after clicking book now button
    group_name=Group.objects.all().filter(user = request.user)# get logged user grouped name
    group_name=str(group_name[0]) # convert to string
    if "Student" == group_name:
        #user_name=request.user.get_full_name()
        username = request.user.email
        #user_name= username.rpartition('@')[0] #getting the string before @ in email
        with transaction.atomic():
            try:
                single_appointment= Appointment.objects.select_for_update().get(id=id)
                form = single_appointment
        #c1 = Q(date=form.date)
        #c2 = Q(time_start= form.time_start)
        #c3 = Q(time_end= form.time_end)
        #c4 = Q(room_number= form.room_number)
        #c5 = Q(appointment_with=user_name)
        #print(c1,c2,c3,c4,c5)
                q= Appointment.objects.filter(date= form.date, time_start=form.time_start,time_end= form.time_end,room_number= form.room_number,address=form.address,appointment_with=username)
        #print(q) #to prevent same booking twice
        
                if q.exists():
                #raise ValueError('Booking already exists')
                    messages.error(request,"Booking already exists")
                else:
                    form.appointment_with=username
                    form.save()
                    messages.success(request, 'You have Booked Succesfully')
                    template = render_to_string('email_template.html',{'name':request.user.get_full_name(), 'd':form.date,'in':form.time_start, 'out':form.time_end, 'loc':form.room_number,'add':form.address, 'c':form.course, 'u':form.unit, 'p':form.procedure})
                    email = EmailMessage(
                    "Booking Confirmation",
                    template,
                    settings.EMAIL_HOST_USER,
                    [request.user.email],
                    )

                    email.fail_silently=True
                    email.send()
                    """
                     #return HttpResponseRedirect (instance.get_absolute_url())
                    """              
                return redirect('/student/')
            except ValueError:
                messages.error(request, 'This session is booked by another user, Please try again') 
            return redirect('/student/')      
    else:
        return redirect('/')









@login_required
def student_support(request):
    group_name=Group.objects.all().filter(user = request.user)# get logged user grouped name
    group_name=str(group_name[0]) # convert to string
    if "Student" == group_name and request.method=="POST":
        message_text= request.POST.get('message_textbox')
        if is_valid_filter_parameters(message_text):
            email_send=settings.EMAIL_HOST_USER,

            template = render_to_string('email_template_student_support.html',{'name':request.user.get_full_name(), 'email':request.user.email, 'message':message_text})
            email = EmailMessage(
            "Student Support Message",
            template,
            settings.EMAIL_HOST_USER,
            [email_send],
            )
            email.fail_silently=True
            email.send()
            messages.success(request, 'Message Sent Sucessfully')
        else:
            messages.error(request,'Message box is empty')
          
    return render(request, 'student_support.html')





@login_required
def student_profile(request):
    group_name=Group.objects.all().filter(user = request.user)# get logged user grouped name
    group_name=str(group_name[0]) # convert to string
    if "Student" == group_name:
        user = request.user
        form =ProfileForm(instance=user)
        if request.method=='POST':
            form =ProfileForm(request.POST, request.FILES,instance=user)
            if form.is_valid():
                saving=form.save(commit=True)
                saving.save()
                messages.success(request, "Profile Updated")
            else:
                messages.error(request, 'Error, Profile not Updated')
        profile= {
            "form":form,
        }
    return render(request, 'student_profile.html', profile)





@login_required
def appointment_student_delete(request, id):
    group_name=Group.objects.all().filter(user = request.user)# get logged user grouped name
    group_name=str(group_name[0]) # convert to string
    if "Student" == group_name:

        single_appointment= Appointment.objects.get(id=id)
        #b = course.objects.filter(single_appointment_id=id)
        #c= unit.objects.filter(b_id=b.id)
        #d= procedure.objects.filter(c_id=c.id).delete()

        single_appointment.appointment_with =''
        single_appointment.save()
        messages.success(request, 'Booking Deleted Succesfully')
        return redirect('/student/my_appointment/')
    else:
        return redirect('/')


#ajax load units dependent dropdown

@login_required
def load_units(request):
    course_id = request.GET.get('course')    
    units = unit.objects.filter(course_id=course_id).order_by('name')
    return JsonResponse(list(units.values('id','name')), safe=False)

    #context = {'units': units}
    #return render(request, 'units_dropdown_list_options.html', context)

# ajax load procedures dependent dropdown

@login_required
def load_procedures(request):
    unit_id = request.GET.get('unit')    
    procedures = procedure.objects.filter(unit_id=unit_id).order_by('name')
    return JsonResponse(list(procedures.values('id','name')), safe=False)