/**
 * CineVerse — Review Star Rating Input
 * Interactive 1–5 star rating selector.
 */
document.addEventListener('DOMContentLoaded', () => {
    const starContainer = document.getElementById('star-rating-input');
    const ratingInput = document.getElementById('id_rating');

    if (!starContainer || !ratingInput) return;

    const stars = starContainer.querySelectorAll('.star-input');
    let currentRating = parseInt(ratingInput.value) || 0;

    // Initialise stars if there's a pre-existing value
    if (currentRating > 0) {
        setStars(currentRating);
    }

    stars.forEach(star => {
        const rating = parseInt(star.dataset.rating);

        // Hover preview
        star.addEventListener('mouseenter', () => {
            previewStars(rating);
        });

        // Click to set
        star.addEventListener('click', () => {
            currentRating = rating;
            ratingInput.value = rating;
            setStars(rating);
        });
    });

    // Reset preview on mouse leave
    starContainer.addEventListener('mouseleave', () => {
        setStars(currentRating);
    });

    /**
     * Highlight stars up to the given rating (filled state).
     */
    function setStars(rating) {
        stars.forEach(star => {
            const val = parseInt(star.dataset.rating);
            star.classList.remove('hover-preview');
            if (val <= rating) {
                star.classList.add('active');
                star.classList.replace('bi-star', 'bi-star-fill');
            } else {
                star.classList.remove('active');
                star.classList.replace('bi-star-fill', 'bi-star');
            }
        });
    }

    /**
     * Show a hover preview up to the given rating.
     */
    function previewStars(rating) {
        stars.forEach(star => {
            const val = parseInt(star.dataset.rating);
            if (val <= rating) {
                star.classList.add('hover-preview');
                star.classList.replace('bi-star', 'bi-star-fill');
            } else {
                star.classList.remove('hover-preview');
                if (val > currentRating) {
                    star.classList.replace('bi-star-fill', 'bi-star');
                }
            }
        });
    }
});
