import http from 'k6/http';
import { check } from 'k6';

export const options = {
  vus: 20,
  duration: '30s',
};

export default function () {
  const url =
    'http://127.0.0.1:5000/api/v1/flights/search?date_from=2026-05-01&airport_from=IST&airport_to=ESB&people=1&page=1&per_page=10';

  const response = http.get(url);

  check(response, {
    'search status is 200': (r) => r.status === 200,
  });
}