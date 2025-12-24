# hoa_don/admin.py
from django.contrib import admin
from django.db.models import Sum, Avg
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

    list_filter = ('trang_thai', 'thoi_diem_tao')

    change_list_template = "admin/hoa_don/hoa_don_changelist.html"

    def changelist_view(self, request, extra_context=None):
        qs = self.get_queryset(request).filter(trang_thai='da_tt')

        start = request.GET.get('start')
        end = request.GET.get('end')

        if start and end:
            qs = qs.filter(thoi_diem_tao__date__range=[start, end])

        tong_doanh_thu = qs.aggregate(
            total=Sum('tong_tien')
        )['total'] or 0

        doanh_thu_tb = qs.aggregate(
            avg=Avg('tong_tien')
        )['avg'] or 0

        extra_context = extra_context or {}
        extra_context.update({
            'tong_doanh_thu': tong_doanh_thu,
            'doanh_thu_tb': round(doanh_thu_tb),
            'start': start,
            'end': end,
        })

        return super().changelist_view(request, extra_context=extra_context)
