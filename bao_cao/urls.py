from django.urls import path
from . import views

app_name = 'bao_cao'

urlpatterns = [
    path('', views.trang_chu, name='trang_chu'),
]
