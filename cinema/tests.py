from django.test import TestCase, Client
from django.urls import reverse
from decimal import Decimal
from datetime import date, time
from .models import Movie, Showtime, SeatBooking, MovieReview


class MoviePortalTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.movie = Movie.objects.create(
            title="Inception",
            genre="Sci-Fi",
            duration=148,
            release_date=date(2010, 7, 16),
            description="A mind-bending thriller.",
        )
        self.showtime = Showtime.objects.create(
            movie=self.movie,
            show_date=date.today(),
            show_time=time(18, 30),
            ticket_price=Decimal("250.00"),
            screen_number=1,
        )

    def test_movie_list_view(self):
        response = self.client.get(reverse('cinema:movie_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Inception")

    def test_movie_detail_view(self):
        response = self.client.get(reverse('cinema:movie_detail', kwargs={'pk': self.movie.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Inception")
        self.assertContains(response, "₹250.00")

    def test_book_seats_view_get(self):
        response = self.client.get(reverse('cinema:book_seats', kwargs={'showtime_id': self.showtime.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "₹250.00")
        self.assertContains(response, "booked-seats-data")

    def test_successful_booking_in_rupees(self):
        response = self.client.post(
            reverse('cinema:book_seats', kwargs={'showtime_id': self.showtime.pk}),
            {
                'customer_name': 'Rahul Sharma',
                'customer_email': 'rahul@example.com',
                'customer_phone': '9876543210',
                'selected_seats': 'A1,A2',
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        booking = SeatBooking.objects.get(customer_email='rahul@example.com')
        # 2 seats * 250.00 = 500.00
        self.assertEqual(booking.total_paid, Decimal("500.00"))
        self.assertContains(response, "₹500.00")

    def test_duplicate_seat_booking_rejected(self):
        SeatBooking.objects.create(
            showtime=self.showtime,
            customer_name='Existing User',
            customer_email='exist@example.com',
            selected_seats='B1,B2',
            total_paid=Decimal("500.00"),
        )
        # Attempt to book B1 again
        response = self.client.post(
            reverse('cinema:book_seats', kwargs={'showtime_id': self.showtime.pk}),
            {
                'customer_name': 'New User',
                'customer_email': 'new@example.com',
                'selected_seats': 'B1,B3',
            },
        )
        self.assertEqual(response.status_code, 200)
        # Form error should indicate seat is already booked
        self.assertContains(response, "already booked")
        self.assertFalse(SeatBooking.objects.filter(customer_email='new@example.com').exists())

    def test_submit_review(self):
        response = self.client.post(
            reverse('cinema:submit_review', kwargs={'movie_id': self.movie.pk}),
            {
                'reviewer_name': 'Amit Patel',
                'rating': 5,
                'comment': 'Masterpiece cinema experience!',
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        review = MovieReview.objects.get(reviewer_name='Amit Patel')
        self.assertEqual(review.rating, 5)
        self.assertEqual(self.movie.average_rating(), 5.0)
