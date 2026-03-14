#!/usr/bin/env python
"""
データベース主キー変更後のデータ復元スクリプト
insurance_number (主キー) から id (主キー) への移行
"""
import json
import os
import django

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'care_management.settings')
django.setup()

from clients.models import Client
from assessments.models import Assessment
from django.contrib.auth.models import User

# デフォルトユーザーを取得または作成
default_user, _ = User.objects.get_or_create(
    username='admin',
    defaults={'is_staff': True, 'is_superuser': True}
)

# 1. Clientデータを復元
print("=== Clientデータ復元開始 ===")
try:
    with open('clients_backup.json', 'r', encoding='utf-8-sig') as f:
        client_data = json.load(f)
except UnicodeDecodeError:
    with open('clients_backup.json', 'r', encoding='cp932') as f:
        client_data = json.load(f)

# insurance_number → 新しいid のマッピング
insurance_to_id = {}

for item in client_data:
    fields = item['fields']
    insurance_number = item['pk']  # 旧PKはinsurance_number

    # 新しいClientオブジェクトを作成（idは自動採番される）
    client = Client.objects.create(
        insurance_number=insurance_number,
        name=fields['name'],
        furigana=fields['furigana'],
        birth_date=fields['birth_date'],
        gender=fields['gender'],
        phone=fields.get('phone', ''),
        address=fields.get('address', ''),
        care_level=fields.get('care_level', ''),
        certification_date=fields.get('certification_date'),
        certification_period_start=fields.get('certification_period_start'),
        certification_period_end=fields.get('certification_period_end'),
        care_burden=fields.get('care_burden', ''),
        burden_period_start=fields.get('burden_period_start'),
        burden_period_end=fields.get('burden_period_end'),
        medical_insurance_type=fields.get('medical_insurance_type', ''),
        medical_insurer_name_issuer=fields.get('medical_insurer_name_issuer', ''),
        medical_insurer_number=fields.get('medical_insurer_number', ''),
        medical_insurance_symbol=fields.get('medical_insurance_symbol', ''),
        medical_insurance_number=fields.get('medical_insurance_number', ''),
        family_name1=fields.get('family_name1', ''),
        family_relationship1=fields.get('family_relationship1', ''),
        family_address1=fields.get('family_address1', ''),
        family_living_status1=fields.get('family_living_status1', ''),
        family_care_status1=fields.get('family_care_status1', ''),
        family_employment1=fields.get('family_employment1', ''),
        family_contact1=fields.get('family_contact1', ''),
        family_notes1=fields.get('family_notes1', ''),
        family_name2=fields.get('family_name2', ''),
        family_relationship2=fields.get('family_relationship2', ''),
        family_address2=fields.get('family_address2', ''),
        family_living_status2=fields.get('family_living_status2', ''),
        family_care_status2=fields.get('family_care_status2', ''),
        family_employment2=fields.get('family_employment2', ''),
        family_contact2=fields.get('family_contact2', ''),
        family_notes2=fields.get('family_notes2', ''),
        created_by=User.objects.filter(id=fields.get('created_by')).first() or default_user,
    )

    # マッピングを保存
    insurance_to_id[insurance_number] = client.id
    print(f"復元: {client.name} (insurance_number={insurance_number} → id={client.id})")

print(f"\n[OK] {len(client_data)}件のClient復元完了")
print(f"マッピング: {insurance_to_id}\n")

# 2. Assessmentデータを復元
print("=== Assessmentデータ復元開始 ===")
try:
    with open('assessments_backup.json', 'r', encoding='utf-8-sig') as f:
        assessment_data = json.load(f)
except UnicodeDecodeError:
    with open('assessments_backup.json', 'r', encoding='cp932') as f:
        assessment_data = json.load(f)

for item in assessment_data:
    fields = item['fields']
    old_client_id = fields['client']  # 旧insurance_number

    # 新しいidに変換
    if old_client_id in insurance_to_id:
        new_client_id = insurance_to_id[old_client_id]

        # Assessmentを作成
        assessment = Assessment.objects.create(
            client_id=new_client_id,
            assessment_date=fields['assessment_date'],
            assessor_id=fields.get('assessor'),
            assessment_type=fields['assessment_type'],
            assessment_type_other=fields.get('assessment_type_other'),
            interview_location=fields['interview_location'],
            interview_location_other=fields.get('interview_location_other'),
            status=fields.get('status', 'draft'),
            # その他のフィールド...
        )
        print(f"復元: Assessment #{assessment.id} (client={old_client_id} → {new_client_id})")
    else:
        print(f"警告: client_id={old_client_id} が見つかりません（スキップ）")

print(f"\n[OK] Assessmentデータ復元完了\n")

# 3. その他の関連データ
print("=== 関連データ復元開始 ===")
try:
    with open('clients_related_backup.json', 'r', encoding='utf-8-sig') as f:
        related_data = json.load(f)
except UnicodeDecodeError:
    with open('clients_related_backup.json', 'r', encoding='cp932') as f:
        related_data = json.load(f)

for item in related_data:
    model_name = item['model']
    fields = item['fields']

    # clientフィールドを持つモデルの場合、IDを変換
    if 'client' in fields:
        old_client_id = fields['client']
        if old_client_id in insurance_to_id:
            fields['client'] = insurance_to_id[old_client_id]
            print(f"変換: {model_name} (client={old_client_id} → {fields['client']})")

# 関連データをloaddata経由で復元（変換済み）
with open('clients_related_converted.json', 'w', encoding='utf-8') as f:
    json.dump(related_data, f, ensure_ascii=False, indent=2)

print("\n[OK] 関連データファイルを変換しました (clients_related_converted.json)")
print("\n完了！次のコマンドで関連データをインポートしてください：")
print("python manage.py loaddata clients_related_converted.json")
