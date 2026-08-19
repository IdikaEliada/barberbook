from django.contrib import admin
from .models import Barber, Service, Appointment

admin.site.register(Barber)
admin.site.register(Service)
admin.site.register(Appointment)
