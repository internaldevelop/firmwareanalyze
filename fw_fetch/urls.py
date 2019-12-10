from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # 指定URL抓取固件
    path('download/', views.fwdownload, name='firmware_download'),
    path('downloadtest/', views.test, name='firmware_test'),

]