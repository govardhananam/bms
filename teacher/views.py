from datetime import date, datetime
from time import timezone
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.http.response import JsonResponse
from django.shortcuts import render, get_object_or_404,redirect
from .models import Appointment, unit,course, procedure
from .forms import AppointmentForm, CourseForm, ProfileForm
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.db.models import Q
import re
from django.core.mail import EmailMessage
from django.conf import settings
from django. template.loader import render_to_string

User = get_user_model()
#function to check the form input validity

def is_valid_filter_parameters(param):
    return param != '' and param is not None

def teacher(request):# Dashboard and Reserved Booked
    s=None
    t= None
    group_name=Group.objects.all().filter(user = request.user)# get logged user grouped name
    group_name=str(group_name[0]) # convert to string # Teacher
    if "Teacher" == group_name:
        user_name=request.user.get_username()#Getting Username

        #Getting all Post and Filter By Logged UserName
        appointment_list = Appointment.objects.all().order_by("-id").filter(user=request.user)


        t_list = appointment_list.filter(~Q(appointment_with=''))

        appointment_list = t_list

        total_students = User.objects.all().filter(groups= 2).count() # count total students

        current_bookings = Appointment.objects.all().order_by("-id").filter(user=request.user).exclude(appointment_with= '').count() # count currently booked

        available_bookings = Appointment.objects.all().order_by("-id").filter(user=request.user,appointment_with= '').count()

        total_bookings = (current_bookings + available_bookings)

        #Total users = User.objects.annotate(group_count= Count('groups')).count()



        labels=[]
        data =[]
        months=[]

        queryset_cb = Appointment.objects.all().order_by("-id").filter(user=request.user).exclude(appointment_with= '').count() # count currently booked
        queryset_ab = Appointment.objects.all().order_by("-id").filter(user=request.user, appointment_with= '').count() # active bookings
        queryset_total = queryset_cb+queryset_ab
        labels =['Current Bookings', 'Active Bookings', 'Total Bookings']
        data =[queryset_cb,queryset_ab,queryset_total]



         #last 3 months booked solts <line chart>
        t = Appointment.objects.all().values_list("date", flat=True).distinct().order_by('-date').reverse()[:3]
    
        for a in t:
            months.append(a.strftime("%B"))
        
        
        from datetime import datetime, timedelta

        #current_month = datetime.now().month
        current = Appointment.objects.all().order_by("-id").filter(user=request.user, date__gte=timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)).exclude(appointment_with= '').count()
    
   
        last_month = datetime.today() - timedelta(days=30)
        last = Appointment.objects.all().order_by("-id").filter(user=request.user, date__range=[last_month, timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)]).exclude(appointment_with= '').count()


        past_month = datetime.today() - timedelta(days=60)
        past = Appointment.objects.all().order_by("-id").filter(user=request.user, date__range=[past_month, last_month]).exclude(appointment_with= '').count()
    
    
        cb_data= [past,last,current]

        page = request.GET.get('page', 1)
        paginator = Paginator(appointment_list, 5)
        try:
            appointment_list = paginator.page(page)
        except PageNotAnInteger:
            appointment_list = paginator.page(1)
        except EmptyPage:
            appointment_list = paginator.page(paginator.num_pages)
        #print(appointment_list)
        q=request.GET.get("q") #search start
        if q:
            appointment_list=appointment_list.filter(date__icontains=q)
        else:
            appointment_list = appointment_list #search end
        '''
        for a in appointment_list:
            t = str(a.address)
            #t = t. replace(" ", "")
            pattern= ", (.*?),"
            t = re.search(pattern, t)
            print(t)
        '''

        for appoint in appointment_list: #loop to add + for url encoding of address
            #print(appoint.address) before
                s = str(appoint.address)
                s = s.replace(",","")
                s = s. replace(" ", "+")
                appoint.address = s
                #print(appoint.address) after


        appointments= {
            "query": appointment_list,
            "user_name":user_name,
            "total_students":total_students,
            "current_bookings":current_bookings,
            "available_bookings":available_bookings,
            "total_bookings":total_bookings,
            'labels':labels,
            'data':data,
            'month':months,
            'cb_data':cb_data,


            #"directions":t,

            #"form":AppointmentForm(),
        }
        return render(request, 'teacher.html', appointments )
    else:
        return redirect('/')









# Create Booking Form
def teacher_appointment_list(request):
    group_name=Group.objects.all().filter(user = request.user)# get logged user grouped name
    group_name=str(group_name[0]) # convert to string
    if "Teacher" == group_name:
        user_name=request.user.get_username()#Getting Username

        #Getting all Post and Filter By Logged UserName
        appointment_list = Appointment.objects.all().order_by("-id").filter(user=request.user)
        #print(appointment_list)
        q=request.GET.get("q") #search start
        if q:
            appointment_list=appointment_list.filter(date__icontains=q)
        else:
            appointment_list = appointment_list #search end

        appointments= {
            "query": appointment_list,
            "user_name":user_name,
            "form":AppointmentForm(),
        }
        form = AppointmentForm(request.POST or None)
        data = request.POST.get('slot', 1)
        #print(data)
        w = int(data)

        #suc_mes ='  Slot Created Sucessfully'

        #a =str(w)

        #a = a + suc_mes

        for i in range(w):
            if form.is_valid():
                saving=form.save(commit=False)
                saving.user=request.user
                saving.pk=None
                saving.save()     
                messages.success(request, 'Slots Created Sucessfully')
        return render(request, 'teacher_create_appointment.html', appointments )
    else:
        return redirect('/')






# All Bookings
def teacher_appointment_all(request):
    s = None # global variable for address preprocessing
    group_name=Group.objects.all().filter(user = request.user)# get logged user grouped name
    group_name=str(group_name[0]) # convert to string
    if "Teacher" == group_name:
        user_name=request.user.get_username()#Getting Username
         
        #Getting all Post and Filter By Logged UserName
        appointment_list = Appointment.objects.all().order_by("-id").filter(user=request.user)

        page = request.GET.get('page', 1)
        paginator = Paginator(appointment_list, 8)
        try:
            appointment_list = paginator.page(page)
        except PageNotAnInteger:
            appointment_list = paginator.page(1)
        except EmptyPage:
            appointment_list = paginator.page(paginator.num_pages)
        #print(appointment_list)
        q=request.GET.get("q") #search start
        if q:
            appointment_list=appointment_list.filter(date__icontains=q)
        else:
            appointment_list = appointment_list #search end

        for appoint in appointment_list: #function to add + for url encoding of address
            #print(appoint.address) before
                s = str(appoint.address)
                s = s.replace(",","")
                s = s. replace(" ", "+")
                appoint.address = s
                #print(appoint.address) after
 
        appointments= {
            "query": appointment_list,
            "user_name":user_name,
            #"form":AppointmentForm(),
        }
        return render(request, 'teacher_appointment_list.html', appointments )
    else:
        return redirect('/')


# delete a booking

def appointment_delete(request, id):
    group_name=Group.objects.all().filter(user = request.user)# get logged user grouped name
    group_name=str(group_name[0]) # convert to string
    if "Teacher" == group_name:
        single_appointment= Appointment.objects.get(id=id)
        #b = course.objects.filter(single_appointment_id=id)
        #c= unit.objects.filter(b_id=b.id)
        #d= procedure.objects.filter(c_id=c.id).delete()
        a = single_appointment.appointment_with
        use=a.rpartition('@')[0]
        single_appointment.delete()
        messages.success(request, 'Booking Deleted Succesfully')
        template = render_to_string('email_template_booking_cancellation.html',{'name':use, 'd':single_appointment.date,'in':single_appointment.time_start, 'out':single_appointment.time_end, 'loc':single_appointment.room_number,'add':single_appointment.address, 'c':single_appointment.course, 'u':single_appointment.unit, 'p':single_appointment.procedure})
        email = EmailMessage(
        "Booking Cancellation",
        template,
        settings.EMAIL_HOST_USER,
        [single_appointment.appointment_with],
        )
        email.fail_silently=True
        email.send()

        return redirect('/teacher/list_appointment/')
    else:
        return redirect('/')



# update a booking
def teacher_appointment_update(request,id):
    group_name=Group.objects.all().filter(user = request.user)# get logged user grouped name
    group_name=str(group_name[0]) # convert to string
    if "Teacher" == group_name:
        user_name=request.user.get_username()#Getting Username

        #Getting all Post and Filter By Logged UserName
        appointment_list = Appointment.objects.all().order_by("-id").filter(user=request.user)
        q=request.GET.get("q") #search start
        if q:
            appointment_list=appointment_list.filter(date__icontains=q)
        else:
            appointment_list = appointment_list #search end

        single_appointment= Appointment.objects.get(id=id)
        form = AppointmentForm(request.POST or None, instance=single_appointment)
        if form.is_valid():
                saving=form.save(commit=False)
                saving.user=request.user
                saving.save()
                messages.success(request, 'Post Created Sucessfully')
                return redirect('/teacher/create_appointment/')
                

        appointments= {
            "query": appointment_list,
            "user_name":user_name,
            "form":form,
        }

        return render(request, 'teacher_appointment_update.html', appointments )
    else:
        return redirect('/')


#Addition of slot. Not put in place yet

def add_appointment(request, id): #to add additional slot
    group_name=Group.objects.all().filter(user = request.user)# get logged user grouped name
    group_name=str(group_name[0]) # convert to string
    if "Teacher" == group_name:
        single_appointment= Appointment.objects.get(id=id)
        print(single_appointment)
        single_appointment.pk = None
        single_appointment.save()
        messages.success(request, 'Post Created Sucessfully')
        return redirect('/teacher/create_appointment/')
    else:
        return redirect('/')


#ajax load units dependent dropdown

def load_units(request):
    course_id = request.GET.get('course')    
    units = unit.objects.filter(course_id=course_id).order_by('name')
    return JsonResponse(list(units.values('id','name')), safe=False)

    #context = {'units': units}
    #return render(request, 'units_dropdown_list_options.html', context)

# ajax load procedures dependent dropdown

def load_procedures(request):
    unit_id = request.GET.get('unit')    
    procedures = procedure.objects.filter(unit_id=unit_id).order_by('name')
    return JsonResponse(list(procedures.values('id','name')), safe=False)

    
    #context = {'procedures': procedures}
'''  #return render(request, 'procedure_ddl.html', context)
def load_courses(request):
    courses =course.objects.all()
    print(list(courses.values('id','name')))
    context ={"course":courses}
    return render(request,"teacher_create_appointment.html", context)

'''
'''
def load_courses(request):
    course_id = request.GET.get('id')
    courses = course.objects.filter(id=course_id)
    print(list(courses.values('id','name')))
    context ={'courses':courses}
    return render(request, 'course_dropdown_list_options.html',context)
'''
# All active booking which are available for student to book right now

def teacher_active_bookings(request):
    s=None
    group_name=Group.objects.all().filter(user = request.user)# get logged user grouped name
    group_name=str(group_name[0]) # convert to string
    if "Teacher" == group_name:
        user_name=request.user.get_username()#Getting Username

        #Getting all Post and Filter By Logged UserName
        appointment_list = Appointment.objects.all().order_by("-id").filter(user=request.user)

        nt_list =appointment_list.filter(appointment_with ='')

        appointment_list=nt_list

        page = request.GET.get('page', 1)
        paginator = Paginator(appointment_list, 5)
        try:
            appointment_list = paginator.page(page)
        except PageNotAnInteger:
            appointment_list = paginator.page(1)
        except EmptyPage:
            appointment_list = paginator.page(paginator.num_pages)
        #print(appointment_list)
        q=request.GET.get("q") #search start
        if q:
            appointment_list=appointment_list.filter(date__icontains=q)
        else:
            appointment_list = appointment_list #search end

        for appoint in appointment_list: #function to add + for url encoding of address
            #print(appoint.address) before
                s = str(appoint.address)
                s = s.replace(",","")
                s = s. replace(" ", "+")
                appoint.address = s
                #print(appoint.address) after
        appointments= {
            "query": appointment_list,
            "user_name":user_name,
            #"form":AppointmentForm(),
        }
        return render(request, 'teacher_active_bookings.html', appointments )
    else:
        return redirect('/')



# ADD A PROCEDURE
def teacher_manage_courses(request):
    group_name=Group.objects.all().filter(user = request.user)# get logged user grouped name
    group_name=str(group_name[0]) # convert to string
    if "Teacher" == group_name:
        user_name=request.user.get_username()#Getting Username

        #Getting all Post and Filter By Logged UserName
        appointment_list = Appointment.objects.all().order_by("-id").filter(user=request.user)
        course_list = procedure.objects.all()
        #print(appointment_list)
        q=request.GET.get("q") #search start
        if q:
            appointment_list=appointment_list.filter(date__icontains=q)
        else:
            appointment_list = appointment_list #search end

        courses= {
            "query": appointment_list,
            "course":course_list,
            "user_name":user_name,
            "form":CourseForm(),
        }
        form = CourseForm(request.POST or None)
        if form.is_valid():
            saving=form.save(commit=False)
            saving.pk=None
            saving.save()
            messages.success(request, 'Added Succesfully')
        return render(request, 'teacher_manage_courses.html', courses)
    else:
        return redirect('/')



from django.db.models.functions import ExtractMonth, ExtractYear


from django.utils import timezone


def teacher_visualise(request):

    labels=[]
    data =[]
    months= []
    

    queryset_cb = Appointment.objects.all().order_by("-id").filter(user=request.user).exclude(appointment_with= '').count() # count currently booked
    queryset_ab = Appointment.objects.all().order_by("-id").filter(user=request.user, appointment_with= '').count() # active bookings
    queryset_total = queryset_cb+queryset_ab
    labels =['Current Bookings', 'Active Bookings', 'Total Bookings']
    data =[queryset_cb,queryset_ab,queryset_total]


    #ym = Appointment.objects.all().values_list(ExtractMonth("date"),ExtractYear("date")).distinct()
  
    #last 3 months booked solts <line chart>
    t = Appointment.objects.all().values_list("date", flat=True).distinct().order_by('-date').reverse()[:3]
    
    for a in t:
        months.append(a.strftime("%B"))
        
        
    from datetime import datetime, timedelta

    #current_month = datetime.now().month
    current = Appointment.objects.all().order_by("-id").filter(user=request.user, date__gte=timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)).exclude(appointment_with= '').count()
    
   
    last_month = datetime.today() - timedelta(days=30)
    last = Appointment.objects.all().order_by("-id").filter(user=request.user, date__range=[last_month, timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)]).exclude(appointment_with= '').count()


    past_month = datetime.today() - timedelta(days=60)
    past = Appointment.objects.all().order_by("-id").filter(user=request.user, date__range=[past_month, last_month]).exclude(appointment_with= '').count()
    
    
    cb_data= [past,last,current]


    current_vac = Appointment.objects.all().order_by("-id").filter(user=request.user, date__gte=timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0),appointment_with= '').count()
    
   
    last_vac = Appointment.objects.all().order_by("-id").filter(user=request.user, date__range=[last_month, timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)],appointment_with= '').count()


    past_vac = Appointment.objects.all().order_by("-id").filter(user=request.user, date__range=[past_month, last_month],appointment_with= '').count()


    vac_data = [past_vac,last_vac,current_vac]
    return render(request, 'teacher_visualise.html', {

        'labels':labels,
        'data':data,
        'month':months,
        'cb_data':cb_data,
        'vac_data':vac_data,
    })




def teacher_support(request):
    group_name=Group.objects.all().filter(user = request.user)# get logged user grouped name
    group_name=str(group_name[0]) # convert to string
    if "Teacher" == group_name and request.method=="POST":
        message_text= request.POST.get('message_textbox')
        if is_valid_filter_parameters(message_text):
            email_send=settings.EMAIL_HOST_USER,

            template = render_to_string('email_template_student_support.html',{'name':request.user.get_full_name(), 'email':request.user.email, 'message':message_text})
            email = EmailMessage(
            "Teacher Support Enquiry",
            template,
            settings.EMAIL_HOST_USER,
            [email_send],
            )
            email.fail_silently=True
            email.send()
            messages.success(request, 'Message Sent Sucessfully')
        else:
            messages.error(request, "Mesage box is empty")  
    return render(request, 'teacher_support.html')






def teacher_profile(request):
    group_name=Group.objects.all().filter(user = request.user)# get logged user grouped name
    group_name=str(group_name[0]) # convert to string
    if "Teacher" == group_name:
        user =request.user
        form =ProfileForm(instance=user)
        if request.method=='POST':
            form =ProfileForm(request.POST, request.FILES,instance=user)
            if form.is_valid():
                saving=form.save(commit=True)
                saving.save()
                messages.success(request, 'Profile updated succesfully')
        profile= {
            "form":form,
        }
        return render(request, 'teacher_edit_profile.html', profile)




def page_not_found_view(request, exception):
    return render(request, 'page-not-found.html', status=404)


def internal_server_error_view(request):
    return render(request, 'page-not-found-500.html')