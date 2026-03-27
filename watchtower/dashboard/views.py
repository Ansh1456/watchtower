import csv
import random
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


def get_metrics():
    return {
        'cpu': random.randint(20, 90),
        'ram': random.randint(30, 85),
        'disk': random.randint(40, 80),
        'cpu_history': [random.randint(10, 95) for _ in range(10)],
        'ram_history': [random.randint(20, 90) for _ in range(10)],
        'disk_history': [random.randint(35, 85) for _ in range(10)],
    }


@login_required
def dashboard_view(request):
    metrics = get_metrics()
    return render(request, 'dashboard/dashboard.html', {'metrics': metrics})


@login_required
def export_csv(request):
    metrics = get_metrics()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="watchtower_metrics.csv"'
    writer = csv.writer(response)
    writer.writerow(['Metric', 'Current Value (%)', 'History'])
    writer.writerow(['CPU Usage', metrics['cpu'], ', '.join(map(str, metrics['cpu_history']))])
    writer.writerow(['RAM Usage', metrics['ram'], ', '.join(map(str, metrics['ram_history']))])
    writer.writerow(['Disk Usage', metrics['disk'], ', '.join(map(str, metrics['disk_history']))])
    return response
