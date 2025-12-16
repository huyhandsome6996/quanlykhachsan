from django.contrib import admin
from .models import Khach, DatPhong


@admin.register(Khach)
class KhachAdmin(admin.ModelAdmin):
    list_display = ('ten_khach', 'loai_khach')


@admin.register(DatPhong)
class DatPhongAdmin(admin.ModelAdmin):
    list_display = ('phong', 'khach', 'ngay_nhan', 'dang_o')
