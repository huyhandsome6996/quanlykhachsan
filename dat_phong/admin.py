from django.contrib import admin
from .models import DatPhong
from .models import DichVu
from .models import SuDungDichVu


@admin.register(DatPhong)
class DatPhongAdmin(admin.ModelAdmin):
    list_display = (
        'phong',
        'ten_khach',
        'loai_khach',
        'ngay_nhan',
        'ngay_tra',
        'dang_o',
    )

    list_filter = ('loai_khach', 'dang_o')
    search_fields = ('ten_khach',)

@admin.register(DichVu)
class DichVuAdmin(admin.ModelAdmin):
    list_display = ('ten_dich_vu', 'gia', 'don_vi')

@admin.register(SuDungDichVu)
class SuDungDichVuAdmin(admin.ModelAdmin):
    list_display = ('dat_phong', 'dich_vu', 'so_luong', 'thoi_diem')