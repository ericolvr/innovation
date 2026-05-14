from django.urls import path
from apps.condominiums.views import ScheduleListView

urlpatterns = [
    path('', ScheduleListView.as_view(), name='schedule-list'),
]
