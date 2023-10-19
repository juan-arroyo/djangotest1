from django.urls import path
from . import views


urlpatterns = [
    # Path Converters
    # int : number
    # str : strings
    # path : whole urls /
    # slug : hyphen-and_underscores_stuff
    # UUID : universally unique identifier

    path('', views.home, name='home'),
    path('<int:year>/<str:month>/', views.home, name='home'),
    path('events', views.all_events, name='list-events'),

    # VENUES URL
    path('list_venues', views.list_venues, name='list-venues'),
    path('show_venue/<venue_id>/', views.show_venue, name='show-venue'),
    path('search_venues', views.search_venues, name='search-venues'),
    path('add_venue', views.add_venue, name='add-venue'),
    path('update_venue/<venue_id>/', views.update_venue, name='update-venue'),
    path('delete_venue/<venue_id>/', views.delete_venue, name='delete-venue'),

    # EVENTS URL
    path('add_event', views.add_event, name='add-event'),
    path('update_event/<event_id>/', views.update_event, name='update-event'),
    path('delete_event/<event_id>/', views.delete_event, name='delete-event'),
    path('my_events', views.my_events, name='my-events'),

    # DOWNLOAD TEXT, CSV AND PDF URL
    path('venue_text', views.venue_text, name='venue-text'),
    path('venue_csv', views.venue_csv, name='venue-csv'),
    path('venue_pdf', views.venue_pdf, name='venue-pdf'),
]
