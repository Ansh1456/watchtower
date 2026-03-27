#!/usr/bin/env bash
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
python manage.py shell -c "
from django.contrib.auth.models import User
from users.models import UserProfile
if not User.objects.filter(username='admin').exists():
    u = User.objects.create_superuser('admin', 'admin@demo.com', 'admin1234')
    UserProfile.objects.create(user=u, is_verified=True)
    print('Admin created')
else:
    print('Admin already exists')
"
