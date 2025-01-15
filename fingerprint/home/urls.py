from . import views
from django.urls import path

urlpatterns = [
    path('', views.scan_fingerprint, name='scan_fingerprint'),
    path('fingerprint-success/', views.fingerprint_success, name='fingerprint_success'),
]
