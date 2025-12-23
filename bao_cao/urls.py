from django.urls import path
from . import views

app_name = 'bao_cao'

urlpatterns = [
    path('', views.trang_chu, name='trang_chu'),
    path('cong-suat-phong/', views.bao_cao_cong_suat_phong, name='cong_suat_phong'), #Tú 2
]


