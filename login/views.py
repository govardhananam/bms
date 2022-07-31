from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import Group
from django.views.generic import TemplateView
from django.views import generic
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404,HttpResponseNotFound
from django.shortcuts import render, get_object_or_404,redirect
from django.urls import path, reverse_lazy
from django.urls import re_path as url
from .forms import RegisterForm
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from django.contrib.auth import get_user_model
from teacher.models import course
from teacher.forms import GroupForm



User =get_user_model()


def group_check(request):
    user = request.user
    group_name = Group.objects.all().filter(user=request.user)  # get logged user grouped name
    form = GroupForm(instance=user)
    c = course.objects.all()
    group = Group.objects.all()
    if group_name.exists():
        group_name=str(group_name[0])# convert to string
        if "Student" == group_name:
            return redirect('/student/')
        elif "Teacher" == group_name:
            return redirect('/teacher/')
    else:
        if request.method == "POST":
            form = GroupForm(request.POST,instance=user)
            if form.is_valid():
                saving=form.save(commit=True)
                saving.save()
                messages.success(request, "Course and Category has been finalised")
                return redirect('/group/')
            else:
                messages.error(request, 'Error, Profile not Updated')
        profile = {
        "form": form,
        "course": c,
        "group": group,
        }
        return render(request, 'preference.html', profile)
    





def logout_view(request):
    logout(request)
    return redirect('home')



# to do: need to add forgot password, username and automated email confirmation
def register_teacher(request):
    user =request.user
    if user.is_authenticated:
        return HttpResponse(f"You are already authenticated as {user.email}.")
    if request.method =="POST":
        form= RegisterForm(request.POST)
        if form.is_valid():
            user=form.save()
            new_group = Group.objects.get(name = 'Teacher')
            user = User.objects.get(id=user.id)
            new_group.user_set.add(user)
            #user.groups.add(new_group)
            email =form.cleaned_data.get('email').lower()
            raw_password =form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            messages.success(request, "Registered Sucessfully")
            return redirect('home')
        else:
            messages.error(request, "Unsucessful registartion")
    else:
        form =RegisterForm()
    return render(request,"register_teacher.html", context={"register_form":form})




def register_student(request):
    user = request.user
    c = course.objects.all()
    #course.objects.all().delete()
    #django_groups = [group.name for group in user.groups.all()]
    #print(django_groups)
    if user.is_authenticated:
        return HttpResponse(f"You are already authenticated as {user.email}.")
    if request.method =="POST":
        form= RegisterForm(request.POST)
        if form.is_valid():
            user=form.save()
            new_group = Group.objects.get(name = 'Student')
            user = User.objects.get(id=user.id)
            new_group.user_set.add(user)
            email =form.cleaned_data.get('email').lower()
            raw_password =form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            messages.success(request, "Registered Sucessfully")
            return redirect('home')
        else:
            #return HttpResponse(form.errors.values())
            messages.error(request, "Unsucessful registartion")
    else:
        form =RegisterForm()        
    return render(request,"register_student.html", context={"form":form, "course":c})



'''

def login_view(request):
    user = request.user
    if user.is_authenticated:
        group_name=Group.objects.all().filter(user = request.user)# get logged user grouped name
        group_name=str(group_name[0]) # convert to string

        if "Student" == group_name:
            return redirect('/student/')
        elif "Teacher" == group_name:
            return redirect('/teacher/')
        elif "" == group_name:
            return HttpResponse("No group has been assigned to you")
    else:
        if request.method =="POST":
            form= LoginForm(request.POST)
            if form.is_valid():
                email = request.POST['email']
                password= request.POST['password']
                user = authenticate(email=email, password=password)
                login(request, user)
                group_name=Group.objects.all().filter(user = request.user)# get logged user grouped name
                group_name=str(group_name[0]) # convert to string
                if "Student" == group_name:
                    return redirect('/student/')
                elif "Teacher" == group_name:
                    return redirect('/teacher/')
                elif "" == group_name:
                    return HttpResponse("No group has been assigned to you")
                messages.success(request, "logged in")
            else:
                messages.error(request, "Unsucessful registartion")
        else:
            form =LoginForm()
    return render(request,"index.html", context={"form":form})
'''


