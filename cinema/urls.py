from django.urls import path
from . import views

app_name = 'cinema'

urlpatterns = [
    path('', views.movie_list, name='movie_list'),
    path('movie/<int:pk>/', views.movie_detail, name='movie_detail'),
    path('book/<int:showtime_id>/', views.book_seats, name='book_seats'),
    path('booking/<int:booking_id>/confirmation/', views.booking_confirmation, name='booking_confirmation'),
    path('movie/<int:movie_id>/review/', views.submit_review, name='submit_review'),
    path('api/booked-seats/<int:showtime_id>/', views.get_booked_seats, name='get_booked_seats'),
]
