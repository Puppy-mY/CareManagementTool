import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'care_management.settings')
django.setup()

from clients.models import RegionalSupportCenter

centers = RegionalSupportCenter.objects.all()[:5]
print(f"Total centers: {RegionalSupportCenter.objects.count()}")
print("\nFirst 5 centers:")
for center in centers:
    # バイト列として出力して確認
    print(f"ID: {center.pk}")
    print(f"Name bytes: {center.name.encode('utf-8')}")
    print(f"Office: {center.office_number}")
    print(f"Area: {center.area}")
    print("---")
