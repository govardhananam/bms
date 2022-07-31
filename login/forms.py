from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserCreationForm


User= get_user_model()


class RegisterForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    email = forms.EmailField(max_length=254)

    #zoom_id = forms.CharField(max_length=100, help_text='Zoom ID')

    class Meta:
        model = User
        fields = ["first_name","last_name", "email", "password1", "password2", "course" ]

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(f"Email {email} is already in use.")

        #raise forms.ValidationError('Email "%s" is already in use.' % user)

    
    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

'''
class LoginForm(forms.ModelForm):

    password =forms.CharField(label="password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields= ("email", "password")
    
    def clean(self):
        if self.is_valid():
            email= self.cleaned_data['email']
            password =self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("invalid Login")
    '''
