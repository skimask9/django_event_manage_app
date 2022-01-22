from django.urls import path
from . import views

urlpatterns = [

    path('home', views.home, name="home"),
    path('showinfo', views.show_venue, name = "show-info"),
    path('create-pdf', views.pdf_report_create, name = 'create-pdf'),
    path('pdf_view/', views.ViewPDF.as_view(), name="pdf_view"),
    path('pdf_download/', views.DownloadPDF.as_view(), name="pdf_download"),
    path('liq-down', views.liq, name = "liq-down"),
    path('pdftest', views.pdftest, name ="pdf-test"),
    path('pdftest1', views.pdftest1, name ="pdf-test1"),

]