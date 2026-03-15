# salon-booking-platform

`salon_booking` is a custom Frappe app that provides an Uber-like booking experience for beauty and salon services. Customers can discover providers by location, book appointments, and submit ratings after service completion.

## Features

- Location-aware provider directory (`Service Provider`)
- Service catalog (`Service`)
- Booking workflow with status tracking (`Booking`)
- Customer metadata (`Customer Profile`)
- Weekly schedules (`Provider Availability`)
- Post-service feedback (`Review Rating`)
- Whitelisted API endpoints in `salon_booking/api.py`

## App Structure

```text
salon_booking/
├── setup.py
├── requirements.txt
└── salon_booking/
    ├── api.py
    ├── hooks.py
    ├── config/desktop.py
    ├── modules.txt
    └── doctype/
        ├── service_provider/
        ├── service/
        ├── booking/
        ├── customer_profile/
        ├── provider_availability/
        └── review_rating/
```

## DocTypes Included

1. **Service Provider**
   - provider_name, provider_type (Freelancer/Salon), contact details, location, rating, active flag
2. **Service**
   - name, category, duration, base price, active flag
3. **Booking**
   - customer, provider, service, date/time, location, status, price, payment status
4. **Customer Profile**
   - full name, linked user, phone/email, default address, geo-coordinates
5. **Provider Availability**
   - provider, day_of_week, start_time, end_time, availability toggle
6. **Review Rating**
   - booking, customer, provider, rating, comment, review date

## API Endpoints

All endpoints are whitelisted and accessible via `/api/method/salon_booking.api.<method_name>`.

### 1) Create Booking

```bash
curl -X POST http://localhost:8000/api/method/salon_booking.api.create_booking \
  -H "Authorization: token <api_key>:<api_secret>" \
  -H "Content-Type: application/json" \
  -d '{
    "customer": "CUST-0001",
    "provider": "PROV-0001",
    "service": "Bridal Makeup",
    "booking_date": "2026-03-20",
    "booking_time": "14:00:00",
    "address": "Downtown, Dubai",
    "latitude": 25.2048,
    "longitude": 55.2708
  }'
```

### 2) Get Nearby Providers

```bash
curl "http://localhost:8000/api/method/salon_booking.api.get_nearby_providers?latitude=25.2048&longitude=55.2708&radius_km=8"
```

### 3) Check Provider Availability

```bash
curl "http://localhost:8000/api/method/salon_booking.api.check_provider_availability?provider=PROV-0001&booking_date=2026-03-20&booking_time=14:00:00"
```

### 4) Submit Review

```bash
curl -X POST http://localhost:8000/api/method/salon_booking.api.submit_review \
  -H "Authorization: token <api_key>:<api_secret>" \
  -H "Content-Type: application/json" \
  -d '{"booking": "BK-2026-00001", "rating": 4.5, "review_text": "Great experience"}'
```

## Local Development with Bench

```bash
# from frappe-bench/apps
bench new-app salon_booking
# replace app files with this repository content

# from frappe-bench
bench --site yoursite.local install-app salon_booking
bench --site yoursite.local migrate
bench start
```

## Docker Setup (frappe_docker style)

1. Ensure Docker and Docker Compose are installed.
2. Use provided compose file:

```bash
cd docker/frappe_docker
docker compose up -d
```

3. Open `http://localhost:8000` after services come up.

> Note: In production, use managed secrets, persistent volumes, a reverse proxy, and separate worker/scheduler services.

## GitHub Preparation Checklist

```bash
git init
git add .
git commit -m "feat: scaffold salon_booking frappe app with core doctypes and apis"
git branch -M main
git remote add origin git@github.com:<your-username>/salon-booking-platform.git
git push -u origin main
```

Repository name target: **salon-booking-platform**.

## Recommended Commit Messages

- `feat: scaffold salon_booking app structure`
- `feat: add service marketplace doctypes`
- `feat: implement booking and review APIs`
- `docs: add deployment and bench instructions`
- `chore: add frappe-focused gitignore and docker compose`

## Install App on Existing Site

```bash
cd frappe-bench
bench get-app https://github.com/<your-username>/salon-booking-platform.git
bench --site yoursite.local install-app salon_booking
bench --site yoursite.local migrate
bench --site yoursite.local clear-cache
```

## Production Notes

- Add server-side validations (slot length, overlap windows, cancellation policy).
- Add role-based permission records through fixtures.
- Add scheduled jobs for reminders and no-show handling.
- Add unit/integration tests before go-live.
