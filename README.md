# 🎬 CineVerse — Movie Booking & Review Portal

A full-featured cinema ticketing web application built with Python 3.11+, Django 6.x, SQLite, and Bootstrap 5.

---

## 📁 Project Structure

```
mysite/
│
├── cinema/                      # Main Cinema Application
│   ├── migrations/              # Database schema migrations
│   │   ├── 0001_initial.py
│   │   └── __init__.py
│   ├── static/                  # App static assets
│   │   ├── css/
│   │   │   └── style.css        # Glassmorphism dark cinema theme
│   │   └── js/
│   │       ├── main.js          # Particle background & toast alerts
│   │       ├── seats.js         # 5×8 interactive seat grid & ₹ calculation
│   │       └── reviews.js       # Dynamic 1–5 star rating widget
│   ├── templates/cinema/        # Semantic HTML5 templates
│   │   ├── base.html            # Core layout with Bootstrap 5
│   │   ├── movie_list.html      # Hero banner, catalog & genre filters
│   │   ├── movie_detail.html    # Movie synopsis, showtimes in ₹ & reviews
│   │   ├── book_seats.html      # Interactive seat matrix & checkout
│   │   └── booking_confirmation.html # Booking ticket receipt
│   ├── admin.py                 # Django admin models registration
│   ├── apps.py                  # App configuration
│   ├── forms.py                 # SeatBookingForm & MovieReviewForm
│   ├── models.py                # Movie, Showtime, SeatBooking, MovieReview
│   ├── tests.py                 # Unit & integration test suite (6 passing)
│   ├── urls.py                  # Cinema route definitions
│   ├── views.py                 # Views & controller logic
│   └── __init__.py
│
├── mysite/                      # Django Project Configuration
│   ├── asgi.py                  # ASGI entrypoint
│   ├── settings.py              # Settings (WhiteNoise, Render hosts, SQLite)
│   ├── urls.py                  # Root URL routing
│   ├── wsgi.py                  # WSGI entrypoint for Gunicorn
│   └── __init__.py
│
├── .env.example                 # Example environment variables
├── .gitignore                   # Ignored files (pycache, staticfiles, db, etc.)
├── build.sh                     # Build script for Render deployment
├── create_superuser.py          # Script to auto-provision admin user on deploy
├── db.sqlite3                   # Built-in SQLite database
├── manage.py                    # Django CLI management utility
├── render.yaml                  # Render Infrastructure Blueprint
├── requirements.txt             # Project dependencies (Django, Gunicorn, WhiteNoise)
├── seed_data.py                 # Seeds initial movies, showtimes in ₹, & reviews
└── README.md                    # Project documentation
```

---

## 🚀 Quick Start (Local Development)

### 1. Set Up Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate      # Windows
# or: source venv/bin/activate  # macOS / Linux
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Migrations & Seed Data
```bash
python manage.py migrate
python create_superuser.py
python seed_data.py
```

### 4. Run Development Server
```bash
python manage.py runserver
```
Visit **http://127.0.0.1:8000/** in your browser.

---

## 🧪 Running Automated Tests

Run the test suite to verify all models, views, booking validations, and pricing calculations:
```bash
python manage.py test
```

---

## 🔐 Admin Credentials

- **URL:** http://127.0.0.1:8000/admin/
- **Username:** `admin`
- **Password:** `admin123`

---

## 🌐 Deploying to Render

This project includes a native [`render.yaml`](render.yaml) Blueprint:

1. Push your repository to GitHub.
2. In [Render Dashboard](https://dashboard.render.com/), choose **New + → Blueprint**.
3. Select this repository.
4. Render will run [`build.sh`](build.sh), migrate SQLite, seed data, create the superuser, and launch Gunicorn automatically.
