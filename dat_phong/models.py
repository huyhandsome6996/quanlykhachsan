from django.db import models
from khach_san.models import Phong


from django.db import models
from khach_san.models import Phong


class DatPhong(models.Model):
    LOAI_KHACH_CHOICES = [
        ('vang_lai', 'Vãng lai'),
        ('tour', 'Khách tour đoàn'),
        ('booking', 'Booking'),
        ('agoda', 'Agoda'),
        ('traveloka', 'Traveloka'),
    ]

    phong = models.ForeignKey(
        Phong,
        on_delete=models.PROTECT,
        verbose_name="Phòng"
    )

    ten_khach = models.CharField(
        max_length=100,
        verbose_name="Tên khách"
    )

    loai_khach = models.CharField(
        max_length=20,
        choices=LOAI_KHACH_CHOICES,
        verbose_name="Loại khách"
    )

    ngay_nhan = models.DateField(
        verbose_name="Ngày nhận phòng"
    )

    ngay_tra = models.DateField(
        null=True,
        blank=True,
        verbose_name="Ngày trả phòng"
    )

    dang_o = models.BooleanField(
        default=True,
        verbose_name="Đang ở"
    )

    def __str__(self):
        return f"{self.phong.ma_phong} - {self.ten_khach}"

#nguyên 5
class DichVu(models.Model):
    ten_dich_vu = models.CharField(max_length=100)
    gia = models.PositiveIntegerField()
    don_vi = models.CharField(max_length=50)

    def __str__(self):
        return self.ten_dich_vu

#nguyên 5
class SuDungDichVu(models.Model):
    dat_phong = models.ForeignKey(DatPhong, on_delete=models.CASCADE)
    dich_vu = models.ForeignKey(DichVu, on_delete=models.PROTECT)
    so_luong = models.PositiveIntegerField(default=1)
    thoi_diem = models.DateTimeField(auto_now_add=True)

    def thanh_tien(self):
        return self.so_luong * self.dich_vu.gia