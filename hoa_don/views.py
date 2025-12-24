from django.shortcuts import render, get_object_or_404
from .models import HoaDon
from dat_phong.models import DatPhong
from django.shortcuts import redirect

def chi_tiet_hoa_don(request, dat_phong_id):
    hoa_don = get_object_or_404(HoaDon, dat_phong_id=dat_phong_id)
    return render(request, 'hoa_don/chi_tiet_hoa_don.html', {
        'hoa_don': hoa_don
    })

def xac_nhan_thanh_toan(request, dat_phong_id):
    hoa_don = get_object_or_404(HoaDon, dat_phong_id=dat_phong_id)

    if request.method == 'POST':
        hoa_don.trang_thai = 'da_tt'
        hoa_don.save()
        return redirect('hoa_don:chi_tiet', dat_phong_id)

    return render(request, 'hoa_don/xac_nhan_thanh_toan.html', {
        'hoa_don': hoa_don
    })
