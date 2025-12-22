from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from khach_san.models import Phong
from .models import DatPhong, SuDungDichVu, DichVu


# =========================
# TẠO ĐẶT PHÒNG
# =========================
def tao_dat_phong(request):
    phong_trong = Phong.objects.filter(trang_thai='trong')

    if request.method == 'POST':
        phong_id = request.POST.get('phong')
        ten_khach = request.POST.get('ten_khach')
        loai_khach = request.POST.get('loai_khach')
        ngay_nhan = request.POST.get('ngay_nhan')

        phong = get_object_or_404(Phong, id=phong_id)

        # tạo đơn đặt phòng
        DatPhong.objects.create(
            phong=phong,
            ten_khach=ten_khach,
            loai_khach=loai_khach,
            ngay_nhan=ngay_nhan,
            dang_o=True
        )

        # cập nhật trạng thái phòng
        phong.trang_thai = 'dang_thue'
        phong.save()

        return redirect('bao_cao:trang_chu')

    context = {
        'phong_trong': phong_trong
    }
    return render(request, 'dat_phong/tao_dat_phong.html', context)


# =========================
# CHECK-OUT + TÍNH TIỀN
# =========================
def check_out(request, dat_phong_id):
    dat_phong = get_object_or_404(DatPhong, id=dat_phong_id, dang_o=True)

    ngay_tra = timezone.now().date()
    so_dem = (ngay_tra - dat_phong.ngay_nhan).days
    if so_dem <= 0:
        so_dem = 1

    gia_mot_dem = dat_phong.phong.loai_phong.gia_mot_dem
    ds_dich_vu = SuDungDichVu.objects.filter(dat_phong=dat_phong)
    tong_dich_vu = sum(dv.thanh_tien() for dv in ds_dich_vu)

    tong_tien = so_dem * gia_mot_dem + tong_dich_vu

    if request.method == 'POST':
        dat_phong.ngay_tra = ngay_tra
        dat_phong.dang_o = False
        dat_phong.save()

        phong = dat_phong.phong
        phong.trang_thai = 'trong'
        phong.save()

        return redirect('bao_cao:trang_chu')

    context = {
        'dat_phong': dat_phong,
        'so_dem': so_dem,
        'gia_mot_dem': gia_mot_dem,
        'ds_dich_vu': ds_dich_vu,
        'tong_dich_vu': tong_dich_vu,
        'tong_tien': tong_tien
    }
    return render(request, 'dat_phong/checkout.html', context)


def them_dich_vu(request, dat_phong_id):
    dat_phong = get_object_or_404(DatPhong, id=dat_phong_id, dang_o=True)
    danh_sach_dich_vu = DichVu.objects.all()

    if request.method == 'POST':
        dich_vu_id = request.POST.get('dich_vu')
        so_luong = int(request.POST.get('so_luong', 1))

        dich_vu = get_object_or_404(DichVu, id=dich_vu_id)

        SuDungDichVu.objects.create(
            dat_phong=dat_phong,
            dich_vu=dich_vu,
            so_luong=so_luong
        )

        return redirect('khach_san:chi_tiet_phong', ma_phong=dat_phong.phong.ma_phong)

    context = {
        'dat_phong': dat_phong,
        'danh_sach_dich_vu': danh_sach_dich_vu
    }
    return render(request, 'dat_phong/them_dich_vu.html', context)
