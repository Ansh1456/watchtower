#!/bin/bash
echo "=== Watchtower Setup ==="
pip install -r requirements.txt
python manage.py migrate
python manage.py shell -c "
from django.contrib.auth.models import User
from users.models import UserProfile
if not User.objects.filter(username='admin').exists():
    u = User.objects.create_superuser('admin', 'admin@demo.com', 'admin123')
    UserProfile.objects.create(user=u, is_verified=True)
    print('Created admin user: admin / admin123')
else:
    print('Admin already exists.')
"
echo ""
echo "=== Setup Complete ==="
echo "Run: python manage.py runserver"
echo "Open: http://127.0.0.1:8000"
echo "Admin login: admin / admin123"
