from django.shortcuts import render, redirect, get_list_or_404
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

from .models import SuDungDichVu #nguyên 5
def check_out(request, dat_phong_id):
    dat_phong = get_object_or_404(DatPhong, id=dat_phong_id, dang_o=True)

    ngay_tra = timezone.now().date()
    so_dem = (ngay_tra - dat_phong.ngay_nhan).days
    if so_dem <= 0:
        so_dem = 1

    gia_mot_dem = dat_phong.phong.loai_phong.gia_mot_dem
    tong_dich_vu = sum(dv.thanh_tien() for dv in SuDungDichVu.objects.filter(dat_phong=dat_phong)) #nguyên 5
    tong_tien = so_dem * gia_mot_dem + tong_dich_vu #nguyên 5: cộng thêm tổng dịch vụ sử dụng
###############################################################


   
    if request.method == 'POST':
        # cập nhật đơn đặt phòng
        dat_phong.ngay_tra = ngay_tra
        dat_phong.dang_o = False
        dat_phong.save()

        # cập nhật phòng
        phong = dat_phong.phong
        phong.trang_thai = 'trong'
        phong.save()

        return redirect('bao_cao:trang_chu')

