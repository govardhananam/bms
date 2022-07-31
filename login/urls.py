from teacher.models import Appointment, course, procedure, unit
from django.urls import path, include
from . import views
from django.contrib.auth.views import LoginView
#from django.contrib.auth.models import User
from django.urls import re_path as url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth import views as django_auth_views



from rest_framework import routers, serializers, viewsets
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.exceptions import ValidationError

User = get_user_model()

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'first_name', 'last_name','email','is_staff']

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer





class BookingSerializer(serializers.ModelSerializer):
      class Meta:
            model =Appointment
            fields =[ 'date', 'time_start', 'time_end', 'course', 'unit', 'procedure', 'appointment_with', 'address']

class BookingCreate(viewsets.ModelViewSet):
      queryset = Appointment.objects.all()
      serializer_class= BookingSerializer





class CourseSerializer(serializers.ModelSerializer):
      class Meta:
            model =course
            fields=['url', 'id', 'c_id', 'name']

class CourseCreate(viewsets.ModelViewSet):
      queryset = course.objects.all()
      serializer_class = CourseSerializer






class UnitSerializer(serializers.ModelSerializer):
      class Meta:
            model =unit
            fields=['url', 'id', 'name', 'u_id', 'course']

class UnitCreate(viewsets.ModelViewSet):
      queryset = unit.objects.all()
      serializer_class = UnitSerializer





class ProcedureSerializer(serializers.ModelSerializer):

      #course = CourseSerializer(many=True, read_only=True)
      #unit = UnitSerializer(many=True, read_only=True)
      class Meta:
            model =procedure
            fields=['url', 'id', 'name', 'course', 'unit']

class ProcedureCreate(viewsets.ModelViewSet):
      queryset = procedure.objects.all()
      serializer_class = ProcedureSerializer




# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'coursecreate',CourseCreate)
router.register(r'unitcreate',UnitCreate)
router.register(r'procedurecreate',ProcedureCreate)
router.register(r'bookingcreate',BookingCreate)


from .views import(

	group_check,
	logout_view,
	register_teacher,
	register_student,
      #login_view,
	)

urlpatterns = [

      path('api/', include(router.urls)),
      path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
      path('', LoginView.as_view(template_name='index.html'), name="home"),
      #path('', login_view, name='home'),
      path('logout/', views.logout_view, name='logout'),
      path('group/', views.group_check, name='group'),
      path('register_teacher/', views.register_teacher, name='register_teacher'),
      path('register_student/', views.register_student, name='register_student'),





       # Password reset links (ref: https://github.com/django/django/blob/master/django/contrib/auth/views.py)
      #path('password_change/done/', django_auth_views.PasswordChangeDoneView.as_view(template_name='password_reset/password_change_done.html'), 
        #name='password_change_done'),

      #path('password_change/', django_auth_views.PasswordChangeView.as_view(template_name='password_reset/password_change.html'), 
        #name='password_change'),

      path('password_reset/done/', django_auth_views.PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_done.html'),
            name='password_reset_done'),
      path('reset/<uidb64>/<token>/', django_auth_views.PasswordResetConfirmView.as_view(template_name='password_reset/password_change.html'), name='password_reset_confirm'),
      path('password_reset/', django_auth_views.PasswordResetView.as_view(template_name='password_reset/password_reset_form.html'), name='password_reset'),
      path('reset/done/', django_auth_views.PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_complete.html'),
      name='password_reset_complete'),    #email
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
