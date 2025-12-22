from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from khach_san.models import Phong
from .models import DatPhong, SuDungDichVu


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
    dat_phong = get_object_or_404(
        DatPhong,
        id=dat_phong_id,
        dang_o=True
    )

    # ngày trả
    ngay_tra = timezone.now().date()

    # số đêm
    so_dem = (ngay_tra - dat_phong.ngay_nhan).days
    if so_dem <= 0:
        so_dem = 1

    # tiền phòng
    gia_mot_dem = dat_phong.phong.loai_phong.gia_mot_dem
    tien_phong = so_dem * gia_mot_dem

    # tiền dịch vụ
    danh_sach_dv = SuDungDichVu.objects.filter(dat_phong=dat_phong)
    tong_dich_vu = sum(dv.thanh_tien() for dv in danh_sach_dv)

    # tổng tiền
    tong_tien = tien_phong + tong_dich_vu

    # ================= POST: xác nhận check-out =================
    if request.method == 'POST':
        dat_phong.ngay_tra = ngay_tra
        dat_phong.dang_o = False
        dat_phong.save()

        phong = dat_phong.phong
        phong.trang_thai = 'trong'
        phong.save()

        return redirect('bao_cao:trang_chu')

    # ================= GET: hiển thị trang check-out =================
    context = {
        'dat_phong': dat_phong,
        'so_dem': so_dem,
        'gia_mot_dem': gia_mot_dem,
        'tien_phong': tien_phong,
        'danh_sach_dv': danh_sach_dv,
        'tong_dich_vu': tong_dich_vu,
        'tong_tien': tong_tien,
    }

    return render(request, 'dat_phong/checkout.html', context)
