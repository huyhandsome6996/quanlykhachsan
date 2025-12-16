from django.db import models


class LoaiPhong(models.Model):
    ten_loai = models.CharField(max_length=100)
    gia_mot_dem = models.PositiveIntegerField(
        verbose_name="Giá / đêm (VND)"
    )

    def __str__(self):
        return self.ten_loai

    

    
class Phong(models.Model):
    TRANG_THAI_CHOICES = [
        ('trong', 'Trống'),
        ('dang_thue', 'Đang thuê'),
        ('dang_bao_tri', 'Đang bảo trì'),
    ]

    ma_phong = models.CharField(max_length=10, unique=True)
    loai_phong = models.ForeignKey(LoaiPhong, on_delete=models.PROTECT)
    trang_thai = models.CharField(
        max_length=20,
        choices=TRANG_THAI_CHOICES,
        default='trong'
    )

    def __str__(self):
        return f"Phòng {self.ma_phong}"
