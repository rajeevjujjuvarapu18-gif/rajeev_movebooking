/**
 * CineVerse — Seat Selection Grid (5 rows × 8 columns)
 * Interactive seat selection with dynamic price calculation.
 */
document.addEventListener('DOMContentLoaded', () => {
    const seatGrid = document.getElementById('seat-grid');
    const selectedSeatsInput = document.getElementById('id_selected_seats');
    const selectedSeatsDisplay = document.getElementById('selected-seats-display');
    const seatCountDisplay = document.getElementById('seat-count-display');
    const totalPriceDisplay = document.getElementById('total-price-display');
    const confirmBtn = document.getElementById('confirm-booking-btn');

    if (!seatGrid) return;

    // Load data passed from Django via json_script tags (or globals)
    const bookedDataEl = document.getElementById('booked-seats-data');
    const priceDataEl = document.getElementById('ticket-price-data');
    const BOOKED_SEATS = bookedDataEl ? JSON.parse(bookedDataEl.textContent) : (window.BOOKED_SEATS || []);
    const TICKET_PRICE = priceDataEl ? parseFloat(JSON.parse(priceDataEl.textContent)) : (window.TICKET_PRICE || 0);

    const rows = ['A', 'B', 'C', 'D', 'E'];  // 5 rows
    const cols = 8;                             // 8 columns
    const selectedSeats = new Set();

    // Build the 5×8 grid
    rows.forEach(row => {
        const rowDiv = document.createElement('div');
        rowDiv.className = 'seat-row';

        // Row label
        const label = document.createElement('span');
        label.className = 'seat-row-label';
        label.textContent = row;
        rowDiv.appendChild(label);

        for (let col = 1; col <= cols; col++) {
            const seatId = `${row}${col}`;
            const seat = document.createElement('div');
            seat.className = 'seat';
            seat.textContent = seatId;
            seat.dataset.seat = seatId;
            seat.id = `seat-${seatId}`;

            // Mark booked seats
            if (BOOKED_SEATS.includes(seatId)) {
                seat.classList.add('booked');
                seat.title = 'Already booked';
            } else {
                seat.addEventListener('click', () => toggleSeat(seat, seatId));
                seat.title = `Click to select seat ${seatId}`;
            }

            rowDiv.appendChild(seat);
        }

        // Right-side row label
        const labelRight = document.createElement('span');
        labelRight.className = 'seat-row-label';
        labelRight.textContent = row;
        rowDiv.appendChild(labelRight);

        seatGrid.appendChild(rowDiv);
    });

    /**
     * Toggle a seat between selected and available.
     */
    function toggleSeat(seatEl, seatId) {
        if (selectedSeats.has(seatId)) {
            selectedSeats.delete(seatId);
            seatEl.classList.remove('selected');
        } else {
            selectedSeats.add(seatId);
            seatEl.classList.add('selected');
        }
        updateSummary();
    }

    /**
     * Update the booking summary and hidden form field.
     */
    function updateSummary() {
        const seats = Array.from(selectedSeats).sort();
        const count = seats.length;
        const total = (count * TICKET_PRICE).toFixed(2);

        // Update display
        selectedSeatsDisplay.textContent = count > 0 ? seats.join(', ') : 'None';
        seatCountDisplay.textContent = count;
        totalPriceDisplay.textContent = `₹${total}`;

        // Update hidden input
        selectedSeatsInput.value = seats.join(',');

        // Enable/disable submit button
        confirmBtn.disabled = count === 0;
    }

    // Initialize summary (in case of form re-render with errors)
    if (selectedSeatsInput.value) {
        const preSelected = selectedSeatsInput.value.split(',').filter(s => s.trim());
        preSelected.forEach(seatId => {
            const seatEl = document.getElementById(`seat-${seatId.trim()}`);
            if (seatEl && !seatEl.classList.contains('booked')) {
                selectedSeats.add(seatId.trim());
                seatEl.classList.add('selected');
            }
        });
        updateSummary();
    }
});
