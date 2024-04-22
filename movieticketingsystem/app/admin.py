from django.contrib import admin
from .models import Theatre, Admin, Customer, Movie, Show, Ticket

admin.site.register(Theatre)
admin.site.register(Admin)
admin.site.register(Customer)
admin.site.register(Movie)
admin.site.register(Show)
admin.site.register(Ticket)