import json
from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Avg
from .models import Movie, Showtime, SeatBooking, MovieReview
from .forms import SeatBookingForm, MovieReviewForm


def movie_list(request):
    """Display all movies with genre filtering and average ratings."""
    genre_filter = request.GET.get('genre', '')
    movies = Movie.objects.all()

    # Get distinct genres for the filter
    genres = Movie.objects.values_list('genre', flat=True).distinct().order_by('genre')

    if genre_filter:
        movies = movies.filter(genre=genre_filter)

    # Annotate with average rating
    movies = movies.annotate(avg_rating=Avg('reviews__rating'))

    context = {
        'movies': movies,
        'genres': genres,
        'selected_genre': genre_filter,
    }
    return render(request, 'cinema/movie_list.html', context)


def movie_detail(request, pk):
    """Display movie details with showtimes and reviews."""
    movie = get_object_or_404(Movie, pk=pk)
    showtimes = movie.showtimes.all()
    reviews = movie.reviews.all()
    review_form = MovieReviewForm()

    context = {
        'movie': movie,
        'showtimes': showtimes,
        'reviews': reviews,
        'review_form': review_form,
        'avg_rating': movie.average_rating(),
        'review_count': movie.review_count(),
    }
    return render(request, 'cinema/movie_detail.html', context)


def book_seats(request, showtime_id):
    """Display seat selection grid and handle booking."""
    showtime = get_object_or_404(Showtime, pk=showtime_id)
    booked_seats = showtime.booked_seats()

    if request.method == 'POST':
        form = SeatBookingForm(request.POST, showtime=showtime)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.showtime = showtime

            # Server-side price calculation
            seat_count = len(booking.get_seat_list())
            booking.total_paid = showtime.ticket_price * seat_count

            booking.save()
            messages.success(request, 'Booking confirmed! Enjoy the movie!')
            return redirect('cinema:booking_confirmation', booking_id=booking.pk)
        else:
            messages.error(request, 'Booking failed. Please check the errors below.')
    else:
        form = SeatBookingForm(showtime=showtime)

    context = {
        'showtime': showtime,
        'movie': showtime.movie,
        'form': form,
        'booked_seats': booked_seats,
        'ticket_price': float(showtime.ticket_price),
    }
    return render(request, 'cinema/book_seats.html', context)


def booking_confirmation(request, booking_id):
    """Display booking confirmation details."""
    booking = get_object_or_404(SeatBooking, pk=booking_id)
    context = {
        'booking': booking,
        'movie': booking.showtime.movie,
        'showtime': booking.showtime,
    }
    return render(request, 'cinema/booking_confirmation.html', context)


def submit_review(request, movie_id):
    """Handle movie review submission."""
    movie = get_object_or_404(Movie, pk=movie_id)

    if request.method == 'POST':
        form = MovieReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie = movie
            review.save()
            messages.success(request, 'Thank you for your review!')
            return redirect('cinema:movie_detail', pk=movie.pk)
        else:
            messages.error(request, 'Please fix the errors in your review.')
            # Re-render the movie detail page with errors
            showtimes = movie.showtimes.all()
            reviews = movie.reviews.all()
            context = {
                'movie': movie,
                'showtimes': showtimes,
                'reviews': reviews,
                'review_form': form,
                'avg_rating': movie.average_rating(),
                'review_count': movie.review_count(),
            }
            return render(request, 'cinema/movie_detail.html', context)

    return redirect('cinema:movie_detail', pk=movie.pk)


def get_booked_seats(request, showtime_id):
    """API endpoint to get booked seats for a showtime."""
    showtime = get_object_or_404(Showtime, pk=showtime_id)
    return JsonResponse({'booked_seats': showtime.booked_seats()})
