from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder' : 'Email'}))
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control','placeholder' : 'First Name'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control','placeholder' : 'Last Name'}))
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control','placeholder' : 'Username'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder' : 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder' : 'Password Confirmation'}))


    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email','password1', 'password2')  
        labels = {
            'username': '' ,
            'first_name': '',
            'last_name': '',
            'email': '',
            'password1': '',
            'password2': '',
        }