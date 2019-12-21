from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('binwalk_scan_signature/', views.binwalk_scan_signature, name='firmware_binwalk'), # 固件文件头自动解码或解析
    path('binwalk_scan_opcodes/', views.binwalk_scan_opcodes, name='firmware_binwalk'),     # 架构识别
    path('binwalk_file_extract/', views.binwalk_file_extract, name='firmware_binwalk'),     # 抽取文件
    path('binwalk_file_test/', views.binwalk_file_test, name='firmware_binwalk'),  # 抽取文件
]