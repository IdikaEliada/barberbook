# BarberBook — Barbershop Appointment Scheduling System

A Django web app for booking barbershop appointments. Built for SEN 310.

## Features
- Customer registration/login
- Browse services and barbers
- Book an appointment (with double-booking prevention)
- View/cancel own appointments
- Admin dashboard to confirm appointments (via `is_staff` users)
- Django admin at /admin/

## Local setup
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed        # creates sample barbers, services, admin user
python manage.py runserver
```
Default seeded admin: username `admin`, password `adminpass123` (change before deploying).

## Deployment (Render.com free tier)
1. Push this project to a GitHub repo.
2. On Render: New -> Web Service -> connect the repo.
3. Build command: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
4. Start command: `gunicorn barberbook.wsgi`
5. Add environment variables: `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS=<your-app>.onrender.com`
6. Add a Render PostgreSQL instance and set `DATABASE_URL`, or leave SQLite for a demo (data resets on redeploy).
7. After first deploy, run `python manage.py migrate` and `python manage.py seed` from the Render shell.
