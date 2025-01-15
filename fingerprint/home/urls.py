from . import views
from django.urls import path

urlpatterns = [
    path('', views.scan_fingerprint, name='scan_fingerprint'),
    path('fingerprint-success/', views.fingerprint_success, name='fingerprint_success'),
    path('upload-document/', views.upload_document, name='upload_document'),
    path('document-success/', views.document_success, name='document_success'),
]
