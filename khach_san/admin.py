from django.contrib import admin
from .models import Phong, LoaiPhong


@admin.register(LoaiPhong)
class LoaiPhongAdmin(admin.ModelAdmin):
    list_display = ('ten_loai',)


@admin.register(Phong)
class PhongAdmin(admin.ModelAdmin):
    list_display = ('ma_phong', 'loai_phong', 'trang_thai')
    list_filter = ('trang_thai', 'loai_phong')
