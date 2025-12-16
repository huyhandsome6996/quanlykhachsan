from django.db import models
from khach_san.models import Phong


class Khach(models.Model):
    LOAI_KHACH_CHOICES = [
        ('vang_lai', 'Vãng lai'),
        ('tour', 'Khách tour đoàn'),
        ('booking', 'Booking'),
        ('agoda', 'Agoda'),
        ('traveloka', 'Traveloka'),
    ]

    ten_khach = models.CharField(max_length=100)
    loai_khach = models.CharField(max_length=20, choices=LOAI_KHACH_CHOICES)

    def __str__(self):
        return self.ten_khach


class DatPhong(models.Model):
    phong = models.ForeignKey(Phong, on_delete=models.PROTECT)
    khach = models.ForeignKey(Khach, on_delete=models.PROTECT)
    ngay_nhan = models.DateField()
    ngay_tra = models.DateField(null=True, blank=True)
    dang_o = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.phong} - {self.khach}"
