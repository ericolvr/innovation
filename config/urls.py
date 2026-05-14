from django.urls import path, include, re_path
from django.views.generic import TemplateView

urlpatterns = [
    path('api/auth/', include('apps.users.urls.auth')),
    path('api/users/', include('apps.users.urls.users')),
    path('api/clients/', include('apps.clients.urls')),
    path('api/condominiums/', include('apps.condominiums.urls.condominiums')),
    path('api/maintenances/', include('apps.condominiums.urls.maintenances')),
    path('api/technicians/', include('apps.technicians.urls')),
    path('api/schedules/', include('apps.condominiums.urls.schedules')),

    # catch-all — React Router assume o controle
    re_path(r'^.*$', TemplateView.as_view(template_name='index.html')),
]
