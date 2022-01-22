from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import Venue, Event 
from datetime import date
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import   DateInput
from django.forms.widgets import DateInput


#Create a venue form

class VenueForm(ModelForm):
    class Meta: #always use it (idk)
        model = Venue
        fields = ('name', 'address', 'zip_code', 'phone', 'web', 'email_adress','venue_image') #but we can use "__all__" или опред. как тут
        labels = {
            'name': '' ,
            'address': '',
            'zip_code': '',
            'phone': '',
            'web': '',
            'email_adress': '',
            'venue_image': '',
        }

        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control', 'placeholder' : 'Venue Name'}),
            'address': forms.TextInput(attrs={'class':'form-control','placeholder' : 'Address'}),
            'zip_code': forms.TextInput(attrs={'class':'form-control','placeholder' : 'Zip Code'}),
            'phone': forms.TextInput(attrs={'class':'form-control','placeholder' : 'Phone'}),
            'web': forms.TextInput(attrs={'class':'form-control','placeholder' : 'Web'}),
            'email_adress': forms.EmailInput(attrs={'class':'form-control','placeholder' : 'Email'}),
            'venue_image': forms.ClearableFileInput(attrs={'class':'form-control','placeholder' : 'Image'}),       
        }

class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'

#ADMIN EVENTFORM
class EventFormAdmin(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.fields['venue'].empty_label = "Select"
        self.fields['manager'].empty_label = "Select"

    error_css_class = 'error-field'
    required_css_class = 'required_field'

    class Meta:
        model = Event
        fields = ('name', 'event_date', 'venue', 'manager','description')
        labels = {
            'name': '' ,
            'event_date': '',   
            'venue': '',
            'manager': '',
            'description': '',
        }
        
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control', 'placeholder' : 'Event Name'}),
            'event_date': DateTimeInput(attrs={'class':'form-control'}),       
            'venue': forms.Select(attrs={'type':'select', 'class':'form-select'}),   
            'manager': forms.Select(attrs={'type':'select','class':'form-select'}),
            'description': forms.Textarea(attrs={'class':'form-control','placeholder' : 'Description', 'style': "height: 200px"}),
        }
       
    def clean_venue(self):
        venue = self.cleaned_data['venue']
        if venue == None :
            raise ValidationError ("Select Venue!")
        return venue

    def clean_manager(self):
        manager = self.cleaned_data['manager']
        if manager == None :
            raise ValidationError ("Select Manager!")
        return manager




#Regular EVENTFORM
class EventForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.fields['venue'].empty_label = "Select"

    error_css_class = 'error-field'
    required_css_class = 'required_field'

    class Meta:
        model = Event
        fields = ('name', 'event_date', 'venue', 'description')
        labels = {
            'name': '' ,
            'event_date': '',   
            'venue': '',
            'description': '',
        }
        
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control', 'placeholder' : 'Event Name'}),
            'event_date': DateTimeInput(attrs={'class':'form-control'}),       
            'venue': forms.Select(attrs={'type':'select', 'class':'form-select'}),   
            'description': forms.Textarea(attrs={'class':'form-control','placeholder' : 'Description', 'style': "height: 200px"}),
        }
       
    def clean_venue(self):
        venue = self.cleaned_data['venue']
        if venue == None :
            raise ValidationError ("Select Venue!")
        return venue



class UserRegistrationForm(UserCreationForm):
    
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'type' : 'username',
        'placeholder' : 'enter username'
    }))
    email = forms.CharField(widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'type' : 'email',
        'placeholder' : 'email@example.com',
        
    }))
    password1 = forms.CharField(widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'type' : 'password',
        'placeholder' : 'enter password',
    }),label="Password")
    password2 = forms.CharField(widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'type' : 'password',
        'placeholder' : 'password confirmation '
    }),label="Confirm")

