from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Movie(models.Model):
    """Represents a movie in the cinema catalog."""
    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=100)
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    release_date = models.DateField()
    poster_url = models.URLField(max_length=500, blank=True)
    description = models.TextField()

    class Meta:
        ordering = ['-release_date']

    def __str__(self):
        return self.title

    def average_rating(self):
        """Calculate the average rating from all reviews."""
        reviews = self.reviews.all()
        if reviews.exists():
            return round(reviews.aggregate(models.Avg('rating'))['rating__avg'], 1)
        return 0

    def review_count(self):
        """Return the total number of reviews."""
        return self.reviews.count()


class Showtime(models.Model):
    """Represents a specific showing of a movie."""
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='showtimes')
    show_date = models.DateField()
    show_time = models.TimeField()
    ticket_price = models.DecimalField(max_digits=8, decimal_places=2)
    screen_number = models.PositiveIntegerField()

    class Meta:
        ordering = ['show_date', 'show_time']

    def __str__(self):
        return f"{self.movie.title} - {self.show_date} {self.show_time} (Screen {self.screen_number})"

    def booked_seats(self):
        """Return a list of all seats booked for this showtime."""
        bookings = self.bookings.all()
        seats = []
        for booking in bookings:
            seats.extend(booking.get_seat_list())
        return seats


class SeatBooking(models.Model):
    """Represents a booking of one or more seats for a showtime."""
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE, related_name='bookings')
    customer_name = models.CharField(max_length=200)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20, blank=True)
    selected_seats = models.CharField(max_length=500, help_text="Comma-separated seat IDs, e.g. A1,A2,B3")
    total_paid = models.DecimalField(max_digits=10, decimal_places=2)
    booked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-booked_at']

    def __str__(self):
        return f"{self.customer_name} - {self.showtime} ({self.selected_seats})"

    def get_seat_list(self):
        """Return a list of individual seat IDs."""
        return [s.strip() for s in self.selected_seats.split(',') if s.strip()]


class MovieReview(models.Model):
    """Represents a user review/rating for a movie."""
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    reviewer_name = models.CharField(max_length=200)
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return f"{self.reviewer_name} - {self.movie.title} ({self.rating}/5)"
