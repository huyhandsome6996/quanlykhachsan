from django.shortcuts import render
from .models import Phong

def danh_sach_phong(request):
    danh_sach_phong = Phong.objects.select_related('loai_phong').all()
    return render(request, 'khach_san/danh_sach_phong.html', {
        'danh_sach_phong': danh_sach_phong
    })
