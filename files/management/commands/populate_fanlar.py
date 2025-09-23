from django.core.management.base import BaseCommand
from files.models import FanYonalishi


class Command(BaseCommand):
    help = 'Fan yo\'nalishlari ma\'lumotlarini qo\'shish'

    def handle(self, *args, **options):
        fanlar = [
            "O'zbek tili",
            "Til nazariyasi. Amaliy va kompyuter lingvistikasi",
            "Ta'lim va tarbiya nazariyasi va metodikasi(ijtimoiy-gumanitar fanlar)",
            "Chet tili (Ingliz tili)",
            "Chet tili (Rus tili)",
            "Chet tili (Fransuz tili)",
            "Chet tili (Nemis tili)",
        ]
        
        for fan_nom in fanlar:
            fan, created = FanYonalishi.objects.get_or_create(
                name=fan_nom
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Fan yaratildi: {fan_nom}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Fan mavjud: {fan_nom}')
                )
        
        self.stdout.write(
            self.style.SUCCESS('Barcha fanlar muvaffaqiyatli yaratildi!')
        )