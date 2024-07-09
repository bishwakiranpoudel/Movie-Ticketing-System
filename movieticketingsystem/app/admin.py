from django.contrib import admin
from .models import Theatre, Admin, Customer, Movie, Show, Ticket
from django.contrib.admin import AdminSite

class MyAdminSite(AdminSite):
    site_header = 'Movie Ticketing System'
    site_title = 'Movie Ticketing Admin'
    index_title = 'Dashboard'

admin_site = MyAdminSite(name='myadmin')


class TicketInline(admin.TabularInline):
    model = Ticket
    extra = 0
    readonly_fields = ('seat_no', 'status', 'customer')

class ShowInline(admin.TabularInline):
    model = Show
    extra = 0

class TheatreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'location')
    inlines = [ShowInline]

class ShowAdmin(admin.ModelAdmin):
    list_display = ('id', 'movie', 'theatre', 'start_time', 'end_time', 'language')
    inlines = [TicketInline]

class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'director')
    inlines = [ShowInline]

class StatusListFilter(admin.SimpleListFilter):
    title = 'status'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return (
            ('booked', 'Booked'),
            ('not_booked', 'Not Booked'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'booked':
            return queryset.filter(status='booked')
        elif self.value() == 'not_booked':
            return queryset.filter(status='not_booked')
        return queryset

class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_theatre_name', 'get_show_start_time', 'get_movie_name', 'price', 'get_customer_id', 'status')
    list_filter = ('status', 'show', 'show__theatre')
    search_fields = ('customer__username', 'customer__cid')

    actions = ['mark_as_booked', 'verify_ticket_belongs_to_user']

    def mark_as_booked(self, request, queryset):
        queryset.update(status='booked')
        self.message_user(request, "Selected tickets marked as booked")
    mark_as_booked.short_description = "Mark selected tickets as booked"

    def verify_ticket_belongs_to_user(self, request, queryset):
        for ticket in queryset:
            if ticket.customer:
                self.message_user(request, f"Ticket {ticket.id} belongs to {ticket.customer.username}")
            else:
                self.message_user(request, f"Ticket {ticket.id} does not belong to any user")
    verify_ticket_belongs_to_user.short_description = "Verify if selected tickets belong to a user"

    def get_theatre_name(self, obj):
        return obj.show.theatre.name
    get_theatre_name.short_description = 'Theatre Name'

    def get_show_start_time(self, obj):
        return obj.show.start_time
    get_show_start_time.short_description = 'Start Time'

    def get_movie_name(self, obj):
        return obj.show.movie.title
    get_movie_name.short_description = 'Movie Name'

    def get_customer_id(self, obj):
        return obj.customer.cid if obj.customer else None
    get_customer_id.short_description = 'Customer ID'

admin.site.register(Ticket, TicketAdmin)

admin.site.register(Theatre, TheatreAdmin)
admin.site.register(Movie, MovieAdmin)
admin.site.register(Show, ShowAdmin)
admin.site.register(Customer)
admin.site.register(Admin)
