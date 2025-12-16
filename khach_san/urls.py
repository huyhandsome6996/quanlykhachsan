from django.urls import path
from . import views

app_name = 'khach_san'

urlpatterns = [
    path('phong/', views.danh_sach_phong, name='danh_sach_phong'),
    path('phong/<str:ma_phong>/', views.chi_tiet_phong, name='chi_tiet_phong'),
]
