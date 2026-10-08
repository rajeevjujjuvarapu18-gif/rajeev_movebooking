from django.contrib import admin
from .models import Movie, Showtime, SeatBooking, MovieReview


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'duration', 'release_date')
    list_filter = ('genre', 'release_date')
    search_fields = ('title', 'genre', 'description')


@admin.register(Showtime)
class ShowtimeAdmin(admin.ModelAdmin):
    list_display = ('movie', 'show_date', 'show_time', 'ticket_price', 'screen_number')
    list_filter = ('show_date', 'screen_number', 'movie')
    search_fields = ('movie__title',)


@admin.register(SeatBooking)
class SeatBookingAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'showtime', 'selected_seats', 'total_paid', 'booked_at')
    list_filter = ('booked_at', 'showtime__movie')
    search_fields = ('customer_name', 'customer_email')


@admin.register(MovieReview)
class MovieReviewAdmin(admin.ModelAdmin):
    list_display = ('reviewer_name', 'movie', 'rating', 'created_date')
    list_filter = ('rating', 'created_date', 'movie')
    search_fields = ('reviewer_name', 'comment')
