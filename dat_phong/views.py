from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from khach_san.models import Phong
from .models import DatPhong, SuDungDichVu, DichVu
from hoa_don.models import HoaDon
from django.contrib.admin.views.decorators import staff_member_required

# =========================
# TẠO ĐẶT PHÒNG
# =========================
@staff_member_required
def tao_dat_phong(request):
    phong_trong = Phong.objects.filter(trang_thai='trong')

    if request.method == 'POST':
        phong_id = request.POST.get('phong')
        ten_khach = request.POST.get('ten_khach')
        loai_khach = request.POST.get('loai_khach')
        ngay_nhan = request.POST.get('ngay_nhan')
        

        phong = get_object_or_404(Phong, id=phong_id)
        ngay_tra_du_kien = request.POST.get('ngay_tra_du_kien')

        # tạo đơn đặt phòng
        DatPhong.objects.create(
            phong=phong,
            ten_khach=ten_khach,
            loai_khach=loai_khach,
            ngay_nhan=ngay_nhan,
            ngay_tra_du_kien=ngay_tra_du_kien,
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
@staff_member_required
def check_out(request, dat_phong_id):
    dat_phong = get_object_or_404(
        DatPhong,
        id=dat_phong_id,
        dang_o=True
    )

    # ====== TÍNH TIỀN ======
    ngay_tra = timezone.now().date()
    so_dem = (ngay_tra - dat_phong.ngay_nhan).days
    if so_dem <= 0:
        so_dem = 1

    gia_mot_dem = dat_phong.phong.loai_phong.gia_mot_dem

    ds_dich_vu = SuDungDichVu.objects.filter(dat_phong=dat_phong)
    tong_dich_vu = sum(dv.thanh_tien for dv in ds_dich_vu)

    tien_phong = so_dem * gia_mot_dem
    tong_tien = tien_phong + tong_dich_vu

    # ====== KHI XÁC NHẬN CHECK-OUT ======
    if request.method == 'POST':
        # 1. Cập nhật đặt phòng
        dat_phong.ngay_tra = ngay_tra
        dat_phong.dang_o = False
        dat_phong.save()

        # 2. Cập nhật phòng
        phong = dat_phong.phong
        phong.trang_thai = 'trong'
        phong.save()

        # 3. TẠO HÓA ĐƠN (QUAN TRỌNG)
        HoaDon.objects.get_or_create(
            dat_phong=dat_phong,
            defaults={
                'tien_phong': tien_phong,
                'tien_dich_vu': tong_dich_vu,
                'tong_tien': tong_tien,
                'trang_thai': 'chua_tt'
            }
        )

        # 4. CHỈ redirect SAU KHI ĐÃ TẠO HÓA ĐƠN
        return redirect('hoa_don:chi_tiet', dat_phong.id)

    # ====== GET: HIỂN THỊ TRANG CHECKOUT ======
    return render(request, 'dat_phong/checkout.html', {
        'dat_phong': dat_phong,
        'so_dem': so_dem,
        'tien_phong': tien_phong,
        'ds_dich_vu': ds_dich_vu,
        'tien_dich_vu': tong_dich_vu,
        'tong_tien': tong_tien,
    })


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


def danh_sach_dat_phong(request):
    danh_sach = DatPhong.objects.select_related('phong') \
        .order_by('-dang_o', '-ngay_nhan')
    context = {
        'danh_sach': danh_sach
    }

