from django.shortcuts import render
from django.shortcuts import redirect, render
import calendar
from calendar import HTMLCalendar
from events.models import Event,MyClubUser,Venue
from django.http import HttpResponse, request
from django.http import FileResponse
from django.template.loader import get_template
from io import BytesIO
from xhtml2pdf import pisa
from django.views import View
from requests_html import HTMLSession
import csv
from datetime import datetime
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
from django.db.models import Sum


# Create your views here.


def liq(request):
    response = HttpResponse(content_type='text/csv')
    response ['Content-Disposition'] = 'attachment; filename = liq'  + ' ' + str(datetime.now())+'.csv'
    
    session = HTMLSession()

    url = 'https://liquipedia.net/dota2/Liquipedia:Upcoming_and_ongoing_matches'

    response1 = session.get(url)

    container = response1.html.find('#main-content-column', first = True)

    list1 = container.find('table')

    sheet = [['Team left' , 'vs', 'BO' , 'Team right', 'date/torn','the']]
    for item in list1:
        elements = item.text.split('\n')
        left = elements[0]
        vs = elements [1]
        bo = elements[2]
        right = elements [3]
        date = elements [4]   
        sheet.append([left, vs, bo, right, date])  
    
    writer = csv.writer(response)
    writer.writerows(sheet)
    return response


def pdftest(request):
    response = HttpResponse(content_type='application/pdf')
    response ['Content-Disposition'] = 'inline;attachment; filename = venues'  + ' ' + str(datetime.now())+'.pdf'

    response['Content-Transfer-Encoding'] = 'binary'

    venues = Venue.objects.all()

    sum = venues.aggregate(Sum('id'))
    
    html_string = render_to_string('pdf_convert/pdf-output.html', {'venues':venues, 'total': sum ['id__sum'] })

    html = HTML (string=html_string)

    result = html.write_pdf()

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)


        
        response.write(output.read())

    return response


def pdftest1(request):
    response = HttpResponse(content_type='application/pdf')
    response ['Content-Disposition'] = 'inline;attachment; filename = events'  + ' ' + str(datetime.now())+'.pdf'

    response['Content-Transfer-Encoding'] = 'binary'

    events = Event.objects.all()

    sum = events.aggregate(Sum('id'))
    
    html_string = render_to_string('pdf_convert/pdf-output2.html', {'events':events, 'total': sum ['id__sum'] })

    html = HTML (string=html_string)

    result = html.write_pdf()

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)


        
        response.write(output.read())

    return response

def home(request):
    cal = HTMLCalendar().formatmonth(theyear=2022, themonth=1)
    return render(request, 'pdf_convert/home.html',{
        'cal' : cal
    })

def show_venue(request):
    venues = Venue.objects.all()

    return render(request, 'pdf_convert/showinfo.html',{
        'venues':venues
    })


def pdf_report_create(request):
    venues = Venue.objects.all()
    template_path = 'pdf_convert/pdfReport.html'
    context = {'venues': venues}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="venues'  + ' ' + str(datetime.now())+'.pdf' #we can use atachment; to actually download 
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response



def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


data = {
    "company": "Dennnis Ivanov Company",
    "address": "123 Street name",
    "city": "Vancouver",
    "state": "WA",
    "zipcode": "98663",


    "phone": "555-555-2345",
    "email": "youremail@dennisivy.com",
    "website": "dennisivy.com",
    }

#Opens up page as PDF
class ViewPDF(View):
    def get(self, request, *args, **kwargs):

        pdf = render_to_pdf('pdf_convert/pdftemplate.html', data)
        return HttpResponse(pdf, content_type='application/pdf')


#Automaticly downloads to PDF file
class DownloadPDF(View):
    def get(self, request, *args, **kwargs):
        
        pdf = render_to_pdf('pdf_convert/pdftemplate.html', data)

        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Venue_%s.pdf" %("12341231")
        content = "attachment; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response