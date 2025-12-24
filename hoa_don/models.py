from django.db import models
from dat_phong.models import DatPhong

class HoaDon(models.Model):
    TRANG_THAI_CHOICES = [
        ('chua_tt', 'Chưa thanh toán'),
        ('da_tt', 'Đã thanh toán'),
    ]

    dat_phong = models.OneToOneField(
        DatPhong,
        on_delete=models.CASCADE,
        related_name='hoa_don',
        verbose_name="Đặt phòng"
    )

    tien_phong = models.PositiveIntegerField(default=0)
    tien_dich_vu = models.PositiveIntegerField(default=0)
    tong_tien = models.PositiveIntegerField(default=0)

    trang_thai = models.CharField(
        max_length=10,
        choices=TRANG_THAI_CHOICES,
        default='chua_tt'
    )

    thoi_diem_tao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Hóa đơn {self.id} - {self.dat_phong.ten_khach}"