#!/usr/bin/env python
import os
import sys
import django
from datetime import date

# Django設定
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'care_management.settings')
django.setup()

from assessments.forms import DetailedAssessmentForm

def test_all_form_choices():
    """全ての選択肢フィールドをテストするためのダミーデータ"""

    # 全ての選択肢の最初の有効な値を取得
    test_data = {
        # 基本情報
        'life_history': 'テスト生活歴',
        'personal_hopes': 'テスト本人希望',
        'family_hopes': 'テスト家族希望',

        # 保険情報
        'care_level': 'independent',  # 最初の有効な値
        'dementia_level': 'independent',  # 最初の有効な値
        'burden_ratio': '1',  # 最初の有効な値
        'medical_insurance': 'テスト医療保険',
        'disability_handbook': False,
        'difficulty_certificate': False,
        'life_protection': False,

        # 家族状況
        'family_member1': 'テスト家族1',
        'family_member2': 'テスト家族2',

        # 居住状況
        'household_type': 'family_together',
        'housing_type': 'detached',
        'housing_rights': 'owned',
        'has_private_room': True,
        'has_cooling': True,
        'toilet_type': 'western',
        'has_bath': True,
        'bedding_type': 'futon',
        'has_stairs': False,
        'home_renovation_needed': False,
        'home_renovation_necessity': False,

        # サービス利用状況
        'services': ['home_care'],
        'welfare_equipment': ['wheelchair'],
        'other_services': 'テストその他サービス',
        'informal_services': 'テストインフォーマル',
        'social_relationships': 'テスト社会関係',

        # 健康状態
        'disease_1': 'テスト疾患1',
        'disease_2': 'テスト疾患2',
        'disease_3': 'テスト疾患3',
        'medical_history': 'テスト既往歴',
        'main_doctor': 'テスト主治医',
        'outpatient_clinic': 'テスト往診医',
        'medication': 'テストかかりつけ医',
        'hospital': 'テスト通院',
        'medication_details': 'テスト服薬',
        'allergies': False,

        # 身体状況
        'skin_condition': ['none'],
        'infection_status': ['none'],
        'special_treatment': ['none'],
        'pain_location': 'テスト痛み部位',
        'pain_existence': 'テスト痛み有無',
        'height': 160.0,
        'weight': 50.0,
        'vision': 'normal',
        'hearing': 'normal',
        'physical_notes': 'テスト身体特記',

        # 認知機能
        'dementia_symptoms': False,
        'bpsd_symptoms': ['none'],
        'conversation': 'possible',
        'communication': 'possible',
        'cognitive_notes': 'テスト認知特記',

        # 基本動作
        'turning_over': 'no_assistance',
        'getting_up': 'no_assistance',
        'sitting': 'can_do',
        'standing_up': 'no_assistance',
        'standing': 'no_support',
        'transfer': 'independent',
        'indoor_mobility': 'independent',
        'outdoor_mobility': 'independent',
        'basic_activity_notes': 'テスト基本動作特記',

        # ADL（食事）
        'eating_method': 'oral',
        'eating_assistance': 'independent',
        'swallowing': 'can_do',
        'meal_form_main': 'normal',
        'meal_form_side': 'normal',
        'water_thickening': False,
        'eating_restriction': 'none',
        'eating_utensils': ['chopsticks'],
        'eating_notes': 'テスト食事特記',

        # ADL（口腔）
        'oral_hygiene_assistance': 'independent',
        'natural_teeth_presence': True,
        'denture_presence': False,
        'denture_location': [],
        'oral_notes': 'テスト口腔特記',

        # ADL（入浴・更衣）
        'bathing_assistance': 'independent',
        'bathing_form': 'regular_bath',
        'bathing_restriction': False,
        'dressing_upper': 'independent',
        'dressing_lower': 'independent',
        'bathing_notes': 'テスト入浴特記',

        # ADL（排泄）
        'excretion_assistance': 'independent',
        'urination': True,
        'urinary_incontinence': False,
        'defecation': True,
        'fecal_incontinence': False,
        'daytime_location': ['toilet'],
        'nighttime_location': ['toilet'],
        'excretion_supplies': [],
        'excretion_notes': 'テスト排泄特記',

        # IADL
        'cooking': 'independent',
        'cleaning': 'independent',
        'washing': 'independent',
        'shopping': 'independent',
        'money_management': 'independent',
        'iadl_notes': 'テストIADL特記',

        # 認知機能（詳細）
        'dementia_presence': 'none',
        'dementia_details': 'テスト認知症詳細',
        'bpsd_presence': 'none',
        'bpsd_symptoms': ['none'],
    }

    # フォームをテスト
    form = DetailedAssessmentForm(test_data)

    print("=== フォームバリデーションテスト ===")
    print(f"フォームの有効性: {form.is_valid()}")

    if not form.is_valid():
        print("\n=== バリデーションエラー ===")
        for field, errors in form.errors.items():
            print(f"フィールド '{field}': {errors}")

        print("\n=== フィールドと選択肢の詳細確認 ===")
        for field_name, field in form.fields.items():
            if hasattr(field, 'choices') and field.choices:
                print(f"\n{field_name}:")
                print(f"  ラベル: {field.label}")
                print(f"  選択肢: {field.choices}")
                if field_name in form.errors:
                    print(f"  エラー: {form.errors[field_name]}")
    else:
        print("すべてのフィールドでバリデーションが成功しました！")

    return form.is_valid(), form.errors

if __name__ == '__main__':
    test_all_form_choices()