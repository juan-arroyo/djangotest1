from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.http import FileResponse
from django.core.paginator import Paginator
from django.contrib import messages

import calendar
from calendar import HTMLCalendar
from datetime import datetime
import csv
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

from . models import Event, Venue
from django.contrib.auth.models import User
from . forms import VenueForm, EventForm, EventFormAdmin


# GENERATE PDF FILE VENUE LIST
def venue_pdf(request):
    # Create a Bytestream buffer
    buf = io.BytesIO()
    # Create a canvas
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    # Create a text object
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont('Helvetica', 14)

    # Designate The Model
    venues = Venue.objects.all()

    # Create blank list
    lines = []

    for venue in venues:
        lines.append(venue.name)
        lines.append(venue.address)
        lines.append(venue.zip_code)
        lines.append(venue.phone)
        lines.append(venue.web)
        lines.append(venue.email_address)
        lines.append("=========================")

    # Loop
    for line in lines:
        textob.textLine(line)
    

    # Finish Up
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename='venue.pdf')


# GENERATE TEXT FILE VENUE LIST
def venue_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=venues.csv'

    # Create a csv writer
    writer = csv.writer(response)

    # Designate The Model
    venues = Venue.objects.all()

    # Add column headings to the csv file
    writer.writerow(['Venue Name', 'Address', 'Zip Code', 'Phone', 'Web Address', 'Email'])


    # Loop Thu and output
    for venue in venues:
        writer.writerow([venue.name, venue.address, venue.zip_code, venue.phone, venue.web, venue.email_address])

    # Write To CsvFile
    return response


# GENERATE TEXT FILE VENUE LIST
def venue_text(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=venues.txt'

    # Designate The Model
    venues = Venue.objects.all()

    # Create blank list
    lines = []

    # Loop Thu and output
    for venue in venues:
        lines.append(f'{venue.name}\n{venue.address}\n{venue.zip_code}\n{venue.phone}\n{venue.web}\n{venue.email_address}\n\n\n')

    # Write To TextFile
    response.writelines(lines)
    return response

#############################################################################
#############################################################################
#############################################################################

##### MY EVENT PAGE #####
def my_events(request):
    if request.user.is_authenticated:
        me = request.user.id
        events = Event.objects.filter(manager=me)
        context = {'events':events}
        return render(request, 'events/my_events.html', context)
    else:
        messages.success(request, "You aren't Authorized to View This Page !!! ")
        return redirect('home')


##### DELETE EVENT #####
def delete_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.user == event.manager:
        event.delete()
        messages.success(request, 'Event Deleted!!')
        return redirect('list-events')
    else:
        messages.success(request, "You aren't Authorized to delete This Event! ")
        return redirect('list-events')


##### UPDATE EVENT #####
def update_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.user.is_superuser:
        form = EventFormAdmin(request.POST or None, instance=event)
    else:
        form = EventForm(request.POST or None, instance=event)
    if form.is_valid():
        form.save()
        return redirect('list-events')

    context = {'event':event, 'form':form}
    return render(request, 'events/update_event.html', context)


##### ADD EVENT #####
def add_event(request):
    submitted = False
    # form = EventForm()

    if request.method == 'POST':
        if request.user.is_superuser:
            form = EventFormAdmin(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/add_event?submitted=True')
        else:
            form = EventForm(request.POST)
            if form.is_valid():
                event = form.save(commit=False)
                event.manager = request.user # logged in user (el owner viene de models)
                event.save()
                return HttpResponseRedirect('/add_event?submitted=True')
    else:
        # Just Going To The Page, Not Submitting
        if request.user.is_superuser:
            form = EventFormAdmin()
        else:
            form = EventForm()

        if 'submitted' in request.GET:
            submitted = True


    context = {'form':form, 'submitted':submitted}
    return render(request, 'events/add_event.html', context)


##### SHOW ALL EVENTS #####
def all_events(request):
    event_list = Event.objects.all().order_by('event_date')

    context = {'event_list':event_list}
    return render(request, 'events/event_list.html', context)

#############################################################################
#############################################################################
#############################################################################

##### DELETE VENUE #####
def delete_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue.delete()
    return redirect('list-venues')


##### UPDATE VENUE #####
def update_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    form = VenueForm(request.POST or None, instance=venue)
    if form.is_valid():
        form.save()
        return redirect('list-venues')

    context = {'venue':venue, 'form':form}
    return render(request, 'events/update_venue.html', context)


##### SEARCH VENUES #####
def search_venues(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        # El name viene de la tabla de la db Venue
        venues = Venue.objects.filter(name__contains=searched)

        context = {'searched':searched, 'venues':venues}
        return render(request, 'events/search_venue.html', context)
    else:
        context = {}
        return render(request, 'events/search_venue.html', context)
        

##### SHOW VENUE #####
def show_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    #Asigamos un owner a los venue
    venue_owner = User.objects.get(pk=venue.owner)

    context = {'venue':venue, 'venue_owner':venue_owner}
    return render(request, 'events/show_venue.html', context)


##### LIST VENUE #####
def list_venues(request):
    venue_list = Venue.objects.all()

    # Set up Pagination
    p  = Paginator(Venue.objects.all(), 4)
    page = request.GET.get('page')
    venues = p.get_page(page)
    nums = "a" * venues.paginator.num_pages

    context = {'venue_list':venue_list, 'venues':venues, 'nums':nums}
    return render(request, 'events/venue_list.html', context)


##### ADD VENUE #####
def add_venue(request):
    submitted = False
    form = VenueForm()

    if request.method == 'POST':
        form = VenueForm(request.POST)
        if form.is_valid():
            # form.save()
            venue = form.save(commit=False)
            venue.owner = request.user.id # logged in user (el owner viene de models)
            venue.save()
            return HttpResponseRedirect('/add_venue?submitted=True')
    else:
        if 'submitted' in request.GET:
            submitted = True


    context = {'form':form, 'submitted':submitted}
    return render(request, 'events/add_venue.html', context)


##### HOME #####
def home(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
    name = 'John'

    # Convertimos primera letra a mayuscula
    month = month.capitalize()

    # Convert month from name to number
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)

    # Create calendar
    cal = HTMLCalendar().formatmonth(year, month_number)

    # Get current year
    now = datetime.now()
    current_year = now.year

    # Get current time
    time = now.strftime('%H:%M %p')

    context = {'first_name': name, 'year': year,
               'month': month, 'month_number': month_number, 'cal': cal, 'current_year': current_year, 'time': time}
    return render(request, 'events/home.html', context)
