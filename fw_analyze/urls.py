from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('binwalk_scan_signature/', views.binwalk_scan_signature, name='firmware_binwalk'),
    path('binwalk_scan_opcodes/', views.binwalk_scan_opcodes, name='firmware_binwalk'),
    path('binwalk_file_extract/', views.binwalk_file_extract, name='firmware_binwalk'),
]