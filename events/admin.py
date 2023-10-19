from django.contrib import admin
from . models import Event
from . models import MyClubUser
from . models import Venue


# @admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display  = ('name', 'address', 'phone')
    ordering = ('name',)
    search_fields = ('name', 'address')


class EventAdmin(admin.ModelAdmin):
    fields = (('name', 'venue'), 'event_date', 'description', 'manager')
    list_display = ('name', 'event_date', 'venue')
    list_filter = ('event_date', 'venue')
    ordering = ('event_date',)


admin.site.register(Venue, VenueAdmin)
admin.site.register(MyClubUser)
admin.site.register(Event, EventAdmin)