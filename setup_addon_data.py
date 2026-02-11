#!/usr/bin/env python
"""
事業所と加算の初期データ設定スクリプト
"""

import os
import sys
import django
from decimal import Decimal

# Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'care_management.settings')
django.setup()

from clients.models import ServiceProvider, ServiceAddOn, ProviderAddOnSetting

def setup_addon_data():
    """事業所と加算の初期データを設定"""
    
    # 事業所データ作成
    print("=== 事業所データ作成 ===")
    providers = [
        {"name": "あさひデイサービスセンター", "service_category": "day_service"},
        {"name": "みんなのヘルパーステーション", "service_category": "home_helper"},
        {"name": "やすらぎ訪問看護ステーション", "service_category": "visiting_nurse"},
        {"name": "いきいき福祉用具センター", "service_category": "welfare_equipment"},
    ]
    
    created_providers = {}
    for provider_data in providers:
        provider, created = ServiceProvider.objects.get_or_create(
            name=provider_data['name'],
            defaults=provider_data
        )
        created_providers[provider_data['service_category']] = provider
        status = "作成" if created else "既存"
        print(f"{status}: {provider.name}")
    
    # 加算データ作成
    print("\n=== 加算データ作成 ===")
    addons = [
        # デイサービス用加算
        {"name": "機能訓練加算Ⅰ", "addon_type": "functional_training", "units": Decimal("12"), "description": "機能訓練指導員による個別機能訓練"},
        {"name": "機能訓練加算Ⅱ", "addon_type": "functional_training", "units": Decimal("20"), "description": "理学療法士等による個別機能訓練"},
        {"name": "入浴加算", "addon_type": "bathing", "units": Decimal("40"), "description": "入浴介助の提供"},
        {"name": "認知症対応型共同生活介護費", "addon_type": "dementia", "units": Decimal("60"), "description": "認知症利用者への専門的ケア"},
        {"name": "栄養改善加算", "addon_type": "nutrition", "units": Decimal("200"), "description": "管理栄養士による栄養ケア"},
        {"name": "口腔機能向上加算", "addon_type": "oral_care", "units": Decimal("150"), "description": "言語聴覚士等による口腔機能訓練"},
        {"name": "送迎減算", "addon_type": "transportation", "units": Decimal("47"), "is_addition": False, "description": "送迎を行わない場合の減算"},
        {"name": "大規模型減算Ⅰ", "addon_type": "large_scale", "units": Decimal("15"), "is_addition": False, "description": "利用定員51人以上75人以下の場合"},
        {"name": "大規模型減算Ⅱ", "addon_type": "large_scale", "units": Decimal("25"), "is_addition": False, "description": "利用定員76人以上の場合"},
    ]
    
    created_addons = []
    for addon_data in addons:
        addon, created = ServiceAddOn.objects.get_or_create(
            name=addon_data['name'],
            defaults=addon_data
        )
        created_addons.append(addon)
        status = "作成" if created else "既存"
        sign = "+" if addon.is_addition else "-"
        print(f"{status}: {addon.name} ({sign}{addon.units}単位)")
    
    # デイサービス事業所に加算を設定
    print(f"\n=== デイサービス事業所加算設定 ===")
    day_service_provider = created_providers.get('day_service')
    if day_service_provider:
        # デイサービスで使用する加算のみ有効にする
        day_service_addons = [
            'functional_training',  # 機能訓練加算
            'bathing',              # 入浴加算
            'dementia',            # 認知症加算
            'nutrition',           # 栄養改善加算
            'oral_care',           # 口腔機能向上加算
        ]
        
        for addon in created_addons:
            if addon.addon_type in day_service_addons:
                setting, created = ProviderAddOnSetting.objects.get_or_create(
                    provider=day_service_provider,
                    addon=addon,
                    defaults={'is_enabled': True}
                )
                status = "設定" if created else "既存"
                print(f"{status}: {day_service_provider.name} - {addon.name}")
    
    print(f"\n=== セットアップ完了 ===")
    print(f"事業所: {ServiceProvider.objects.count()}件")
    print(f"加算種別: {ServiceAddOn.objects.count()}件")
    print(f"事業所別加算設定: {ProviderAddOnSetting.objects.count()}件")

if __name__ == "__main__":
    setup_addon_data()