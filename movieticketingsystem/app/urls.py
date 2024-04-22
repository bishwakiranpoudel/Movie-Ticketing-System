from django.urls import path
from . import views

urlpatterns = [
    path('theatres/', views.theatre_list, name='theatre_list'),
    path('theatres/<int:theatre_id>/', views.theatre_detail, name='theatre_detail'),
    # Add more URL patterns for other views

    path('', views.movie_list, name='movie_list'),
    path('movies/<int:movie_id>/theatres/', views.theatre_list, name='theatre_list'),
    path('movies/<int:movie_id>/theatres/<int:theatre_id>/shows/<int:show_id>/', views.show_detail, name='show_detail'),
    path('shows/<int:show_id>/book/', views.seat_booking, name='seat_booking'),
    path('movies/<int:movie_id>/theatres/<int:theatre_id>/shows/', views.show_list, name='show_list'),
     path('movies/<int:movie_id>/theatres/<int:theatre_id>/shows/<int:show_id>/book/', views.book_ticket, name='book_ticket'),
    # Add more URL patterns for other views
    ]