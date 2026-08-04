from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from autonomous_activation_system.notifications.models import Notification

@login_required
def notification_list(request):
    notifications = request.user.notifications.order_by('-created_at')[:50]
    unread_count = request.user.notifications.filter(is_read=False).count()
    return render(request, 'notifications/index.html', {'notifications': notifications, 'unread_count': unread_count})
