#!/usr/bin/env python
import os
import sys
import django
from datetime import date

# Django設定
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'care_management.settings')
django.setup()

from clients.models import Client
from assessments.models import Assessment
from django.contrib.auth.models import User

def create_sample_assessment():
    # 青木節子さんのクライアント情報を取得
    try:
        client = Client.objects.get(insurance_number='9900112233')
        print(f"クライアント見つかりました: {client.name}")
    except Client.DoesNotExist:
        print("青木節子さんが見つかりません")
        return

    # 管理者ユーザーを取得（作成者として使用）
    try:
        user = User.objects.first()
        print(f"作成者: {user.username}")
    except:
        print("ユーザーが見つかりません")
        return

    # アセスメント作成
    assessment = Assessment.objects.create(
        client=client,
        assessment_date=date.today(),
        assessor=user,
        assessment_type='new',
        interview_location='home',

        # 基本情報
        basic_info={
            'life_history': '元教員として40年間勤務。退職後は書道教室を開いていた。3年前に夫を亡くし、現在は長女と二人暮らし。',
            'personal_hopes': '自宅で生活を続けたい。できるだけ自分でできることは続けていきたい。',
            'family_hopes': '母の意思を尊重し、安全に自宅で過ごしてもらいたい。必要な支援は受けてもらいたい。'
        },

        # 保険情報
        insurance_info={
            'care_level': 'B1',
            'dementia_level': 'IIa',
            'burden_ratio': '1',
            'medical_insurance': '後期高齢者医療',
            'disability_handbook': True,
            'difficulty_certificate': False,
            'life_protection': False
        },

        # 家族状況
        family_situation={
            'family_member1': '青木花子（長女・55歳）',
            'family_member2': '青木太郎（長男・52歳）'
        },

        # 居住状況
        living_situation={
            'household_type': 'family_together',
            'housing_type': 'detached',
            'housing_rights': 'owned',
            'has_private_room': True,
            'has_cooling': True,
            'toilet_type': 'western',
            'has_bath': True,
            'bedding_type': 'bed',
            'has_stairs': False,
            'home_renovation_needed': True,
            'home_renovation_necessity': True
        },

        # サービス利用状況
        services={
            'services': ['home_care', 'facility_care'],
            'welfare_equipment': ['walking_aid', 'special_bed'],
            'other_services': '配食サービス週3回利用',
            'informal_services': '近所の方による買い物支援',
            'social_relationships': '町内会活動、老人会への参加'
        },

        # 健康状態
        health_status={
            'disease_1': '高血圧症',
            'disease_2': '変形性膝関節症',
            'disease_3': '白内障',
            'medical_history': '胆石手術歴あり（10年前）',
            'main_doctor': '田中内科クリニック　田中一郎医師',
            'outpatient_clinic': '市立病院整形外科',
            'medication': '降圧剤、膝関節痛軟膏',
            'hospital': '月1回通院',
            'medication_details': 'アムロジピン5mg 1日1回朝食後、ロキソニンテープ貼付',
            'allergies': False
        },

        # 身体状況
        physical_status={
            'skin_condition': ['none'],
            'infection_status': ['none'],
            'special_treatment': ['none'],
            'pain_location': '両膝関節に軽度の疼痛あり',
            'pain_existence': '歩行時に軽度の疼痛',
            'height': '152',
            'weight': '48',
            'vision': 'large_letters_ok',
            'hearing': 'normal',
            'physical_notes': '全体的に活動的で、軽度の膝痛はあるが日常生活に大きな支障なし'
        },

        # 認知機能
        cognitive_function={
            'dementia_presence': 'yes',
            'dementia_details': '軽度認知症、時間の見当識に軽度の障害あり',
            'bpsd_presence': 'no',
            'bpsd_symptoms': ['none'],
            'conversation': 'possible',
            'communication': 'possible',
            'cognitive_notes': '日常会話は問題なし、複雑な話は理解に時間がかかる場合あり'
        },

        # 基本動作
        basic_activities={
            'turning_over': 'no_assistance',
            'getting_up': 'with_assistance',
            'sitting': 'can_do',
            'standing_up': 'with_assistance',
            'standing': 'with_something',
            'transfer': 'supervision',
            'indoor_mobility': 'supervision',
            'outdoor_mobility': 'partial_assistance',
            'basic_activity_notes': '屋内移動は概ね自立、屋外は見守りが必要'
        },

        # ADL
        adl={
            'eating_method': 'oral',
            'eating_assistance': 'independent',
            'swallowing': 'can_do',
            'meal_form_main': 'normal',
            'meal_form_side': 'normal',
            'water_thickening': False,
            'eating_restriction': 'none',
            'eating_utensils': ['chopsticks', 'spoon'],
            'eating_notes': '食事は自立、好き嫌いは特になし',
            'oral_hygiene_assistance': 'independent',
            'denture_presence': True,
            'tooth_decay': False,
            'oral_notes': '上下義歯使用、口腔状態良好',
            'bathing_assistance': 'partial_assistance',
            'bathing_form': 'regular_bath',
            'bathing_restriction': False,
            'dressing_upper': 'independent',
            'dressing_lower': 'supervision',
            'bathing_notes': '入浴は一部介助、更衣は概ね自立',
            'excretion_assistance': 'independent',
            'urination': True,
            'urinary_incontinence': False,
            'defecation': True,
            'fecal_incontinence': False,
            'daytime_location': ['toilet'],
            'nighttime_location': ['portable_toilet'],
            'excretion_supplies': [],
            'excretion_notes': '排泄は自立、夜間のみポータブルトイレ使用'
        },

        # IADL
        iadl={
            'cooking': 'partial_assistance',
            'cleaning': 'partial_assistance',
            'washing': 'supervision',
            'shopping': 'full_assistance',
            'money_management': 'supervision',
            'iadl_notes': '簡単な調理は可能、重い物の移動は困難、買い物は同行が必要'
        }
    )

    print(f"アセスメント作成完了: ID {assessment.id}")
    return assessment

if __name__ == '__main__':
    create_sample_assessment()