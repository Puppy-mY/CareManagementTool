#!/usr/bin/env python
"""
階層化されたサービス種別データの更新スクリプト
"""

import os
import sys
import django
from decimal import Decimal

# Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'care_management.settings')
django.setup()

from clients.models import ServiceType

def update_service_types():
    """サービス種別を階層化されたデータに更新"""
    
    # 既存データをクリア
    ServiceType.objects.all().delete()
    
    # デイサービスカテゴリのサービス
    day_services = [
        {"name": "通所介護（1時間以上2時間未満）", "category": "day_service", "duration_minutes": 90, "unit_per_minute": Decimal("4.2"), "total_units": Decimal("378")},
        {"name": "通所介護（2時間以上3時間未満）", "category": "day_service", "duration_minutes": 150, "unit_per_minute": Decimal("2.8"), "total_units": Decimal("420")},
        {"name": "通所介護（3時間以上4時間未満）", "category": "day_service", "duration_minutes": 210, "unit_per_minute": Decimal("3.1"), "total_units": Decimal("651")},
        {"name": "通所介護（4時間以上5時間未満）", "category": "day_service", "duration_minutes": 270, "unit_per_minute": Decimal("2.4"), "total_units": Decimal("648")},
        {"name": "通所介護（5時間以上6時間未満）", "category": "day_service", "duration_minutes": 330, "unit_per_minute": Decimal("2.3"), "total_units": Decimal("759")},
        {"name": "通所介護（6時間以上7時間未満）", "category": "day_service", "duration_minutes": 390, "unit_per_minute": Decimal("2.1"), "total_units": Decimal("819")},
        {"name": "通所介護（7時間以上8時間未満）", "category": "day_service", "duration_minutes": 450, "unit_per_minute": Decimal("2.0"), "total_units": Decimal("900")},
        {"name": "通所介護（8時間以上9時間未満）", "category": "day_service", "duration_minutes": 510, "unit_per_minute": Decimal("1.8"), "total_units": Decimal("918")},
    ]
    
    # ヘルパーサービス
    helper_services = [
        {"name": "身体介護1（20分）", "category": "home_helper", "duration_minutes": 20, "unit_per_minute": Decimal("8.3"), "total_units": Decimal("166")},
        {"name": "身体介護1（30分）", "category": "home_helper", "duration_minutes": 30, "unit_per_minute": Decimal("8.3"), "total_units": Decimal("249")},
        {"name": "身体介護1（45分）", "category": "home_helper", "duration_minutes": 45, "unit_per_minute": Decimal("7.4"), "total_units": Decimal("333")},
        {"name": "身体介護1（60分）", "category": "home_helper", "duration_minutes": 60, "unit_per_minute": Decimal("6.8"), "total_units": Decimal("408")},
        {"name": "身体介護1（90分）", "category": "home_helper", "duration_minutes": 90, "unit_per_minute": Decimal("6.0"), "total_units": Decimal("540")},
        {"name": "生活援助1（20分）", "category": "home_helper", "duration_minutes": 20, "unit_per_minute": Decimal("5.5"), "total_units": Decimal("110")},
        {"name": "生活援助1（30分）", "category": "home_helper", "duration_minutes": 30, "unit_per_minute": Decimal("5.5"), "total_units": Decimal("165")},
        {"name": "生活援助2（45分）", "category": "home_helper", "duration_minutes": 45, "unit_per_minute": Decimal("4.9"), "total_units": Decimal("220")},
        {"name": "生活援助2（60分）", "category": "home_helper", "duration_minutes": 60, "unit_per_minute": Decimal("4.5"), "total_units": Decimal("270")},
        {"name": "生活援助2（90分）", "category": "home_helper", "duration_minutes": 90, "unit_per_minute": Decimal("3.8"), "total_units": Decimal("342")},
    ]
    
    # 訪問看護サービス
    visiting_nurse_services = [
        {"name": "訪問看護（20分未満）", "category": "visiting_nurse", "duration_minutes": 15, "unit_per_minute": Decimal("20.0"), "total_units": Decimal("300")},
        {"name": "訪問看護（30分未満）", "category": "visiting_nurse", "duration_minutes": 25, "unit_per_minute": Decimal("16.0"), "total_units": Decimal("400")},
        {"name": "訪問看護（30分以上）", "category": "visiting_nurse", "duration_minutes": 40, "unit_per_minute": Decimal("13.8"), "total_units": Decimal("552")},
        {"name": "訪問看護（90分以上）", "category": "visiting_nurse", "duration_minutes": 100, "unit_per_minute": Decimal("8.0"), "total_units": Decimal("800")},
    ]
    
    # 福祉用具サービス
    welfare_equipment_services = [
        {"name": "福祉用具貸与（手すり）", "category": "welfare_equipment", "duration_minutes": None, "unit_per_minute": Decimal("0"), "total_units": Decimal("100")},
        {"name": "福祉用具貸与（歩行器）", "category": "welfare_equipment", "duration_minutes": None, "unit_per_minute": Decimal("0"), "total_units": Decimal("200")},
        {"name": "福祉用具貸与（車いす）", "category": "welfare_equipment", "duration_minutes": None, "unit_per_minute": Decimal("0"), "total_units": Decimal("300")},
        {"name": "福祉用具貸与（特殊寝台）", "category": "welfare_equipment", "duration_minutes": None, "unit_per_minute": Decimal("0"), "total_units": Decimal("400")},
        {"name": "福祉用具貸与（床ずれ防止用具）", "category": "welfare_equipment", "duration_minutes": None, "unit_per_minute": Decimal("0"), "total_units": Decimal("150")},
        {"name": "福祉用具貸与（体位変換器）", "category": "welfare_equipment", "duration_minutes": None, "unit_per_minute": Decimal("0"), "total_units": Decimal("120")},
    ]
    
    # その他のサービス
    other_services = [
        {"name": "居宅療養管理指導（医師）", "category": "other", "duration_minutes": 30, "unit_per_minute": Decimal("16.7"), "total_units": Decimal("501")},
        {"name": "居宅療養管理指導（薬剤師）", "category": "other", "duration_minutes": 20, "unit_per_minute": Decimal("11.5"), "total_units": Decimal("230")},
        {"name": "短期入所生活介護（1日）", "category": "other", "duration_minutes": 1440, "unit_per_minute": Decimal("0.4"), "total_units": Decimal("576")},
    ]
    
    # 全サービスを登録
    all_services = day_services + helper_services + visiting_nurse_services + welfare_equipment_services + other_services
    
    created_count = 0
    for service_data in all_services:
        service = ServiceType.objects.create(**service_data)
        created_count += 1
        print(f"作成: {service.get_category_display()} - {service.name}")
    
    print(f"\n合計 {created_count} 件のサービス種別を作成しました。")

if __name__ == "__main__":
    update_service_types()