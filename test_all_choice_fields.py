#!/usr/bin/env python
import os
import sys
import django

# Django設定
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'care_management.settings')
django.setup()

from assessments.forms import DetailedAssessmentForm

def test_all_choice_fields():
    """全ての選択肢フィールドを個別にテスト"""

    # 最小限のベースデータ
    base_data = {
        'care_level': 'independent',
        'dementia_level': 'independent',
        'burden_ratio': '1',
    }

    # 選択肢フィールドとテスト値
    choice_field_tests = {
        'eating_restriction': 'none',
        'household_type': 'family_together',
        'housing_type': 'apartment_complex',
        'housing_rights': 'owned',
        'toilet_type': 'western',
        'bedding_type': 'futon',
        'vision': 'normal',
        'hearing': 'poor',
        'conversation': 'possible',
        'communication': 'possible',
        'turning_over': 'no_assistance',
        'getting_up': 'no_assistance',
        'sitting': 'can_do',
        'standing_up': 'no_assistance',
        'standing': 'no_support',
        'transfer': 'independent',
        'indoor_mobility': 'independent',
        'outdoor_mobility': 'independent',
        'eating_method': 'oral',
        'eating_assistance': 'independent',
        'swallowing': 'can_do',
        'meal_form_main': 'normal',
        'meal_form_side': 'normal',
        'oral_hygiene_assistance': 'independent',
        'bathing_assistance': 'independent',
        'bathing_form': 'regular_bath',
        'dressing_upper': 'independent',
        'dressing_lower': 'independent',
        'excretion_assistance': 'independent',
        'cooking': 'independent',
        'cleaning': 'independent',
        'washing': 'independent',
        'shopping': 'independent',
        'money_management': 'independent',
        'dementia_presence': 'no',
        'bpsd_presence': 'no',
    }

    failed_fields = []

    for field_name, test_value in choice_field_tests.items():
        test_data = base_data.copy()
        test_data[field_name] = test_value

        form = DetailedAssessmentForm(test_data)

        if not form.is_valid():
            if field_name in form.errors:
                print(f"NG {field_name} = '{test_value}': {form.errors[field_name]}")
                failed_fields.append(field_name)
            else:
                # 他のフィールドエラーがある場合はこのフィールドは問題ない
                continue
        else:
            print(f"OK {field_name} = '{test_value}': OK")

    print(f"\n=== 結果 ===")
    print(f"テスト対象フィールド: {len(choice_field_tests)}")
    print(f"失敗したフィールド: {len(failed_fields)}")

    if failed_fields:
        print(f"失敗フィールド: {', '.join(failed_fields)}")

        # 失敗したフィールドの選択肢を表示
        form = DetailedAssessmentForm()
        for field_name in failed_fields:
            if hasattr(form.fields[field_name], 'choices'):
                print(f"\n{field_name} の選択肢:")
                for choice in form.fields[field_name].choices:
                    print(f"  '{choice[0]}' -> '{choice[1]}'")

if __name__ == '__main__':
    test_all_choice_fields()