#!/usr/bin/env python
"""
初期データを作成するスクリプト
サービス種別の基本的な項目を登録します。
"""
import os
import sys
import django

# Django設定の初期化
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'care_management.settings')
django.setup()

from clients.models import ServiceType

def create_service_types():
    """サービス種別の初期データを作成"""
    service_types = [
        # 訪問介護
        {"name": "身体介護", "unit_per_minute": 4.0},
        {"name": "生活援助", "unit_per_minute": 2.3},
        {"name": "通院等乗降介助", "unit_per_minute": 1.0},
        
        # 訪問看護
        {"name": "訪問看護（30分未満）", "unit_per_minute": 15.5},
        {"name": "訪問看護（30分以上1時間未満）", "unit_per_minute": 11.8},
        {"name": "訪問看護（1時間以上1時間30分未満）", "unit_per_minute": 8.2},
        
        # 通所介護（デイサービス）
        {"name": "通所介護（3-4時間）", "unit_per_minute": 7.5},
        {"name": "通所介護（4-5時間）", "unit_per_minute": 7.9},
        {"name": "通所介護（5-7時間）", "unit_per_minute": 9.4},
        {"name": "通所介護（7-9時間）", "unit_per_minute": 10.6},
        
        # 訪問リハビリテーション
        {"name": "訪問リハビリ（1単位20分）", "unit_per_minute": 15.7},
        
        # 福祉用具貸与
        {"name": "福祉用具貸与", "unit_per_minute": 0.1},
        
        # その他
        {"name": "その他サービス", "unit_per_minute": 1.0},
    ]
    
    created_count = 0
    for service_data in service_types:
        service_type, created = ServiceType.objects.get_or_create(
            name=service_data["name"],
            defaults={
                "unit_per_minute": service_data["unit_per_minute"],
                "is_active": True
            }
        )
        if created:
            created_count += 1
            print(f"OK {service_type.name} を作成しました")
        else:
            print(f"-- {service_type.name} は既に存在します")
    
    print(f"\n合計 {created_count} 件のサービス種別を作成しました。")
    return created_count

def main():
    print("=== 初期データの作成を開始します ===")
    print()
    
    try:
        # サービス種別の作成
        print("1. サービス種別の作成...")
        create_service_types()
        
        print()
        print("=== 初期データの作成が完了しました ===")
        
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()