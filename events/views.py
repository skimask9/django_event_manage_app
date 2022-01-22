import re
from django.shortcuts import redirect, render
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from django.http import HttpResponseRedirect, response
from .models import Event,MyClubUser,Venue
from .forms import VenueForm,EventForm,EventFormAdmin
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required   
from django.http import HttpResponse
import csv
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.lib.pagesizes import landscape
from reportlab.platypus import Image
from django.core.paginator import Paginator



#<-------ALL EVENTS LIST--------->
def all_events(request):
    #event_list = Event.objects.all().order_by('-event_date')
    #event_list = Event.objects.all()
    p = Paginator(Event.objects.all(), 3)
    page = request.GET.get('page')
    events = p.get_page(page)
    return render (request, 'events/event_list.html',{
        #"event_list": event_list,
        'events' : events ,
    })

def all_events1(request,event_id):
    #event_list = Event.objects.all().order_by('-event_date')
    #event_list = Event.objects.all()
    event = Event.objects.get(pk=event_id)
    if request.method == "POST":
        event.delete()
        messages.success(request, ("Deleted Successfully!"))
        return HttpResponseRedirect(reverse('list-events'))
    else:
        return render (request, 'events/event_list.html', {
        'event': event
    })
 



#<-------ADD EVENT FORM---------->
@login_required
def add_event(request):
    #чтобы определять какой метод щас ПОСТ или ГЕТ , просто кто-то перешел на стр с формой
    # #или запостил форму                
    if request.method == "POST":
        if request.user.is_superuser:
            form = EventFormAdmin(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, ("Added Successfully!"))
                return HttpResponseRedirect(reverse('list-events'))
        else:
            form = EventForm(request.POST)
            if form.is_valid():
                #form.save()
                event = form.save(commit=False)
                event.manager = request.user
                event.save()
                messages.success(request, ("Added Successfully!"))
                return HttpResponseRedirect(reverse('list-events'))
    else:
        if request.user.is_superuser:

            form = EventFormAdmin()
        else:
            form = EventForm() 
    return render (request, 'events/add_event.html',{ 
        'form' : form 
    })



def venue_text(request,venue_id):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename = venue'+ ' ' + str(datetime.now())+'.docx'

    venues = Venue.objects.get(pk=venue_id)
    lines = []
    venue = (['Name - ',venues.name, '\nAddress - ', venues.address, '\nZip Code - ', venues.zip_code, '\nPhone - ' , venues.phone, '\nUrl Web - ', venues.web,'\nEmail - ' , venues.email_adress])
    for   venue1 in venue:
        lines.append(venue1)
    
    response.writelines(lines)   
    return response
    #lines = ["This is line 1\n",
    #"This is line 2\n",
    #"This is line 3\n"]


#def venue_pdf(request):
    #Create bytestream buffer

    buf = io.BytesIO()
    #Create a canvas
    c=canvas.Canvas(buf,  bottomup = 0)
    #Create a text object
    textob = c.beginText()
    c.setPageSize((595, 842))
    textob.setTextOrigin(inch,inch)
    textob.setFont("Helvetica-Bold", 9)
    logo = 'logo-social.png'

    #ADd some lines of text

    #lines = [
    #    "This is line 1", 
    #    "This is line 2", 
    #    "This is line 3",
    #    ]
   
    venues = Venue.objects.all()
    lines = []

    for venue in venues:
        lines.append(venue.name)
        lines.append(venue.address)
        lines.append(venue.zip_code)
        lines.append(venue.phone)
        lines.append(venue.web)
        lines.append(venue.email_adress)
        lines.append(" ================== ")
    #Loop 
    for line in lines:
        textob.textLine(line)

    c.setFont('Helvetica', 12, leading = None)
    c.drawCentredString(400,660, venue.phone + ':')

    #Finish
    c.drawImage(logo, 50, 700, width = 500, height = 120)
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    #Return
    return FileResponse(buf, as_attachment=True, filename='venue')

def venue_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename = venues' + ' ' + str(datetime.now())+'.csv'

    #Create a csv writer

    writer = csv.writer(response)

    venues = Venue.objects.all()

    # Add column headings to the csv file
    writer.writerow(['Venue Name','Address', 'Zip Code','Phone', 'Web', 'Web Address'])


    for venue in venues:
       writer.writerow([ venue.name ,venue.address, venue.zip_code, venue.phone,  venue.web, venue.email_adress ])

    return response 



def test(request):
    if request.method == 'POST':
        name = request.POST["name"]
        venue = Venue.objects.get(pk = request.POST ["venue"])
        description = request.POST["description"]
        form = Event.objects.create(name = name, event_date = timezone.now(), 
        venue = venue,   description = description )
        form.save()
        return HttpResponseRedirect(reverse('list-events'))
    return render(request, "events/test.html", { 
        'venues' : Venue.objects.all()
    })





#<-------UPDATE VENUE FORM---------->
@login_required
def update_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    form = VenueForm(request.POST or None, request.FILES or None, instance=venue)
    if form.is_valid():
        form.save()
        messages.success(request, ("Edited Successfully!"))
        return redirect('list-venues')
    return render (request, 'events/update_venue.html', {
        'venue': venue,
        'form' : form
    })


#<-------UPDATE EVENT FORM---------->
@login_required
def update_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    form = EventForm(request.POST or None, instance=event)
    if form.is_valid():
        form.save()
        messages.success(request, ("Edited Successfully!"))
        return redirect('list-events')  
    return render (request, 'events/update_event.html', {
        'event': event,
        'form' : form
    })


@login_required
def my_events(request):
    user = request.user.id
    events = Event.objects.filter(manager=user)
    return render (request, 'events/my_events.html',{
        'events': events
    })





#<-------ADD VENUE FORM---------->
@login_required
def add_venue(request):
    #чтобы определять какой метод щас ПОСТ или ГЕТ , просто кто-то перешел на стр с формой
    # #или запостил форму               
    if request.method == "POST":
        form = VenueForm(request.POST, request.FILES)
        if form.is_valid():
            venue = form.save(commit=False)
            venue.owner = request.user.id
            venue.save()
            messages.success(request, ("Added Successfully!"))
            #form.save()
            return HttpResponseRedirect(reverse('list-venues'))
    else:
        form = VenueForm() 
    return render (request, 'events/add_venue.html',{
        'form':form,
    })

#<-------ALL VENUES LIST--------->
def list_venues(request):
    venue_list = Venue.objects.all().order_by('name')
    return render (request , 'events/venue.html',{
        'venue_list' : venue_list,
    })

#def list_venues1(request,venue_id):    
    venue = Venue.objects.get(pk=venue_id)
    if request.method == "POST":
        venue.delete()
        messages.success(request, ("Deleted Successfully!"))
        return HttpResponseRedirect(reverse('list-venues'))
    else:
        return render(request,'events/venue.html',{
        "venue" : venue
    })


#<-------EACH VENUE DETAILED--------->
def show_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue_owner = User.objects.get(pk=venue.owner)
    return render (request, 'events/show_venue.html', {
        'venue': venue,
        'venue_owner': venue_owner
    })

#<-------DELETE AN EVENT--------->
#@login_required
#def delete_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.method == "POST":
        event.delete()
        messages.success(request, ("Deleted Successfully!"))
        return HttpResponseRedirect(reverse('list-events'))
    return render(request, 'events/delete_event.html', {
        'event': event
    })

#<-------DELETE VENUE-------->
@login_required
def delete_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    if request.method == "POST":
        venue.delete()
        messages.success(request, ("Deleted Successfully!"))
        return HttpResponseRedirect(reverse('list-venues'))
    return render(request,'events/delete_venue.html',{
        "venue" : venue
    })



#<-------SEARCH VENUE--------->
def search(request):
    if request.method == 'POST':    
        searched = request.POST['searched']
        venues = Venue.objects.filter(name__contains = searched)
        events = Event.objects.filter(name__contains = searched)
        return render(request, 'events/search.html',{
            'searched' : searched,
            'venues' : venues,
            'events' : events
            
        })
    else:
        return render (request,'events/search.html',{})




#<-------TESTING--------->
def home(request,year=datetime.now().year, month=datetime.now().strftime('%B')): 
    name = "John"
    month_number = list(calendar.month_name).index(month)
    cal = HTMLCalendar().formatmonth(year, month_number)
    now = datetime.now()
    current_year = now.year

    event_list = Event.objects.filter(event_date__year = year , event_date__month = month_number)

    time = now.strftime('%H:%M:%S')
    return render(request, 'events/home.html',{
        "first_name" : name,
        "year_dict" : year,
        "month_dict" : month,
        "month_number" : month_number,
        "cal": cal,
        "current_year" : current_year,
        "time" : time,
        "event_list" : event_list
    })