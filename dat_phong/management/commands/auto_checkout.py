from django.core.management.base import BaseCommand
from django.utils import timezone
from dat_phong.models import DatPhong

class Command(BaseCommand):
    help = "Tự động trả phòng khi đến ngày trả dự kiến"

    def handle(self, *args, **kwargs):
        today = timezone.now().date()

        danh_sach = DatPhong.objects.filter(
            dang_o=True,
            ngay_tra_du_kien__lte=today
        )

        for dp in danh_sach:
            dp.ngay_tra = today
            dp.dang_o = False
            dp.save()

            phong = dp.phong
            phong.trang_thai = 'trong'
            phong.save()

        self.stdout.write("Auto checkout completed.")
