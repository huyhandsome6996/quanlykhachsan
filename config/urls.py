
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('bao_cao.urls')),
    path('', include('khach_san.urls')),
    path('dat-phong/', include('dat_phong.urls')),
    path('hoa-don/', include('hoa_don.urls')),

   
]

