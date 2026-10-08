from django import forms
from .models import SeatBooking, MovieReview, Showtime


class SeatBookingForm(forms.ModelForm):
    """Form for booking seats at a showtime."""

    class Meta:
        model = SeatBooking
        fields = ['customer_name', 'customer_email', 'customer_phone', 'selected_seats']
        widgets = {
            'customer_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your full name',
                'id': 'id_customer_name',
            }),
            'customer_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@example.com',
                'id': 'id_customer_email',
            }),
            'customer_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone number (optional)',
                'id': 'id_customer_phone',
            }),
            'selected_seats': forms.HiddenInput(attrs={
                'id': 'id_selected_seats',
            }),
        }

    def __init__(self, *args, showtime=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.showtime = showtime

    def clean_selected_seats(self):
        seats_str = self.cleaned_data.get('selected_seats', '')
        if not seats_str:
            raise forms.ValidationError("You must select at least one seat.")

        seats = [s.strip() for s in seats_str.split(',') if s.strip()]
        if not seats:
            raise forms.ValidationError("You must select at least one seat.")

        # Validate seat format (e.g., A1, B3, E8)
        valid_rows = 'ABCDE'
        valid_cols = range(1, 9)
        for seat in seats:
            if len(seat) < 2 or seat[0] not in valid_rows:
                raise forms.ValidationError(f"Invalid seat: {seat}")
            try:
                col = int(seat[1:])
                if col not in valid_cols:
                    raise forms.ValidationError(f"Invalid seat: {seat}")
            except ValueError:
                raise forms.ValidationError(f"Invalid seat: {seat}")

        # Check for duplicate seats in the same showtime
        if self.showtime:
            already_booked = self.showtime.booked_seats()
            conflicts = [s for s in seats if s in already_booked]
            if conflicts:
                raise forms.ValidationError(
                    f"The following seats are already booked: {', '.join(conflicts)}"
                )

        return ','.join(seats)


class MovieReviewForm(forms.ModelForm):
    """Form for submitting a movie review."""

    class Meta:
        model = MovieReview
        fields = ['reviewer_name', 'rating', 'comment']
        widgets = {
            'reviewer_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your name',
                'id': 'id_reviewer_name',
            }),
            'rating': forms.HiddenInput(attrs={
                'id': 'id_rating',
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your review...',
                'rows': 4,
                'id': 'id_comment',
            }),
        }

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating is None:
            raise forms.ValidationError("Please select a rating.")
        if rating < 1 or rating > 5:
            raise forms.ValidationError("Rating must be between 1 and 5.")
        return rating
