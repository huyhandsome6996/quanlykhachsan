from django.urls import path
from . import views

app_name = 'hoa_don'

urlpatterns = [
    path('<int:dat_phong_id>/', views.chi_tiet_hoa_don, name='chi_tiet'),
    path('<int:dat_phong_id>/thanh-toan/', views.xac_nhan_thanh_toan, name='thanh_toan'),
]
