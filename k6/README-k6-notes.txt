Run these tests with k6.

Scenarios required by assignment:
- Normal Load: 20 virtual users, 30 seconds
- Peak Load: 50 virtual users, 30 seconds
- Stress Load: 100 virtual users, 30 seconds

Endpoints tested:
1. GET /api/v1/flights/search
2. POST /api/v1/bookings

Before running bookings.js:
- Make sure the target flight exists
- Make sure the target flight has enough available seats
- Replace the JWT token in bookings.js

