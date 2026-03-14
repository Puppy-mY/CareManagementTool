import json
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'care_management.settings')
django.setup()

from clients.models import RegionalSupportCenter

# バックアップファイルを読み込む
try:
    with open('clients_related_converted.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    print("Successfully loaded clients_related_converted.json")
except Exception as e:
    print(f"Error loading file: {e}")
    exit(1)

# RegionalSupportCenterのデータのみを抽出
regional_centers = [item for item in data if item['model'] == 'clients.regionalsupportcenter']

print(f"Found {len(regional_centers)} regional support centers")

# データベースから既存のデータを削除
RegionalSupportCenter.objects.all().delete()
print("Cleared existing regional support centers")

# データを復元
created_count = 0
for item in regional_centers:
    fields = item['fields']
    try:
        center = RegionalSupportCenter.objects.create(
            id=item['pk'],
            name=fields['name'],
            office_number=fields['office_number'],
            postal_code=fields.get('postal_code', ''),
            address=fields.get('address', ''),
            phone=fields.get('phone', ''),
            area=fields.get('area', 'other'),
            is_active=fields.get('is_active', True)
        )
        created_count += 1
        if created_count <= 5:  # 最初の5件だけ表示
            print(f"Created: {center.name} ({center.office_number})")
    except Exception as e:
        print(f"Error creating center {item['pk']}: {e}")

print(f"\nTotal created: {created_count}")
print(f"Final count in database: {RegionalSupportCenter.objects.count()}")
