"""
Seed the database with sample movies, showtimes, bookings, and reviews
so that every feature of the portal is demonstrable out of the box.
"""
import os
import django
from datetime import date, time, timedelta
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from cinema.models import Movie, Showtime, SeatBooking, MovieReview

# ---------- Movies ----------
movies_data = [
    {
        'title': 'Galactic Odyssey',
        'genre': 'Sci-Fi',
        'duration': 148,
        'release_date': date(2026, 9, 15),
        'poster_url': 'https://images.unsplash.com/photo-1534996858221-380b92700493?w=400&h=600&fit=crop',
        'description': 'In the year 2187, humanity\'s last starship embarks on a perilous journey across uncharted galaxies to find a new home. Captain Aria Chen must navigate treacherous asteroid fields, encounter alien civilizations, and confront a mutiny that threatens to destroy the last hope for the human race.',
    },
    {
        'title': 'The Last Heist',
        'genre': 'Action',
        'duration': 126,
        'release_date': date(2026, 10, 1),
        'poster_url': 'https://images.unsplash.com/photo-1509347528160-9a9e33742cdb?w=400&h=600&fit=crop',
        'description': 'A retired master thief is pulled back into the underworld for one final job — stealing a priceless diamond from the most secure vault in Europe. With a team of eccentric specialists and a 72-hour deadline, every second counts in this pulse-pounding thriller.',
    },
    {
        'title': 'Whispers in the Dark',
        'genre': 'Horror',
        'duration': 108,
        'release_date': date(2026, 9, 28),
        'poster_url': 'https://images.unsplash.com/photo-1509281373149-e957c6296406?w=400&h=600&fit=crop',
        'description': 'When a family moves into a centuries-old mansion in rural England, they begin hearing whispers that seem to come from the walls themselves. As the sinister history of the house unravels, they realize that some doors were never meant to be opened.',
    },
    {
        'title': 'Love in Paris',
        'genre': 'Romance',
        'duration': 115,
        'release_date': date(2026, 10, 5),
        'poster_url': 'https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=400&h=600&fit=crop',
        'description': 'An aspiring writer from New York and a Parisian café owner find their worlds colliding during a magical autumn in the City of Lights. Through missed connections and serendipitous encounters along the Seine, they discover that love writes its own story.',
    },
    {
        'title': 'Code Zero',
        'genre': 'Thriller',
        'duration': 132,
        'release_date': date(2026, 9, 20),
        'poster_url': 'https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=400&h=600&fit=crop',
        'description': 'When a rogue AI gains control of the world\'s nuclear arsenal, cybersecurity expert Maya Park has just 12 hours to crack the most sophisticated code ever written. With governments in chaos and the clock ticking, she must outwit an intelligence that learns faster than any human.',
    },
    {
        'title': 'Laughing Matters',
        'genre': 'Comedy',
        'duration': 98,
        'release_date': date(2026, 10, 3),
        'poster_url': 'https://images.unsplash.com/photo-1485846234645-a62644f84728?w=400&h=600&fit=crop',
        'description': 'Three former college roommates reunite for a cross-country road trip that goes hilariously wrong. Between a stolen llama, a case of mistaken identity, and an accidental viral video, they rediscover the friendship that once made them inseparable.',
    },
]

print("Seeding movies...")
created_movies = []
for data in movies_data:
    movie, created = Movie.objects.get_or_create(
        title=data['title'],
        defaults=data,
    )
    created_movies.append(movie)
    status = "Created" if created else "Exists"
    print(f"  {status}: {movie.title}")

# ---------- Showtimes ----------
print("\nSeeding showtimes...")
today = date.today()
show_times = [time(10, 30), time(14, 0), time(18, 30), time(21, 0)]
prices = [Decimal('250.00'), Decimal('300.00'), Decimal('350.00'), Decimal('450.00')]

for movie in created_movies:
    for day_offset in range(5):  # Next 5 days
        show_date = today + timedelta(days=day_offset)
        for i, (st, price) in enumerate(zip(show_times, prices)):
            showtime, created = Showtime.objects.get_or_create(
                movie=movie,
                show_date=show_date,
                show_time=st,
                defaults={
                    'ticket_price': price,
                    'screen_number': (i % 3) + 1,
                },
            )
            if created:
                print(f"  Created: {showtime}")

# ---------- Sample Bookings ----------
print("\nSeeding sample bookings...")
first_showtime = Showtime.objects.first()
if first_showtime and not SeatBooking.objects.filter(showtime=first_showtime).exists():
    SeatBooking.objects.create(
        showtime=first_showtime,
        customer_name='John Demo',
        customer_email='john@example.com',
        customer_phone='555-0100',
        selected_seats='A1,A2,A3',
        total_paid=first_showtime.ticket_price * 3,
    )
    SeatBooking.objects.create(
        showtime=first_showtime,
        customer_name='Jane Sample',
        customer_email='jane@example.com',
        customer_phone='555-0200',
        selected_seats='C4,C5',
        total_paid=first_showtime.ticket_price * 2,
    )
    print("  Created sample bookings for first showtime.")

# ---------- Sample Reviews ----------
print("\nSeeding sample reviews...")
review_data = [
    ('Alice M.', 5, 'Absolutely phenomenal! The visual effects blew my mind and the story kept me on the edge of my seat.'),
    ('Bob T.', 4, 'Really entertaining. Great performances by the entire cast. Lost one star for the pacing in the middle act.'),
    ('Charlie R.', 3, 'Decent movie with some great moments, but the plot felt a bit predictable at times.'),
    ('Diana K.', 5, 'A masterpiece! Every frame is a work of art. Will definitely watch again.'),
    ('Eve S.', 4, 'Solid film with excellent direction. The soundtrack is incredible.'),
]

for movie in created_movies[:3]:
    for name, rating, comment in review_data:
        review, created = MovieReview.objects.get_or_create(
            movie=movie,
            reviewer_name=name,
            defaults={
                'rating': rating,
                'comment': comment,
            },
        )
        if created:
            print(f"  Created review by {name} for {movie.title}")

print("\nSeeding complete!")
