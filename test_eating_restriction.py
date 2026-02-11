#!/usr/bin/env python
import os
import sys
import django

# Django設定
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'care_management.settings')
django.setup()

from assessments.forms import DetailedAssessmentForm

def test_eating_restriction():
    """食事制限フィールドの各選択肢をテスト"""

    # 基本データ（最小限）
    base_data = {
        'care_level': 'independent',
        'dementia_level': 'independent',
        'burden_ratio': '1',
    }

    # 各選択肢をテスト
    eating_restriction_values = ['', 'yes', 'none', 'unknown']

    for value in eating_restriction_values:
        test_data = base_data.copy()
        test_data['eating_restriction'] = value

        form = DetailedAssessmentForm(test_data)

        print(f"eating_restriction = '{value}':")
        print(f"  フォーム有効性: {form.is_valid()}")

        if not form.is_valid():
            if 'eating_restriction' in form.errors:
                print(f"  エラー: {form.errors['eating_restriction']}")
            else:
                print(f"  その他のエラー: {form.errors}")
        print()

    # フォームの選択肢を確認
    eating_restriction_field = form.fields['eating_restriction']
    print("eating_restriction フィールドの選択肢:")
    for choice in eating_restriction_field.choices:
        print(f"  '{choice[0]}' -> '{choice[1]}'")

if __name__ == '__main__':
    test_eating_restriction()