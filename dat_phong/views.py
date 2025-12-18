from django.shortcuts import render, redirect
from khach_san.models import Phong
from .models import DatPhong
from django.utils import timezone


def tao_dat_phong(request):
    phong_trong = Phong.objects.filter(trang_thai='trong')

    if request.method == 'POST':
        phong_id = request.POST.get('phong')
        ten_khach = request.POST.get('ten_khach')
        loai_khach = request.POST.get('loai_khach')
        ngay_nhan = request.POST.get('ngay_nhan')

        phong = Phong.objects.get(id=phong_id)

        # Tạo đặt phòng
        DatPhong.objects.create(
            phong=phong,
            ten_khach=ten_khach,
            loai_khach=loai_khach,
            ngay_nhan=ngay_nhan,
            dang_o=True
        )

        # Cập nhật trạng thái phòng
        phong.trang_thai = 'dang_thue'
        phong.save()

        return redirect('bao_cao:trang_chu')

    context = {
        'phong_trong': phong_trong
    }
    return render(request, 'dat_phong/tao_dat_phong.html', context)
