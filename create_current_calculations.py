#!/usr/bin/env python
"""
既存利用者の当月限度額試算を作成するスクリプト
"""
import os
import sys
import django
from datetime import datetime

# Django設定の初期化
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'care_management.settings')
django.setup()

from clients.models import Client, LimitCalculation

def create_current_month_calculations():
    """既存利用者の当月限度額試算を作成"""
    now = datetime.now()
    created_count = 0
    
    # 要介護度が設定されている利用者のみ対象
    clients = Client.objects.filter(care_level__isnull=False)
    
    for client in clients:
        calculation, created = LimitCalculation.objects.get_or_create(
            client=client,
            year=now.year,
            month=now.month,
            defaults={'care_manager_units': 0}
        )
        
        if created:
            created_count += 1
            print(f"OK {client.name}さんの{now.year}年{now.month}月試算を作成")
        else:
            print(f"-- {client.name}さんの試算は既に存在")
    
    print(f"\n合計 {created_count} 件の限度額試算を作成しました。")
    return created_count

def main():
    print("=== 既存利用者の当月限度額試算作成 ===")
    print()
    
    try:
        create_current_month_calculations()
        print("\n=== 処理が完了しました ===")
        
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()