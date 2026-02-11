import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'care_management.settings')
django.setup()

from clients.models import HomeCareSupportOffice

# 安濃津ろまんの情報を登録
office, created = HomeCareSupportOffice.objects.get_or_create(
    office_number='2470100419',
    defaults={
        'name': '居宅介護支援事業所 安濃津ろまん',
        'postal_code': '514-0009',
        'address': '三重県津市羽所町○○',  # 実際の住所に変更してください
        'phone': '059-123-4567',  # 実際の電話番号に変更してください
        'fax': '059-123-4568',  # 実際のFAX番号に変更してください
        'manager_name': '',  # 管理者名を入力してください
        'is_active': True,
    }
)

if created:
    print(f'居宅介護支援事業所「{office.name}」を登録しました')
else:
    print(f'居宅介護支援事業所「{office.name}」は既に登録されています')

print(f'\n総登録数: {HomeCareSupportOffice.objects.count()}件')
