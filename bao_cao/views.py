from django.shortcuts import render
from khach_san.models import Phong

def trang_chu(request):
    return render(request, 'trang_chu.html', {
        'so_phong_trong': Phong.objects.filter(trang_thai='trong').count(),
        'so_phong_dang_thue': Phong.objects.filter(trang_thai='dang_thue').count(),
        'doanh_thu_hom_nay': 0,
        'don_dat_hom_nay': 0,
        'danh_sach_phong': Phong.objects.select_related('loai_phong').all()
    })
