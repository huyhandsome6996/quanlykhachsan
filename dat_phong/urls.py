from django.urls import path
from . import views

app_name = 'dat_phong'

urlpatterns = [
    path('tao/', views.tao_dat_phong, name='tao_dat_phong'),
    path('check-out/<int:dat_phong_id>/', views.check_out, name='check_out'), #Tú 4
    path('them-dich-vu/<int:dat_phong_id>/', views.them_dich_vu, name='them_dich_vu'),
    path('danh-sach/', views.danh_sach_dat_phong, name='danh_sach_dat_phong'),

]
