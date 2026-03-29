import http from 'k6/http';
import { check } from 'k6';

export const options = {
  vus: 20,
  duration: '30s',
};

export default function () {
  const url = 'http://127.0.0.1:5000/api/v1/bookings';

  const payload = JSON.stringify({
    flight_number: 'TK101',
    date: '2026-05-01',
    passenger_names: [
      `Load Test Passenger ${__VU}-${__ITER}`
    ],
    trip_type: 'one_way'
  });

  const params = {
    headers: {
      'Content-Type': 'application/json',
      Authorization: 'Bearer YOUR_JWT_TOKEN_HERE',
    },
  };

  const response = http.post(url, payload, params);

  check(response, {
    'booking status is 201 or 400 or 404': (r) =>
      r.status === 201 || r.status === 400 || r.status === 404,
  });
}