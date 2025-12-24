from django.db import models
from django.db.models import Max
from khach_san.models import Phong



class DatPhong(models.Model):
    LOAI_KHACH_CHOICES = [
        ('vang_lai', 'Vãng lai'),
        ('tour', 'Khách tour đoàn'),
        ('booking', 'Booking'),
        ('agoda', 'Agoda'),
        ('traveloka', 'Traveloka'),
    ]

    ma_khach = models.CharField(
        max_length=10,
        unique=True,
        editable=False,
        null=True,
        blank=True,
        verbose_name="Mã khách"
    )

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

    ngay_tra_du_kien = models.DateField(
        verbose_name="Ngày trả dự kiến"
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

    def save(self, *args, **kwargs):
        if not self.ma_khach:
            max_code = DatPhong.objects.aggregate(
                max_code=Max('ma_khach')
            )['max_code']

            if max_code:
                number = int(max_code.replace('KH', '')) + 1
            else:
                number = 1

            self.ma_khach = f"KH{number:02d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.ma_khach} - {self.ten_khach}"

    class Meta:
        ordering = ['-dang_o', '-ngay_nhan']


class DichVu(models.Model):
    ten_dich_vu = models.CharField(max_length=100)
    gia = models.PositiveIntegerField()
    don_vi = models.CharField(max_length=50)

    def __str__(self):
        return self.ten_dich_vu


class SuDungDichVu(models.Model):
    dat_phong = models.ForeignKey(DatPhong, on_delete=models.CASCADE)
    dich_vu = models.ForeignKey(DichVu, on_delete=models.PROTECT)
    so_luong = models.PositiveIntegerField(default=1)
    thoi_diem = models.DateTimeField(auto_now_add=True)

    def thanh_tien(self):
        return self.so_luong * self.dich_vu.gia
