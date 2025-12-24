from django.shortcuts import render
from khach_san.models import Phong
from dat_phong.models import DatPhong
from django.contrib.admin.views.decorators import staff_member_required



def trang_chu(request):
    return render(request, 'trang_chu.html', {
        'so_phong_trong': Phong.objects.filter(trang_thai='trong').count(),
        'so_phong_dang_thue': Phong.objects.filter(trang_thai='dang_thue').count(),
        'doanh_thu_hom_nay': 0,
        'don_dat_hom_nay': 0,
        'danh_sach_phong': Phong.objects.select_related('loai_phong').all()
    })
#-----------------------------------------------
@staff_member_required
def bao_cao_cong_suat_phong(request): #Tú 1
    tong_phong = Phong.objects.count()
    phong_dang_o = DatPhong.objects.filter(dang_o=True).count()

    cong_suat = 0
    if tong_phong > 0:
        cong_suat = round((phong_dang_o / tong_phong) * 100, 2)

    context = {
        'tong_phong': tong_phong,
        'phong_dang_o': phong_dang_o,
        'cong_suat': cong_suat
    }

    return render(request, 'bao_cao/cong_suat_phong.html', context)