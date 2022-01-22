from django.db import models
from django.db.models.fields import DateTimeField
from django.contrib.auth.models import User
from django.forms.widgets import Select

class Venue (models.Model): 
    name = models.CharField('Venue Name', max_length=55)
    address = models.CharField( max_length=300)
    zip_code = models.CharField('Zip Code', max_length=15)
    phone = models.IntegerField('Contact Phone')
    web = models.URLField('Website adress', blank = True)
    email_adress = models.EmailField('Email Adress', blank = True)
    owner = models.IntegerField('Venue Owner', blank=False, default=1)
    venue_image = models.ImageField(" Venue Image", null = True, blank = True, upload_to ="images/")
    def __str__(self):
         return self.name


class MyClubUser(models.Model):
    first_name= models.CharField( max_length=30)
    last_name= models.CharField( max_length=30) 
    email = models.EmailField('User Email')

    def __str__(self):
         return self.first_name + ' ' + self.last_name

class Event (models.Model):
     name = models.CharField('Event Name', max_length=55)
     event_date = models.DateTimeField('Event Date')
     venue = models.ForeignKey(Venue,  blank=True, null=True, on_delete=models.CASCADE)
     manager = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
     description = models.TextField(blank=True)
     attendess = models.ManyToManyField(MyClubUser, blank=True)

     def __str__(self):
         return self.name