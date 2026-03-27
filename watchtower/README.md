   Watchtower — System Monitoring Dashboard

A clean, minimal system monitoring prototype built with Django + Chart.js.

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run setup (creates DB + admin user)
bash setup.sh

# 3. Start the server
python manage.py runserver

# 4. Open in browser
http://127.0.0.1:8000
```

## Demo Credentials

| Role  | Username | Password |
|-------|----------|----------|
| Admin | admin    | admin123 |

## Features

- **Registration** with mocked OTP email verification
- **Login/Logout** with session management
- **Dashboard** — live CPU, RAM, Disk gauges (auto-refresh every 3s)
- **Charts** — Line chart + Donut chart via Chart.js
- **Admin Panel** — user list with roles, verification status, join date
- **CSV Export** — download current metrics as a CSV file

## Project Structure

```
watchtower/
├── manage.py
├── requirements.txt
├── setup.sh
├── watchtower/         # Django project config
│   ├── settings.py
│   └── urls.py
├── users/              # Auth: register, login, OTP
│   ├── models.py
│   ├── views.py
│   └── templates/users/
├── dashboard/          # Metrics dashboard + CSV export
│   ├── views.py
│   └── templates/dashboard/
├── adminpanel/         # Admin user management
│   ├── views.py
│   └── templates/adminpanel/
├── static/
│   ├── css/style.css
│   └── js/dashboard.js
└── templates/          # Shared base templates
    ├── base_auth.html
    └── base_dashboard.html
```

## Notes

- Metrics are randomly generated (demo mode) — no real system monitoring needed
- OTP is displayed in a flash message instead of email (demo mode)
- SQLite database — no external DB required
