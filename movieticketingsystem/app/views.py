from django.shortcuts import redirect, render, get_object_or_404
from .models import Movie, Theatre, Show, Ticket
from .forms import CustomerLoginForm  # Import the CustomerLoginForm from your forms module

from .models import Customer

def book_ticket(request, movie_id, theatre_id, show_id, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    
    if ticket.status == 'not_booked':
        if request.method == 'POST':
            form = CustomerLoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                
                # Retrieve the customer based on the entered username
                customer = Customer.objects.filter(username=username).first()
                
                # Check if a customer with the provided username exists and if the password matches
                if customer and customer.password == password:
                    # Update ticket status to 'booked'
                    ticket.status = 'booked'
                    # Assign the ticket to the customer
                    ticket.customer = customer
                    ticket.save()
                    return redirect('show_detail', show_id=show_id, movie_id=movie_id, theatre_id=theatre_id)
                else:
                    return render(request, 'app/invalid_credentials.html')
        else:
            form = CustomerLoginForm()
        
        return render(request, 'app/book_ticket.html', {'form': form, 'ticket': ticket})
    else:
        return render(request, 'app/already_booked.html')

def movie_list(request):
    movies = Movie.objects.all()
    return render(request, 'app/movie_list.html', {'movies': movies})

def theatre_list(request, movie_id):
    # Retrieve the movie based on the movie_id
    movie = Movie.objects.get(pk=movie_id)

    # Retrieve all theatres for the given movie
    theatres = Theatre.objects.filter(show__movie=movie).distinct()

    # Create a dictionary to store shows for each theatre
    theatre_shows = {}
    for theatre in theatres:
        # Retrieve shows for each theatre
        shows = Show.objects.filter(movie=movie, theatre=theatre)
        theatre_shows[theatre] = shows

    return render(request, 'app/theatre_list.html', {'movie': movie, 'theatre_shows': theatre_shows})

def theatre_detail(request, theatre_id):
    theatre = Theatre.objects.get(id=theatre_id)
    return render(request, 'app/theatre_detail.html', {'theatre': theatre})

def show_detail(request, show_id, movie_id, theatre_id):
    show = get_object_or_404(Show, id=show_id)
    tickets = Ticket.objects.filter(show=show)
    movie = show.movie  # Get the movie associated with the show
    theatre = show.theatre  # Get the theatre associated with the show
    return render(request, 'app/show_detail.html', {'show': show, 'tickets': tickets, 'movie': movie, 'theatre': theatre})

def seat_booking(request, show_id):
    show = get_object_or_404(Show, pk=show_id)
    booked_seats = Ticket.objects.filter(show=show).values_list('seat_no', flat=True)
    total_seats = range(1, show.hall_capacity + 1)  # Assuming hall_capacity is a field in your Show model
    available_seats = [seat for seat in total_seats if seat not in booked_seats]
    return render(request, 'app/seat_booking.html', {'show': show, 'available_seats': available_seats})


def show_list(request, movie_id, theatre_id):
    # Get the movie based on the provided movie_id
    movie = Movie.objects.get(id=movie_id)
    
    # Get the shows for the selected movie and theatre
    shows = Show.objects.filter(movie=movie, theatre_id=theatre_id)
    
    return render(request, 'app/show_list.html', {'movie': movie, 'shows': shows})