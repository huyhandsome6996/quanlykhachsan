from django.shortcuts import render, get_object_or_404
from .models import Phong


def danh_sach_phong(request):
    danh_sach_phong = Phong.objects.select_related('loai_phong').all()
    return render(request, 'khach_san/danh_sach_phong.html', {
        'danh_sach_phong': danh_sach_phong
    })


def chi_tiet_phong(request, ma_phong):
    phong = get_object_or_404(Phong, ma_phong=ma_phong)
    return render(request, 'khach_san/chi_tiet_phong.html', {
        'phong': phong
    })
