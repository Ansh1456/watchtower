from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from users.models import UserProfile


@login_required
def admin_view(request):
    if not request.user.is_staff:
        return redirect('dashboard')

    users = User.objects.all().order_by('-date_joined')
    total_users = users.count()
    verified_users = UserProfile.objects.filter(is_verified=True).count()
    staff_users = users.filter(is_staff=True).count()

    user_data = []
    for user in users:
        try:
            verified = user.userprofile.is_verified
        except UserProfile.DoesNotExist:
            verified = True  # superusers won't have a profile
        user_data.append({
            'user': user,
            'verified': verified,
        })

    context = {
        'user_data': user_data,
        'total_users': total_users,
        'verified_users': verified_users,
        'staff_users': staff_users,
    }
    return render(request, 'adminpanel/admin.html', context)
