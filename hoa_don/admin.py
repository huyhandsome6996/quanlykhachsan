# hoa_don/admin.py
from django.contrib import admin
from .models import HoaDon

@admin.register(HoaDon)
class HoaDonAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'dat_phong',
        'tong_tien',
        'trang_thai',
        'thoi_diem_tao'
    )
    list_filter = ('trang_thai',) #
