from django.core.management.base import BaseCommand
from files.models import FanYonalishi

class Command(BaseCommand):
    help = "Default FanYonalishi larni yaratish"
    
    def handle(self, *args, **options):
        fan_yonalishlari = [
            "O'zbek tili",
            "Til nazariyasi. Amaliy va kompyuter lingvistikasi", 
            "Ta'lim va tarbiya nazariyasi va metodikasi (ijtimoiy-gumanitar fanlar)",
            "Chet tili (Ingliz tili)",
            "Chet tili (Nemis tili)"
        ]
        
        for fan_name in fan_yonalishlari:
            fan, created = FanYonalishi.objects.get_or_create(name=fan_name)
            if created:
                self.stdout.write(f"Yaratildi: {fan_name}")
            else:
                self.stdout.write(f"Mavjud: {fan_name}")
        
        self.stdout.write(self.style.SUCCESS("Barcha fan yo'nalishlari tayyor!"))