from django.urls import path,include
from . import views




urlpatterns = [
    #Path Converters
    # int: nubmers
    #str : strings
    #path : whole urls /
    #slug: hyphen-and_underscores_stuff
    #UUID: universally unique identifier
    path('', views.home, name="home1"),
    path('<int:year>/<str:month>', views.home, name="home"),
    path('events', views.all_events, name = "list-events"),
    path('events/<event_id>', views.all_events1, name = "list-events"),
    path('add_venue', views.add_venue, name = 'add-venue'),
    path('list_venues', views.list_venues, name = 'list-venues'),
    #path('list_venues/<venue_id>', views.list_venues1, name = 'list-venues'),
    path('show_venue/<venue_id>', views.show_venue, name='show-venue'),
    path('search', views.search, name = 'search'),
    path('update_venue/<venue_id>', views.update_venue, name='update-venue'),
    path('add_event', views.add_event, name = 'add-event'),
    path('update_event/<event_id>', views.update_event, name='update-event'),
    path('test', views.test, name = 'test'),
    #path('delete_event/<event_id>', views.delete_event, name = 'delete-event'),
    path('delete_venue/<venue_id>', views.delete_venue, name = 'delete-venue'),
    path('venue_text/<venue_id>', views.venue_text, name='venue-text'),
    path('venue_csv', views.venue_csv, name='venue-csv'),
    path('my_events', views.my_events, name='my-events'),
    path('__debug__/', include('debug_toolbar.urls')),
    #path('venue_pdf', views.venue_pdf, name='venue-pdf'),
]