from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from datetime import date
import json
import os
from .models import Assessment
from clients.models import Client
from .forms import DetailedAssessmentForm

# openpyxlの利用可能性チェック
try:
    from openpyxl import load_workbook
    from openpyxl.cell.cell import MergedCell
    OPENPYXL_AVAILABLE = True
except ImportError:
    OPENPYXL_AVAILABLE = False


@login_required
def assessment_list(request):
    # 全アセスメントを取得（クライアントサイドでフィルタリング）
    assessments = Assessment.objects.select_related('client', 'assessor').order_by('-assessment_date')

    # 作成者一覧を取得（アセスメントを作成したことがあるユーザーのみ）
    all_assessors = User.objects.filter(
        id__in=Assessment.objects.values_list('assessor_id', flat=True).distinct()
    ).order_by('username')

    context = {
        'assessments': assessments,
        'all_assessors': all_assessors,
    }

    return render(request, 'assessments/assessment_list.html', context)


@login_required
def assessment_detail(request, pk):
    assessment = get_object_or_404(Assessment, pk=pk)

    # 同じ利用者の他のアセスメント履歴を取得
    assessment_history = Assessment.objects.filter(
        client=assessment.client
    ).exclude(pk=pk).order_by('-assessment_date')

    context = {
        'assessment': assessment,
        'assessment_history': assessment_history,
    }

    return render(request, 'assessments/assessment_detail.html', context)



@login_required
def assessment_edit(request, pk):
    assessment = get_object_or_404(Assessment, pk=pk)

    if request.method == 'POST':
        form = DetailedAssessmentForm(request.POST)

        if form.is_valid():
            # actionパラメータを取得
            action = request.POST.get('action', 'save')

            # 詳細データをJSONフィールドに保存
            detailed_data = {}

            # 各セクションのデータを整理
            detailed_data['basic_info'] = {
                'life_history': form.cleaned_data.get('life_history', ''),
                'personal_hopes': form.cleaned_data.get('personal_hopes', ''),
                'family_hopes': form.cleaned_data.get('family_hopes', ''),
                'special_situation_status': request.POST.get('special_situation_status', ''),
                'special_situation': request.POST.getlist('special_situation'),
                'special_situation_other': request.POST.get('special_situation_other', ''),
            }

            detailed_data['insurance_info'] = {
                'care_level': form.cleaned_data.get('care_level', ''),
                'dementia_level': form.cleaned_data.get('dementia_level', ''),
                'burden_ratio': form.cleaned_data.get('burden_ratio', ''),
                'medical_insurance': form.cleaned_data.get('medical_insurance', ''),
                'disability_handbook': form.cleaned_data.get('disability_handbook', False),
                'difficulty_certificate': form.cleaned_data.get('difficulty_certificate', False),
                'life_protection': form.cleaned_data.get('life_protection', False),
            }

            detailed_data['family_situation'] = {
                'family_member1': form.cleaned_data.get('family_member1', ''),
                'family_member2': form.cleaned_data.get('family_member2', ''),
            }

            detailed_data['living_situation'] = {
                'home_environment': request.POST.get('home_environment', ''),
                'other_home_environment_detail_text': request.POST.get('other_home_environment_detail_text', ''),
                'housing_type': request.POST.get('housing_type', ''),
                'other_housing_type_detail_text': request.POST.get('other_housing_type_detail_text', ''),
                'has_elevator': request.POST.get('has_elevator', ''),
                'housing_ownership': request.POST.get('housing_ownership', ''),
                'other_ownership_detail_text': request.POST.get('other_ownership_detail_text', ''),
                'private_room': request.POST.get('private_room', ''),
                'air_conditioning': request.POST.get('air_conditioning', ''),
                'toilet_type': request.POST.get('toilet_type', ''),
                'toilet_handrail': request.POST.get('toilet_handrail', ''),
                'toilet_step': request.POST.get('toilet_step', ''),
                'bathroom': request.POST.get('bathroom', ''),
                'bathroom_handrail': request.POST.get('bathroom_handrail', ''),
                'bathroom_step': request.POST.get('bathroom_step', ''),
                'sleeping_arrangement': request.POST.get('sleeping_arrangement', ''),
                'other_sleeping_detail_text': request.POST.get('other_sleeping_detail_text', ''),
                'room_level_difference': request.POST.get('room_level_difference', ''),
                'housing_modification': request.POST.get('housing_modification', ''),
                'housing_modification_need': request.POST.get('housing_modification_need', ''),
                'housing_notes': request.POST.get('housing_notes', ''),
            }

            detailed_data['services'] = {
                'care_services': form.cleaned_data.get('care_services', []),
                'welfare_equipment': form.cleaned_data.get('welfare_equipment', []),
                'other_services': form.cleaned_data.get('other_services', ''),
                'informal_services': form.cleaned_data.get('informal_services', []),
                'other_services_detail_text': form.cleaned_data.get('other_services_detail_text', ''),
                'social_relationships': form.cleaned_data.get('social_relationships', ''),
            }

            detailed_data['health_status'] = {
                'disease_1': form.cleaned_data.get('disease_1', ''),
                'disease_2': form.cleaned_data.get('disease_2', ''),
                'disease_3': form.cleaned_data.get('disease_3', ''),
                'medical_history': form.cleaned_data.get('medical_history', ''),
                'health_basic_info_details': form.cleaned_data.get('health_basic_info_details', ''),
                'main_doctor_hospital': form.cleaned_data.get('main_doctor_hospital', ''),
                'main_doctor_name': form.cleaned_data.get('main_doctor_name', ''),
                'visiting_doctor_hospital': form.cleaned_data.get('visiting_doctor_hospital', ''),
                'visiting_doctor_name': form.cleaned_data.get('visiting_doctor_name', ''),
                'medication_status': form.cleaned_data.get('medication_status', ''),
                'medication_content': form.cleaned_data.get('medication_content', ''),
                'allergy_details': form.cleaned_data.get('allergy_details', ''),
                'main_doctor': form.cleaned_data.get('main_doctor', ''),
                'outpatient_clinic': form.cleaned_data.get('outpatient_clinic', ''),
                'medication': form.cleaned_data.get('medication', ''),
                'hospital': form.cleaned_data.get('hospital', ''),
                'medication_details': form.cleaned_data.get('medication_details', ''),
                'allergies': form.cleaned_data.get('allergies', False),
            }

            detailed_data['physical_status'] = {
                'skin_condition': form.cleaned_data.get('skin_condition', []),
                'infection_status': form.cleaned_data.get('infection_status', []),
                'special_treatment': form.cleaned_data.get('special_treatment', []),
                'pain_location': form.cleaned_data.get('pain_location', ''),
                'pain_existence': form.cleaned_data.get('pain_existence', ''),
                'height': str(form.cleaned_data.get('height', '')) if form.cleaned_data.get('height') else '',
                'weight': str(form.cleaned_data.get('weight', '')) if form.cleaned_data.get('weight') else '',
                'vision': form.cleaned_data.get('vision', ''),
                'hearing': form.cleaned_data.get('hearing', ''),
                'physical_notes': form.cleaned_data.get('physical_notes', ''),
            }

            detailed_data['cognitive_function'] = {
                'dementia_presence': form.cleaned_data.get('dementia_presence', ''),
                'dementia_severity': form.cleaned_data.get('dementia_severity', ''),
                'dementia_details': form.cleaned_data.get('dementia_details', ''),
                'bpsd_presence': form.cleaned_data.get('bpsd_presence', ''),
                'bpsd_symptoms': form.cleaned_data.get('bpsd_symptoms', []),
                'bpsd_details': form.cleaned_data.get('bpsd_details', ''),
                'conversation': form.cleaned_data.get('conversation', ''),
                'communication': form.cleaned_data.get('communication', ''),
                'cognitive_notes': form.cleaned_data.get('cognitive_notes', ''),
            }

            detailed_data['basic_activities'] = {
                'turning_over': form.cleaned_data.get('turning_over', ''),
                'getting_up': form.cleaned_data.get('getting_up', ''),
                'sitting': form.cleaned_data.get('sitting', ''),
                'standing_up': form.cleaned_data.get('standing_up', ''),
                'standing': form.cleaned_data.get('standing', ''),
                'transfer': form.cleaned_data.get('transfer', ''),
                'indoor_mobility': form.cleaned_data.get('indoor_mobility', ''),
                'outdoor_mobility': form.cleaned_data.get('outdoor_mobility', ''),
                'indoor_mobility_equipment': form.cleaned_data.get('indoor_mobility_equipment', ''),
                'outdoor_mobility_equipment': form.cleaned_data.get('outdoor_mobility_equipment', ''),
                'basic_activity_notes': form.cleaned_data.get('basic_activity_notes', ''),
            }

            detailed_data['adl'] = {
                'eating_method': form.cleaned_data.get('eating_method', ''),
                'eating_assistance': form.cleaned_data.get('eating_assistance', ''),
                'swallowing': form.cleaned_data.get('swallowing', ''),
                'meal_form_main': form.cleaned_data.get('meal_form_main', ''),
                'meal_form_side': form.cleaned_data.get('meal_form_side', ''),
                'water_thickening': form.cleaned_data.get('water_thickening', False),
                'eating_restriction': form.cleaned_data.get('eating_restriction', ''),
                'eating_utensils': form.cleaned_data.get('eating_utensils', []),
                'eating_notes': form.cleaned_data.get('eating_notes', ''),
                'oral_hygiene_assistance': form.cleaned_data.get('oral_hygiene_assistance', ''),
                'natural_teeth_presence': form.cleaned_data.get('natural_teeth_presence', ''),
                'denture_presence': form.cleaned_data.get('denture_presence', ''),
                'denture_type': form.cleaned_data.get('denture_type', ''),
                'denture_location': form.cleaned_data.get('denture_location', ''),
                'tooth_decay': form.cleaned_data.get('tooth_decay', False),
                'oral_notes': form.cleaned_data.get('oral_notes', ''),
                'bathing_assistance': form.cleaned_data.get('bathing_assistance', ''),
                'bathing_form': form.cleaned_data.get('bathing_form', ''),
                'bathing_restriction': form.cleaned_data.get('bathing_restriction', False),
                'dressing_upper': form.cleaned_data.get('dressing_upper', ''),
                'dressing_lower': form.cleaned_data.get('dressing_lower', ''),
                'bathing_notes': form.cleaned_data.get('bathing_notes', ''),
                'excretion_assistance': form.cleaned_data.get('excretion_assistance', ''),
                'urination': form.cleaned_data.get('urination', False),
                'urinary_incontinence': form.cleaned_data.get('urinary_incontinence', False),
                'defecation': form.cleaned_data.get('defecation', False),
                'fecal_incontinence': form.cleaned_data.get('fecal_incontinence', False),
                'daytime_location': form.cleaned_data.get('daytime_location', []),
                'daytime_method': form.cleaned_data.get('daytime_method', []),
                'nighttime_location': form.cleaned_data.get('nighttime_location', []),
                'nighttime_method': form.cleaned_data.get('nighttime_method', []),
                'excretion_supplies': form.cleaned_data.get('excretion_supplies', []),
                'excretion_notes': form.cleaned_data.get('excretion_notes', ''),
            }

            detailed_data['iadl'] = {
                'cooking': form.cleaned_data.get('cooking', ''),
                'cleaning': form.cleaned_data.get('cleaning', ''),
                'washing': form.cleaned_data.get('washing', ''),
                'shopping': form.cleaned_data.get('shopping', ''),
                'money_management': form.cleaned_data.get('money_management', ''),
                'iadl_notes': form.cleaned_data.get('iadl_notes', ''),
            }

            # 基本情報を更新
            assessment.assessment_type = request.POST.get('assessment_type', assessment.assessment_type)
            assessment.interview_location = request.POST.get('interview_location', assessment.interview_location)

            # 作成日を更新
            created_date = request.POST.get('created_date')
            if created_date:
                from datetime import datetime
                try:
                    assessment.assessment_date = datetime.strptime(created_date, '%Y-%m-%d').date()
                except ValueError:
                    pass

            # その他フィールドの処理
            assessment_type_other = request.POST.get('assessment_type_other', '')
            interview_location_other = request.POST.get('interview_location_other', '')

            # その他フィールドをモデルフィールドに保存
            assessment.assessment_type_other = assessment_type_other
            assessment.interview_location_other = interview_location_other

            # その他フィールドをbasic_infoに追加
            detailed_data['basic_info']['assessment_type_other'] = assessment_type_other
            detailed_data['basic_info']['interview_location_other'] = interview_location_other

            # 健康状態データに疾患名・発症日を追加
            for i in range(1, 7):
                detailed_data['health_status'][f'disease_name_{i}'] = request.POST.get(f'disease_name_{i}', '')
                detailed_data['health_status'][f'onset_date_{i}'] = request.POST.get(f'onset_date_{i}', '')

            # 特別な医療処置を追加
            detailed_data['health_status']['special_medical_treatment_status'] = request.POST.get('special_medical_treatment_status', '')
            detailed_data['health_status']['special_medical_treatment'] = request.POST.getlist('special_medical_treatment')

            # 基本情報の詳細を追加
            detailed_data['health_status']['health_basic_info_details'] = request.POST.get('health_basic_info_details', '')

            # フォームで定義されていないが、テンプレートで使用されているフィールドを直接POSTから取得
            additional_fields = [
                'main_doctor_hospital', 'main_doctor_name', 'visiting_doctor_hospital',
                'visiting_doctor_name', 'family_doctor_hospital_1', 'family_doctor_name_1',
                'family_doctor_hospital_2', 'family_doctor_name_2', 'family_doctor_hospital_3',
                'family_doctor_name_3', 'family_doctor_hospital_4', 'family_doctor_name_4',
                'hospital_visit_status', 'hospital_visit_method', 'hospital_visit_method_other',
                'medical_institution_notes', 'medication_status', 'medication_content',
                'allergy_details', 'medication_allergy_notes', 'has_sleeping_medication',
                'has_laxative', 'has_allergy', 'has_skin_disease', 'skin_disease_other',
                'infection_presence', 'infection_other_text', 'skin_infection_details',
                'has_paralysis', 'has_pain', 'uses_hearing_aid', 'uses_glasses', 'sensory_function_details'
            ]

            for field in additional_fields:
                if field in request.POST:
                    detailed_data['health_status'][field] = request.POST.get(field, '')

            # physical_status関連フィールドをphysical_statusに移動
            if 'physical_status_notes' in request.POST:
                detailed_data['physical_status']['notes'] = request.POST.get('physical_status_notes', '')
            if 'paralysis_pain_details' in request.POST:
                detailed_data['physical_status']['paralysis_pain_details'] = request.POST.get('paralysis_pain_details', '')
            if 'skin_infection_details' in request.POST:
                detailed_data['physical_status']['skin_infection_details'] = request.POST.get('skin_infection_details', '')
            if 'paralysis_location' in request.POST:
                detailed_data['physical_status']['paralysis_location'] = request.POST.get('paralysis_location', '')
            if 'pain_location' in request.POST:
                detailed_data['physical_status']['pain_location'] = request.POST.get('pain_location', '')

            # MultipleChoiceFieldの特別処理
            detailed_data['health_status']['skin_disease'] = request.POST.getlist('skin_disease')
            detailed_data['health_status']['infection'] = request.POST.getlist('infection')

            # その他のセクションのフィールドも追加
            # 基本動作関連
            basic_activity_additional = [
                'indoor_mobility_equipment_other', 'outdoor_mobility_equipment_other'
            ]
            for field in basic_activity_additional:
                if field in request.POST:
                    detailed_data['basic_activities'][field] = request.POST.get(field, '')

            # ADL関連
            adl_additional = [
                'water_thickening_level', 'eating_restriction_detail', 'eating_utensils_other_detail',
                'bathing_restriction_detail', 'urinary_incontinence_frequency',
                'fecal_incontinence_frequency'
            ]
            for field in adl_additional:
                if field in request.POST:
                    detailed_data['adl'][field] = request.POST.get(field, '')

            # 認知機能関連
            cognitive_additional = [
                'dementia_details', 'bpsd_details'
            ]
            for field in cognitive_additional:
                if field in request.POST:
                    detailed_data['cognitive_function'][field] = request.POST.get(field, '')

            # BPSD症状（複数選択）の処理
            if 'bpsd_symptoms' in request.POST:
                detailed_data['cognitive_function']['bpsd_symptoms'] = request.POST.getlist('bpsd_symptoms')

            # サービス関連
            services_additional = [
                'other_services_detail_text', 'services_notes'
            ]
            for field in services_additional:
                if field in request.POST:
                    detailed_data['services'][field] = request.POST.get(field, '')

            # 居住状況関連
            living_additional = [
                'other_home_environment_detail_text', 'other_housing_type_detail_text',
                'other_ownership_detail_text', 'other_sleeping_detail_text', 'housing_notes'
            ]
            for field in living_additional:
                if field in request.POST:
                    detailed_data['living_situation'][field] = request.POST.get(field, '')

            # JSONフィールドにデータを設定
            assessment.basic_info = detailed_data['basic_info']
            assessment.insurance_info = detailed_data['insurance_info']
            assessment.family_situation = detailed_data['family_situation']
            assessment.living_situation = detailed_data['living_situation']
            assessment.services = detailed_data['services']
            assessment.health_status = detailed_data['health_status']
            assessment.physical_status = detailed_data['physical_status']
            assessment.cognitive_function = detailed_data['cognitive_function']
            assessment.basic_activities = detailed_data['basic_activities']
            assessment.adl = detailed_data['adl']
            assessment.iadl = detailed_data['iadl']

            assessment.save()

            # actionによる分岐処理
            if action == 'excel':
                # Excel出力（自動保存済み）
                return generate_assessment_excel(assessment)
            else:
                # 通常の保存
                messages.success(request, 'アセスメントを更新しました')
                url = reverse('client_detail', kwargs={'pk': assessment.client.pk}) + '#assessment-history'
                return HttpResponseRedirect(url)
        else:
            # フォームバリデーションエラーが発生した場合の処理
            print("=== FORM VALIDATION ERROR (EDIT) ===")
            print(f"Form errors: {form.errors}")
            print(f"Form non-field errors: {form.non_field_errors()}")

            # 各フィールドのエラーを詳細出力
            for field, errors in form.errors.items():
                print(f"Field '{field}' errors: {errors}")
            print("=== END FORM VALIDATION ERROR ===")

            messages.error(request, 'フォームにエラーがあります。入力内容を確認してください。')

            # フォームの選択肢を設定（バリデーションエラー後も選択肢を保持）
            form.fields['assessment_type'].widget.choices = Assessment.ASSESSMENT_TYPE_CHOICES
            form.fields['interview_location'].widget.choices = Assessment.INTERVIEW_LOCATION_CHOICES
    else:
        # 既存のデータでフォームを初期化
        initial_data = {
            'assessment_type': assessment.assessment_type,
            'interview_location': assessment.interview_location,
        }

        # その他フィールドの初期値を設定
        if assessment.basic_info:
            initial_data['assessment_type_other'] = assessment.basic_info.get('assessment_type_other', '')
            initial_data['interview_location_other'] = assessment.basic_info.get('interview_location_other', '')

        # 作成日の初期値を設定
        initial_data['created_date'] = assessment.assessment_date
        initial_data['creator'] = assessment.assessor.profile.get_full_name() if assessment.assessor else ''

        # JSONフィールドから既存データを読み込み
        if assessment.basic_info:
            for key, value in assessment.basic_info.items():
                initial_data[key] = value
        if assessment.insurance_info:
            for key, value in assessment.insurance_info.items():
                initial_data[key] = value
        if assessment.family_situation:
            for key, value in assessment.family_situation.items():
                initial_data[key] = value
        if assessment.living_situation:
            for key, value in assessment.living_situation.items():
                initial_data[key] = value
        if assessment.services:
            for key, value in assessment.services.items():
                initial_data[key] = value
        if assessment.health_status:
            for key, value in assessment.health_status.items():
                # 数値フィールドの処理
                if key in ['height', 'weight'] and value:
                    try:
                        initial_data[key] = float(value) if value != '' else None
                    except (ValueError, TypeError):
                        initial_data[key] = None
                else:
                    initial_data[key] = value
        if assessment.physical_status:
            for key, value in assessment.physical_status.items():
                # 数値フィールドの処理
                if key in ['height', 'weight'] and value:
                    try:
                        initial_data[key] = float(value) if value != '' else None
                    except (ValueError, TypeError):
                        initial_data[key] = None
                elif key == 'notes':
                    # physical_status.notesをphysical_status_notesフィールドにマッピング
                    initial_data['physical_status_notes'] = value
                elif key == 'paralysis_pain_details':
                    initial_data['paralysis_pain_details'] = value
                elif key == 'skin_infection_details':
                    initial_data['skin_infection_details'] = value
                elif key == 'paralysis_location':
                    initial_data['paralysis_location'] = value
                elif key == 'pain_location':
                    initial_data['pain_location'] = value
                else:
                    initial_data[key] = value

        # 既存データの互換性のため、health_statusにphysical_status関連フィールドがある場合の処理
        if assessment.health_status:
            # physical_status_notes
            if 'physical_status_notes' in assessment.health_status:
                if 'physical_status_notes' not in initial_data or not initial_data['physical_status_notes']:
                    initial_data['physical_status_notes'] = assessment.health_status['physical_status_notes']
            # paralysis_pain_details
            if 'paralysis_pain_details' in assessment.health_status:
                if 'paralysis_pain_details' not in initial_data or not initial_data['paralysis_pain_details']:
                    initial_data['paralysis_pain_details'] = assessment.health_status['paralysis_pain_details']
            # skin_infection_details
            if 'skin_infection_details' in assessment.health_status:
                if 'skin_infection_details' not in initial_data or not initial_data['skin_infection_details']:
                    initial_data['skin_infection_details'] = assessment.health_status['skin_infection_details']
            # paralysis_location
            if 'paralysis_location' in assessment.health_status:
                if 'paralysis_location' not in initial_data or not initial_data['paralysis_location']:
                    initial_data['paralysis_location'] = assessment.health_status['paralysis_location']
            # pain_location
            if 'pain_location' in assessment.health_status:
                if 'pain_location' not in initial_data or not initial_data['pain_location']:
                    initial_data['pain_location'] = assessment.health_status['pain_location']
        if assessment.cognitive_function:
            for key, value in assessment.cognitive_function.items():
                initial_data[key] = value
        if assessment.basic_activities:
            for key, value in assessment.basic_activities.items():
                initial_data[key] = value
        if assessment.adl:
            for key, value in assessment.adl.items():
                initial_data[key] = value
        if assessment.iadl:
            for key, value in assessment.iadl.items():
                initial_data[key] = value

        form = DetailedAssessmentForm(initial=initial_data)

        # フォームの選択肢を設定
        form.fields['assessment_type'].widget.choices = Assessment.ASSESSMENT_TYPE_CHOICES
        form.fields['interview_location'].widget.choices = Assessment.INTERVIEW_LOCATION_CHOICES

    context = {
        'form': form,
        'assessment': assessment,
        'assessment_types': Assessment.ASSESSMENT_TYPE_CHOICES,
        'interview_locations': Assessment.INTERVIEW_LOCATION_CHOICES,
        'is_edit': True,
    }

    return render(request, 'assessments/detailed_assessment_form.html', context)


@login_required
def detailed_assessment_create(request):
    """アセスメント作成ビュー"""
    client_id = request.GET.get('client')
    selected_client = None
    
    if client_id:
        selected_client = get_object_or_404(Client, pk=client_id)
    
    if request.method == 'POST':
        form = DetailedAssessmentForm(request.POST)

        if form.is_valid():
            # actionパラメータを取得
            action = request.POST.get('action', 'save')

            # 基本アセスメント作成
            client_pk = request.POST.get('selected_client')
            client = get_object_or_404(Client, pk=client_pk)

            assessment = Assessment(
                client=client,
                assessor=request.user,
                assessment_type=request.POST.get('assessment_type', 'new'),
                interview_location=request.POST.get('interview_location', 'home')
            )

            # 作成日を設定
            created_date = request.POST.get('created_date')
            if created_date:
                from datetime import datetime
                try:
                    assessment.assessment_date = datetime.strptime(created_date, '%Y-%m-%d').date()
                except ValueError:
                    pass
            
            # 詳細データをJSONフィールドに保存
            detailed_data = {}
            
            # 各セクションのデータを整理
            detailed_data['basic_info'] = {
                'life_history': form.cleaned_data.get('life_history', ''),
                'personal_hopes': form.cleaned_data.get('personal_hopes', ''),
                'family_hopes': form.cleaned_data.get('family_hopes', ''),
                'assessment_type_other': request.POST.get('assessment_type_other', ''),
                'interview_location_other': request.POST.get('interview_location_other', ''),
                'special_situation_status': request.POST.get('special_situation_status', ''),
                'special_situation': request.POST.getlist('special_situation'),
                'special_situation_other': request.POST.get('special_situation_other', ''),
            }

            detailed_data['insurance_info'] = {
                'care_level': form.cleaned_data.get('care_level', ''),
                'dementia_level': form.cleaned_data.get('dementia_level', ''),
                'burden_ratio': form.cleaned_data.get('burden_ratio', ''),
                'medical_insurance': form.cleaned_data.get('medical_insurance', ''),
                'disability_handbook': form.cleaned_data.get('disability_handbook', False),
                'difficulty_certificate': form.cleaned_data.get('difficulty_certificate', False),
                'life_protection': form.cleaned_data.get('life_protection', False),
            }

            detailed_data['family_situation'] = {
                'family_member1': form.cleaned_data.get('family_member1', ''),
                'family_member2': form.cleaned_data.get('family_member2', ''),
            }

            detailed_data['living_situation'] = {
                'home_environment': request.POST.get('home_environment', ''),
                'other_home_environment_detail_text': request.POST.get('other_home_environment_detail_text', ''),
                'housing_type': request.POST.get('housing_type', ''),
                'other_housing_type_detail_text': request.POST.get('other_housing_type_detail_text', ''),
                'has_elevator': request.POST.get('has_elevator', ''),
                'housing_ownership': request.POST.get('housing_ownership', ''),
                'other_ownership_detail_text': request.POST.get('other_ownership_detail_text', ''),
                'private_room': request.POST.get('private_room', ''),
                'air_conditioning': request.POST.get('air_conditioning', ''),
                'toilet_type': request.POST.get('toilet_type', ''),
                'toilet_handrail': request.POST.get('toilet_handrail', ''),
                'toilet_step': request.POST.get('toilet_step', ''),
                'bathroom': request.POST.get('bathroom', ''),
                'bathroom_handrail': request.POST.get('bathroom_handrail', ''),
                'bathroom_step': request.POST.get('bathroom_step', ''),
                'sleeping_arrangement': request.POST.get('sleeping_arrangement', ''),
                'other_sleeping_detail_text': request.POST.get('other_sleeping_detail_text', ''),
                'room_level_difference': request.POST.get('room_level_difference', ''),
                'housing_modification': request.POST.get('housing_modification', ''),
                'housing_modification_need': request.POST.get('housing_modification_need', ''),
                'housing_notes': request.POST.get('housing_notes', ''),
            }

            detailed_data['services'] = {
                'care_services': form.cleaned_data.get('care_services', []),
                'welfare_equipment': form.cleaned_data.get('welfare_equipment', []),
                'other_services': form.cleaned_data.get('other_services', ''),
                'informal_services': form.cleaned_data.get('informal_services', []),
                'other_services_detail_text': form.cleaned_data.get('other_services_detail_text', ''),
                'social_relationships': form.cleaned_data.get('social_relationships', ''),
            }

            detailed_data['health_status'] = {
                # 疾患名・発症日フィールド
                'disease_name_1': request.POST.get('disease_name_1', ''),
                'disease_name_2': request.POST.get('disease_name_2', ''),
                'disease_name_3': request.POST.get('disease_name_3', ''),
                'disease_name_4': request.POST.get('disease_name_4', ''),
                'disease_name_5': request.POST.get('disease_name_5', ''),
                'disease_name_6': request.POST.get('disease_name_6', ''),
                'onset_date_1': request.POST.get('onset_date_1', ''),
                'onset_date_2': request.POST.get('onset_date_2', ''),
                'onset_date_3': request.POST.get('onset_date_3', ''),
                'onset_date_4': request.POST.get('onset_date_4', ''),
                'onset_date_5': request.POST.get('onset_date_5', ''),
                'onset_date_6': request.POST.get('onset_date_6', ''),
                # 既存フィールド
                'disease_1': form.cleaned_data.get('disease_1', ''),
                'disease_2': form.cleaned_data.get('disease_2', ''),
                'disease_3': form.cleaned_data.get('disease_3', ''),
                'medical_history': form.cleaned_data.get('medical_history', ''),
                'health_basic_info_details': form.cleaned_data.get('health_basic_info_details', ''),
                'main_doctor_hospital': form.cleaned_data.get('main_doctor_hospital', ''),
                'main_doctor_name': form.cleaned_data.get('main_doctor_name', ''),
                'visiting_doctor_hospital': form.cleaned_data.get('visiting_doctor_hospital', ''),
                'visiting_doctor_name': form.cleaned_data.get('visiting_doctor_name', ''),
                'medication_status': form.cleaned_data.get('medication_status', ''),
                'medication_content': form.cleaned_data.get('medication_content', ''),
                'allergy_details': form.cleaned_data.get('allergy_details', ''),
                'main_doctor': form.cleaned_data.get('main_doctor', ''),
                'outpatient_clinic': form.cleaned_data.get('outpatient_clinic', ''),
                'medication': form.cleaned_data.get('medication', ''),
                'hospital': form.cleaned_data.get('hospital', ''),
                'medication_details': form.cleaned_data.get('medication_details', ''),
                'allergies': form.cleaned_data.get('allergies', False),
                # 特別な医療処置
                'special_medical_treatment_status': request.POST.get('special_medical_treatment_status', ''),
                'special_medical_treatment': request.POST.getlist('special_medical_treatment'),
            }

            # フォームで定義されていないが、テンプレートで使用されているフィールドを直接POSTから取得
            additional_fields = [
                'main_doctor_hospital', 'main_doctor_name', 'visiting_doctor_hospital',
                'visiting_doctor_name', 'family_doctor_hospital_1', 'family_doctor_name_1',
                'family_doctor_hospital_2', 'family_doctor_name_2', 'family_doctor_hospital_3',
                'family_doctor_name_3', 'family_doctor_hospital_4', 'family_doctor_name_4',
                'hospital_visit_status', 'hospital_visit_method', 'hospital_visit_method_other',
                'medical_institution_notes', 'medication_status', 'medication_content',
                'allergy_details', 'medication_allergy_notes', 'has_sleeping_medication',
                'has_laxative', 'has_allergy', 'has_skin_disease', 'skin_disease_other',
                'infection_presence', 'infection_other_text', 'skin_infection_details',
                'has_paralysis', 'has_pain', 'uses_hearing_aid', 'uses_glasses', 'sensory_function_details'
            ]

            for field in additional_fields:
                if field in request.POST:
                    detailed_data['health_status'][field] = request.POST.get(field, '')

            # physical_statusの初期化
            detailed_data['physical_status'] = {
                'skin_condition': form.cleaned_data.get('skin_condition', []),
                'infection_status': form.cleaned_data.get('infection_status', []),
                'special_treatment': form.cleaned_data.get('special_treatment', []),
                'pain_location': form.cleaned_data.get('pain_location', ''),
                'pain_existence': form.cleaned_data.get('pain_existence', ''),
                'height': str(form.cleaned_data.get('height', '')) if form.cleaned_data.get('height') else '',
                'weight': str(form.cleaned_data.get('weight', '')) if form.cleaned_data.get('weight') else '',
            }

            detailed_data['cognitive_function'] = {
                'dementia_presence': form.cleaned_data.get('dementia_presence', ''),
                'dementia_severity': form.cleaned_data.get('dementia_severity', ''),
                'dementia_details': form.cleaned_data.get('dementia_details', ''),
                'bpsd_presence': form.cleaned_data.get('bpsd_presence', ''),
                'bpsd_symptoms': form.cleaned_data.get('bpsd_symptoms', []),
                'bpsd_details': form.cleaned_data.get('bpsd_details', ''),
                'conversation': form.cleaned_data.get('conversation', ''),
                'communication': form.cleaned_data.get('communication', ''),
                'cognitive_notes': form.cleaned_data.get('cognitive_notes', ''),
            }

            detailed_data['basic_activities'] = {
                'turning_over': form.cleaned_data.get('turning_over', ''),
                'getting_up': form.cleaned_data.get('getting_up', ''),
                'sitting': form.cleaned_data.get('sitting', ''),
                'standing_up': form.cleaned_data.get('standing_up', ''),
                'standing': form.cleaned_data.get('standing', ''),
                'transfer': form.cleaned_data.get('transfer', ''),
                'indoor_mobility': form.cleaned_data.get('indoor_mobility', ''),
                'outdoor_mobility': form.cleaned_data.get('outdoor_mobility', ''),
                'indoor_mobility_equipment': form.cleaned_data.get('indoor_mobility_equipment', ''),
                'outdoor_mobility_equipment': form.cleaned_data.get('outdoor_mobility_equipment', ''),
                'basic_activity_notes': form.cleaned_data.get('basic_activity_notes', ''),
            }

            detailed_data['adl'] = {
                'eating_method': form.cleaned_data.get('eating_method', ''),
                'eating_assistance': form.cleaned_data.get('eating_assistance', ''),
                'swallowing': form.cleaned_data.get('swallowing', ''),
                'meal_form_main': form.cleaned_data.get('meal_form_main', ''),
                'meal_form_side': form.cleaned_data.get('meal_form_side', ''),
                'water_thickening': form.cleaned_data.get('water_thickening', False),
                'eating_restriction': form.cleaned_data.get('eating_restriction', ''),
                'eating_utensils': form.cleaned_data.get('eating_utensils', []),
                'eating_notes': form.cleaned_data.get('eating_notes', ''),
                'oral_hygiene_assistance': form.cleaned_data.get('oral_hygiene_assistance', ''),
                'natural_teeth_presence': form.cleaned_data.get('natural_teeth_presence', ''),
                'denture_presence': form.cleaned_data.get('denture_presence', ''),
                'denture_type': form.cleaned_data.get('denture_type', ''),
                'denture_location': form.cleaned_data.get('denture_location', ''),
                'tooth_decay': form.cleaned_data.get('tooth_decay', False),
                'oral_notes': form.cleaned_data.get('oral_notes', ''),
                'bathing_assistance': form.cleaned_data.get('bathing_assistance', ''),
                'bathing_form': form.cleaned_data.get('bathing_form', ''),
                'bathing_restriction': form.cleaned_data.get('bathing_restriction', False),
                'dressing_upper': form.cleaned_data.get('dressing_upper', ''),
                'dressing_lower': form.cleaned_data.get('dressing_lower', ''),
                'bathing_notes': form.cleaned_data.get('bathing_notes', ''),
                'excretion_assistance': form.cleaned_data.get('excretion_assistance', ''),
                'urination': form.cleaned_data.get('urination', False),
                'urinary_incontinence': form.cleaned_data.get('urinary_incontinence', False),
                'defecation': form.cleaned_data.get('defecation', False),
                'fecal_incontinence': form.cleaned_data.get('fecal_incontinence', False),
                'daytime_location': form.cleaned_data.get('daytime_location', []),
                'daytime_method': form.cleaned_data.get('daytime_method', []),
                'nighttime_location': form.cleaned_data.get('nighttime_location', []),
                'nighttime_method': form.cleaned_data.get('nighttime_method', []),
                'excretion_supplies': form.cleaned_data.get('excretion_supplies', []),
                'excretion_notes': form.cleaned_data.get('excretion_notes', ''),
            }

            detailed_data['iadl'] = {
                'cooking': form.cleaned_data.get('cooking', ''),
                'cleaning': form.cleaned_data.get('cleaning', ''),
                'washing': form.cleaned_data.get('washing', ''),
                'shopping': form.cleaned_data.get('shopping', ''),
                'money_management': form.cleaned_data.get('money_management', ''),
                'iadl_notes': form.cleaned_data.get('iadl_notes', ''),
            }

            # physical_status関連フィールドをphysical_statusに移動
            if 'physical_status_notes' in request.POST:
                detailed_data['physical_status']['notes'] = request.POST.get('physical_status_notes', '')
            if 'paralysis_pain_details' in request.POST:
                detailed_data['physical_status']['paralysis_pain_details'] = request.POST.get('paralysis_pain_details', '')
            if 'skin_infection_details' in request.POST:
                detailed_data['physical_status']['skin_infection_details'] = request.POST.get('skin_infection_details', '')
            if 'paralysis_location' in request.POST:
                detailed_data['physical_status']['paralysis_location'] = request.POST.get('paralysis_location', '')
            if 'pain_location' in request.POST:
                detailed_data['physical_status']['pain_location'] = request.POST.get('pain_location', '')

            # MultipleChoiceFieldの特別処理
            detailed_data['health_status']['skin_disease'] = request.POST.getlist('skin_disease')
            detailed_data['health_status']['infection'] = request.POST.getlist('infection')

            # その他のセクションのフィールドも追加
            # 基本動作関連
            basic_activity_additional = [
                'indoor_mobility_equipment_other', 'outdoor_mobility_equipment_other'
            ]
            for field in basic_activity_additional:
                if field in request.POST:
                    detailed_data['basic_activities'][field] = request.POST.get(field, '')

            # ADL関連
            adl_additional = [
                'water_thickening_level', 'eating_restriction_detail', 'eating_utensils_other_detail',
                'bathing_restriction_detail', 'urinary_incontinence_frequency',
                'fecal_incontinence_frequency'
            ]
            for field in adl_additional:
                if field in request.POST:
                    detailed_data['adl'][field] = request.POST.get(field, '')

            # 認知機能関連
            cognitive_additional = [
                'dementia_details', 'bpsd_details'
            ]
            for field in cognitive_additional:
                if field in request.POST:
                    detailed_data['cognitive_function'][field] = request.POST.get(field, '')

            # BPSD症状（複数選択）の処理
            if 'bpsd_symptoms' in request.POST:
                detailed_data['cognitive_function']['bpsd_symptoms'] = request.POST.getlist('bpsd_symptoms')

            # サービス関連
            services_additional = [
                'other_services_detail_text', 'services_notes'
            ]
            for field in services_additional:
                if field in request.POST:
                    detailed_data['services'][field] = request.POST.get(field, '')

            # 居住状況関連
            living_additional = [
                'other_home_environment_detail_text', 'other_housing_type_detail_text',
                'other_ownership_detail_text', 'other_sleeping_detail_text', 'housing_notes'
            ]
            for field in living_additional:
                if field in request.POST:
                    detailed_data['living_situation'][field] = request.POST.get(field, '')

            # physical_statusの基本データを設定（既存の追加フィールドを保持）
            detailed_data['physical_status'].update({
                'skin_condition': form.cleaned_data.get('skin_condition', []),
                'infection_status': form.cleaned_data.get('infection_status', []),
                'special_treatment': form.cleaned_data.get('special_treatment', []),
                'pain_location': form.cleaned_data.get('pain_location', ''),
                'pain_existence': form.cleaned_data.get('pain_existence', ''),
                'height': str(form.cleaned_data.get('height', '')) if form.cleaned_data.get('height') else '',
                'weight': str(form.cleaned_data.get('weight', '')) if form.cleaned_data.get('weight') else '',
                'vision': form.cleaned_data.get('vision', ''),
                'hearing': form.cleaned_data.get('hearing', ''),
                'physical_notes': form.cleaned_data.get('physical_notes', ''),
            })
            
            detailed_data['cognitive_function'] = {
                'dementia_presence': form.cleaned_data.get('dementia_presence', ''),
                'dementia_severity': form.cleaned_data.get('dementia_severity', ''),
                'dementia_details': form.cleaned_data.get('dementia_details', ''),
                'bpsd_presence': form.cleaned_data.get('bpsd_presence', ''),
                'bpsd_symptoms': form.cleaned_data.get('bpsd_symptoms', []),
                'bpsd_details': form.cleaned_data.get('bpsd_details', ''),
                'conversation': form.cleaned_data.get('conversation', ''),
                'communication': form.cleaned_data.get('communication', ''),
                'cognitive_notes': form.cleaned_data.get('cognitive_notes', ''),
            }
            
            detailed_data['basic_activities'] = {
                'turning_over': form.cleaned_data.get('turning_over', ''),
                'getting_up': form.cleaned_data.get('getting_up', ''),
                'sitting': form.cleaned_data.get('sitting', ''),
                'standing_up': form.cleaned_data.get('standing_up', ''),
                'standing': form.cleaned_data.get('standing', ''),
                'transfer': form.cleaned_data.get('transfer', ''),
                'indoor_mobility': form.cleaned_data.get('indoor_mobility', ''),
                'outdoor_mobility': form.cleaned_data.get('outdoor_mobility', ''),
                'indoor_mobility_equipment': form.cleaned_data.get('indoor_mobility_equipment', ''),
                'outdoor_mobility_equipment': form.cleaned_data.get('outdoor_mobility_equipment', ''),
                'basic_activity_notes': form.cleaned_data.get('basic_activity_notes', ''),
            }
            
            detailed_data['adl'] = {
                'eating_method': form.cleaned_data.get('eating_method', ''),
                'eating_assistance': form.cleaned_data.get('eating_assistance', ''),
                'swallowing': form.cleaned_data.get('swallowing', ''),
                'meal_form_main': form.cleaned_data.get('meal_form_main', ''),
                'meal_form_side': form.cleaned_data.get('meal_form_side', ''),
                'water_thickening': form.cleaned_data.get('water_thickening', False),
                'eating_restriction': form.cleaned_data.get('eating_restriction', ''),
                'eating_utensils': form.cleaned_data.get('eating_utensils', []),
                'eating_notes': form.cleaned_data.get('eating_notes', ''),
                'oral_hygiene_assistance': form.cleaned_data.get('oral_hygiene_assistance', ''),
                'natural_teeth_presence': form.cleaned_data.get('natural_teeth_presence', ''),
                'denture_presence': form.cleaned_data.get('denture_presence', ''),
                'denture_type': form.cleaned_data.get('denture_type', ''),
                'denture_location': form.cleaned_data.get('denture_location', ''),
                'tooth_decay': form.cleaned_data.get('tooth_decay', False),
                'oral_notes': form.cleaned_data.get('oral_notes', ''),
                'bathing_assistance': form.cleaned_data.get('bathing_assistance', ''),
                'bathing_form': form.cleaned_data.get('bathing_form', ''),
                'bathing_restriction': form.cleaned_data.get('bathing_restriction', False),
                'dressing_upper': form.cleaned_data.get('dressing_upper', ''),
                'dressing_lower': form.cleaned_data.get('dressing_lower', ''),
                'bathing_notes': form.cleaned_data.get('bathing_notes', ''),
                'excretion_assistance': form.cleaned_data.get('excretion_assistance', ''),
                'urination': form.cleaned_data.get('urination', False),
                'urinary_incontinence': form.cleaned_data.get('urinary_incontinence', False),
                'defecation': form.cleaned_data.get('defecation', False),
                'fecal_incontinence': form.cleaned_data.get('fecal_incontinence', False),
                'daytime_location': form.cleaned_data.get('daytime_location', []),
                'daytime_method': form.cleaned_data.get('daytime_method', []),
                'nighttime_location': form.cleaned_data.get('nighttime_location', []),
                'nighttime_method': form.cleaned_data.get('nighttime_method', []),
                'excretion_supplies': form.cleaned_data.get('excretion_supplies', []),
                'excretion_notes': form.cleaned_data.get('excretion_notes', ''),
            }
            
            detailed_data['iadl'] = {
                'cooking': form.cleaned_data.get('cooking', ''),
                'cleaning': form.cleaned_data.get('cleaning', ''),
                'washing': form.cleaned_data.get('washing', ''),
                'shopping': form.cleaned_data.get('shopping', ''),
                'money_management': form.cleaned_data.get('money_management', ''),
                'iadl_notes': form.cleaned_data.get('iadl_notes', ''),
            }
            
            # JSONフィールドにデータを設定
            assessment.basic_info = detailed_data['basic_info']
            assessment.insurance_info = detailed_data['insurance_info']
            assessment.family_situation = detailed_data['family_situation']
            assessment.living_situation = detailed_data['living_situation']
            assessment.services = detailed_data['services']
            assessment.health_status = detailed_data['health_status']
            assessment.physical_status = detailed_data['physical_status']
            assessment.cognitive_function = detailed_data['cognitive_function']
            assessment.basic_activities = detailed_data['basic_activities']
            assessment.adl = detailed_data['adl']
            assessment.iadl = detailed_data['iadl']

            assessment.save()

            # actionによる分岐処理
            if action == 'excel':
                # Excel出力（自動保存済み）
                return generate_assessment_excel(assessment)
            else:
                # 通常の保存
                messages.success(request, 'アセスメントを保存しました')
                url = reverse('client_detail', kwargs={'pk': assessment.client.pk}) + '#assessment-history'
                return HttpResponseRedirect(url)
        else:
            # フォームバリデーションエラーの詳細をログ出力
            print("=== FORM VALIDATION ERROR (CREATE) ===")
            print(f"Form errors: {form.errors}")
            print(f"Form non-field errors: {form.non_field_errors()}")

            # 各フィールドのエラーを詳細出力
            for field, errors in form.errors.items():
                print(f"Field '{field}' errors: {errors}")
            print("=== END FORM VALIDATION ERROR ===")

            messages.error(request, 'フォームにエラーがあります。入力内容を確認してください。')

            # フォームの選択肢を設定（バリデーションエラー後も選択肢を保持）
            form.fields['assessment_type'].widget.choices = Assessment.ASSESSMENT_TYPE_CHOICES
            form.fields['interview_location'].widget.choices = Assessment.INTERVIEW_LOCATION_CHOICES
    else:
        form = DetailedAssessmentForm()

        # フォームの選択肢を設定
        form.fields['assessment_type'].widget.choices = Assessment.ASSESSMENT_TYPE_CHOICES
        form.fields['interview_location'].widget.choices = Assessment.INTERVIEW_LOCATION_CHOICES

    clients = Client.objects.all()
    
    context = {
        'form': form,
        'clients': clients,
        'selected_client': selected_client,
        'assessment_types': Assessment.ASSESSMENT_TYPE_CHOICES,
        'interview_locations': Assessment.INTERVIEW_LOCATION_CHOICES,
        'today': date.today().strftime('%Y-%m-%d'),
        'is_edit': False,
    }

    # 前回アセスメントデータの取得
    if selected_client:
        latest_assessment = Assessment.objects.filter(
            client=selected_client
        ).order_by('-assessment_date', '-created_at').first()
        if latest_assessment:
            context['has_previous_assessment'] = True
            context['previous_assessment_data'] = json.dumps({
                'basic_info': latest_assessment.basic_info or {},
                'insurance_info': latest_assessment.insurance_info or {},
                'family_situation': latest_assessment.family_situation or {},
                'living_situation': latest_assessment.living_situation or {},
                'services': latest_assessment.services or {},
                'health_status': latest_assessment.health_status or {},
                'physical_status': latest_assessment.physical_status or {},
                'cognitive_function': latest_assessment.cognitive_function or {},
                'basic_activities': latest_assessment.basic_activities or {},
                'adl': latest_assessment.adl or {},
                'iadl': latest_assessment.iadl or {},
            }, ensure_ascii=False)

    return render(request, 'assessments/detailed_assessment_form.html', context)


def generate_assessment_excel(assessment):
    """アセスメントのExcel生成（共通関数）"""
    if not OPENPYXL_AVAILABLE:
        raise Exception('Excel出力機能は現在利用できません。openpyxlライブラリのインストールが必要です。')

    try:
        # 座標設定ファイルを読み込み
        coordinates_path = os.path.join(settings.BASE_DIR, 'static', 'config', 'excel_coordinates_assessment.json')
        with open(coordinates_path, 'r', encoding='utf-8') as f:
            coordinates = json.load(f)

        coords = coordinates['assessment_sheet']

        # テンプレートファイルのパス
        template_path = os.path.join(settings.BASE_DIR, 'templates', 'forms', 'assessment_sheet.xlsx')
        if not os.path.exists(template_path):
            raise Exception(f'Excelテンプレートが見つかりません: {template_path}')

        # Excelファイルを読み込み
        workbook = load_workbook(template_path)
        # シート名を確認してアセスメントシートを選択
        # sheet5がエラーの原因なので、正しいシート名を指定
        # デフォルトではactiveシートを使用
        if 'アセスメントシート' in workbook.sheetnames:
            worksheet = workbook['アセスメントシート']
        elif len(workbook.sheetnames) >= 5:
            worksheet = workbook.worksheets[4]  # sheet5 (0-indexed)
        else:
            worksheet = workbook.active

        # 和暦変換関数
        def to_wareki(date):
            if not date:
                return ""
            year = date.year
            month = date.month
            day = date.day

            # 令和: 2019年5月1日〜
            if year >= 2019 and (year > 2019 or month >= 5):
                wareki_year = year - 2018
                return f"令和{wareki_year}年{month}月{day}日"
            # 平成: 1989年1月8日〜2019年4月30日
            elif year >= 1989:
                wareki_year = year - 1988
                return f"平成{wareki_year}年{month}月{day}日"
            # それ以前は昭和として処理
            else:
                wareki_year = year - 1925
                return f"昭和{wareki_year}年{month}月{day}日"

        # 選択肢の値→表示名変換用辞書（接尾辞付き命名規則）
        CHOICE_LABELS = {
            # 基本動作（turning_over, getting_up, standing_up）
            'basic_no_assistance': 'つかまらないでできる',
            'basic_with_assistance': '何かにつかまればできる',
            'basic_cannot': 'できない',
            # 座位（sitting）
            'sitting_can_do': 'できる',
            'sitting_self_support': '自分の手で支えればできる',
            'sitting_support_needed': '支えてもらえればできる',
            'sitting_cannot': 'できない',
            # 立位（standing）
            'standing_no_support': '支えなしでできる',
            'standing_with_something': '何か支えがあればできる',
            'standing_cannot': 'できない',
            # 移乗・移動（transfer, indoor_mobility, outdoor_mobility）
            'mobility_independent': '自立',
            'mobility_supervision': '見守り',
            'mobility_partial_assistance': '一部介助',
            'mobility_full_assistance': '全介助',
            # 移動用具（indoor_mobility_equipment, outdoor_mobility_equipment）
            'equipment_none': 'なし',
            'equipment_wheelchair': '車椅子',
            'equipment_walker': '歩行器',
            'equipment_cane': '杖',
            'equipment_crutches': '松葉杖',
            'equipment_other': 'その他',
            # 食事方法（eating_method）
            'eating_method_oral': '経口摂取',
            'eating_method_tube_oral': '経管栄養+経口摂取',
            'eating_method_tube_only': '経管栄養（胃ろう）',
            'eating_method_tube_nasal': '経管栄養（経鼻）',
            'eating_method_tube_gastronomy': '経管栄養（腸ろう）',
            # 食事動作（eating_assistance）- MOBILITY_CHOICES
            'eating_assistance_independent': '自立',
            'eating_assistance_supervision': '見守り',
            'eating_assistance_partial_assistance': '一部介助',
            'eating_assistance_full_assistance': '全介助',
            # 食事制限（eating_restriction）
            'eating_restriction_yes': 'あり',
            'eating_restriction_no': 'なし',
            'eating_restriction_unknown': '不明',
            # 嚥下（swallowing）
            'swallowing_can_do': 'できる',
            'swallowing_supervision_needed': '見守り等が必要',
            'swallowing_cannot': 'できない',
            # 食事形態（主食）（meal_form_main）
            'meal_main_normal': '普通',
            'meal_main_soft': '軟飯',
            'meal_main_porridge': '全粥',
            'meal_main_paste': 'ペースト',
            # 水分とろみ（water_thickening）
            'water_thickening_yes': 'あり',
            'water_thickening_no': 'なし',
            # 口腔・義歯（natural_teeth_presence, denture_type, denture_location）
            'teeth_yes': 'あり',
            'teeth_no': 'なし',
            'denture_complete': '総義歯',
            'denture_partial': '部分義歯',
            'denture_upper': '上顎',
            'denture_lower': '下顎',
            'denture_both': '上下',
            # 入浴形態（bathing_form）
            'bathing_form_regular_bath': '一般浴',
            'bathing_form_sitting_bath': '寝台浴',
            'bathing_form_shower_bath': 'シャワー浴',
            'bathing_form_chair_bath': 'チェアー浴',
            # 更衣（dressing_upper, dressing_lower）- MOBILITY_CHOICES
            'dressing_independent': '自立',
            'dressing_supervision': '見守り',
            'dressing_partial_assistance': '一部介助',
            'dressing_full_assistance': '全介助',
            # 排泄（urination, defecation）
            'excretion_yes': 'あり',
            'excretion_no': 'なし',
            # 失禁（urinary_incontinence, fecal_incontinence）
            'incontinence_yes': 'あり',
            'incontinence_no': 'なし',
            # 排泄場所（daytime_location, nighttime_location）
            'location_toilet': 'トイレ',
            'location_portable_toilet': 'Pトイレ',
            'location_bed': 'ベッド',
            # IADL（cooking, cleaning, washing, shopping, money_management）- MOBILITY_CHOICES
            'iadl_independent': '自立',
            'iadl_supervision': '見守り',
            'iadl_partial_assistance': '一部介助',
            'iadl_full_assistance': '全介助',
            # 認知症（dementia_presence）
            'dementia_yes': 'あり',
            'dementia_no': 'なし',
            # 認知症の程度（dementia_severity）
            'dementia_mild': '軽度',
            'dementia_moderate': '中等度',
            'dementia_severe': '重度',
            # BPSD症状（bpsd_symptoms）
            'bpsd_none': 'なし',
            'bpsd_persecution_delusion': '被害妄想',
            'bpsd_confabulation': '作話',
            'bpsd_mood_instability': '感情の不安定',
            'bpsd_day_night_reversal': '昼夜逆転',
            'bpsd_home_return_desire': '帰宅願望',
            'bpsd_loud_voice': '大声・奇声',
            'bpsd_violence': '暴力・暴言',
            'bpsd_collection_habit': '収集癖',
            'bpsd_care_resistance': '介護抵抗',
            'bpsd_restlessness': '落ち着きがない',
            'bpsd_wandering': '徘徊',
            'bpsd_destructive_behavior': '破壊行為',
            'bpsd_severe_forgetfulness': 'ひどい物忘れ',
            'bpsd_selfish_behavior': '自分勝手な行動',
            'bpsd_agitation': '不穏',
            'bpsd_depression_tendency': 'うつ傾向',
            # 皮膚疾患（skin_disease）
            'skin_bedsore': '床ずれ',
            'skin_eczema': '湿疹',
            'skin_itching': 'かゆみ',
            'skin_athletes_foot': '水虫',
            'skin_shingles': '帯状疱疹',
            # 感染症（infection）
            'infection_tuberculosis': '結核',
            'infection_pneumonia': '肺炎',
            'infection_hepatitis': '肝炎',
            'infection_scabies': '疥癬',
            'infection_mrsa': 'MRSA',
            # 会話（conversation）
            'conversation_possible': '可能',
            'conversation_unclear': '不明瞭',
            'conversation_somewhat_difficult': 'やや不自由',
            'conversation_completely_impossible': '全くできない',
            'conversation_impossible': '全くできない',
            # 意思疎通（communication）
            'communication_possible': '可能',
            'communication_only_sometimes': 'その場のみ可能',
            # 住居（home_environment）
            'home_family_cohabitation': '家族と同居',
            'home_living_alone': '一人暮らし',
            'home_elderly_household': '高齢世帯',
            'home_daytime_alone': '日中独居',
            'home_two_generation_house': '二世帯住宅',
            'home_other': 'その他',
            # 住宅形態（housing_type）
            'housing_detached_house': '一戸建て',
            'housing_apartment_complex': '集合住宅',
            'housing_public_housing': '公営住宅',
            'housing_condominium': 'マンション',
            'housing_other': 'その他',
            # 住宅所有（housing_ownership）
            'ownership_owned': '所有',
            'ownership_rental': '賃貸',
            'ownership_lodging': '間借り',
            'ownership_other': 'その他',
            # 個室（private_room）
            'room_available': 'あり',
            'room_not_available': 'なし',
            # エアコン（air_conditioning）
            'aircon_available': 'あり',
            'aircon_not_available': 'なし',
            # トイレ（toilet_type）
            'toilet_western': '洋式',
            'toilet_japanese': '和式',
            # 浴室（bathroom）
            'bathroom_available': 'あり',
            'bathroom_not_available': 'なし',
            # 寝具（sleeping_arrangement）
            'sleeping_tatami_floor': '畳・床',
            'sleeping_regular_bed': 'ベッド',
            'sleeping_care_bed': '介護用ベッド',
            'sleeping_other': 'その他',
            # 段差（room_level_difference）
            'level_diff_available': 'あり',
            'level_diff_not_available': 'なし',
            # 住宅改修（housing_modification）
            'modification_completed': 'あり',
            'modification_not_completed': 'なし',
            # 住宅改修の必要性（housing_modification_need）
            'modification_need_needed': 'あり',
            'modification_need_not_needed': 'なし',
            # 視力（vision）
            'vision_normal': '正常',
            'vision_large_letters_ok': '大きい字は可',
            'vision_barely_visible': 'ほぼ見えない',
            'vision_blind': '失明',
            # 聴力（hearing）
            'hearing_normal': '正常',
            'hearing_loud_voice_ok': '大きい声は可',
            'hearing_barely_audible': 'ほぼ聞こえない',
            'hearing_deaf': '聞こえない',
            # 眼鏡等（uses_glasses）
            'glasses_yes': '使用',
            'glasses_no': '未使用',
            # 補聴器等（uses_hearing_aid）
            'hearing_aid_yes': '使用',
            'hearing_aid_no': '未使用',
            # 介護サービス（care_services）
            'service_home_help': '訪問介護',
            'service_visit_bath': '訪問入浴',
            'service_visit_nursing': '訪問看護',
            'service_visit_rehab': '訪問リハビリ',
            'service_day_service': '通所介護',
            'service_day_rehab': '通所リハビリ',
            'service_short_stay': 'ショートステイ',
            'service_small_scale_multi': '小規模多機能',
            # 福祉用具（welfare_equipment）
            'welfare_wheelchair': '車いす',
            'welfare_walker': '車いす付属品',
            'welfare_special_bed': '特殊寝台',
            'welfare_special_bed_accessories': '特殊寝台付属品',
            'welfare_fall_prevention': '床ずれ防止用具',
            'welfare_position_changer': '体位変換器',
            'welfare_walking_aid': '手すり',
            'welfare_slope': 'スロープ',
            'welfare_walking_frame': '歩行器',
            'welfare_walking_support': '歩行補助つえ',
            'welfare_detect_sensor': '排個感知機器',
            'welfare_mobility_lift': '移動用リフト',
            'welfare_automatic_drainage': '自動排泄処理装置',
            # インフォーマルサービス（informal_services）
            'informal_family_support': '家族による支援',
            'informal_neighbor_support': '近隣による支援',
            'informal_volunteer': 'ボランティア',
            'informal_community_group': '地域活動グループ',
            'informal_friend_support': '友人による支援',
            'informal_npo_support': 'NPO団体支援',
            'informal_religious_support': '宗教団体支援',
            'informal_meal_support': '食事支援',
            'informal_excretion_support': '排泄支援',
            'informal_linen_lease': 'リネンリース',
            'informal_laundry': '洗濯',
            'informal_room_cleaning': '居室清掃',
            'informal_sputum_suction': '喀痰吸引',
            'informal_diaper_supply': 'オムツ支給',
            'informal_taxi_voucher': 'タクシー券',
            'informal_massage_voucher': 'マッサージ券',
            'informal_fire_alarm': '火災報知器',
            'informal_auto_fire_extinguisher': '自動消火器',
            'informal_elderly_phone': '老人用電話',
            'informal_bedding_disinfection': '寝具乾燥消毒',
            'informal_induction_cooker': '電磁調理器',
            'informal_emergency_alert': '緊急通報装置',
            'informal_meal_delivery': '配食サービス',
            'informal_other_services': 'その他',
            # 食事用具（eating_utensils）
            'utensil_chopsticks': '箸',
            'utensil_spoon': 'スプーン',
            'utensil_apron': 'エプロン',
            'utensil_assistive': '補助具',
            'utensil_other': 'その他',
            # 排泄用品（excretion_supplies）
            'supply_rehabilitation_pants': 'リハビリパンツ',
            'supply_paper_diaper': '紙おむつ',
            'supply_small_pad': '小パット',
            'supply_large_pad': '大パット',
            # 服薬状況（medication_status）
            'medication_self': '自己管理',
            'medication_family': '家族管理',
            'medication_support': '支援あり',
            'medication_none': '服薬なし',
            # 通院状況（hospital_visit_status）
            'visit_status_regular': '定期通院',
            'visit_status_occasional': '時々通院',
            'visit_status_home_visit': '往診',
            'visit_status_none': '通院なし',
            # 通院方法（hospital_visit_method）
            'visit_method_self': '本人',
            'visit_method_family': '家族',
            'visit_method_care_assistance': '通院乗降介助',
            'visit_method_care_taxi': '介護タクシー',
            # 口腔ケア介助（oral_hygiene_assistance）- MOBILITY_CHOICES
            'oral_assistance_independent': '自立',
            'oral_assistance_supervision': '見守り',
            'oral_assistance_partial_assistance': '一部介助',
            'oral_assistance_full_assistance': '全介助',
            # 入浴介助（bathing_assistance）- MOBILITY_CHOICES
            'bathing_assistance_independent': '自立',
            'bathing_assistance_supervision': '見守り',
            'bathing_assistance_partial_assistance': '一部介助',
            'bathing_assistance_full_assistance': '全介助',
            # 入浴制限（bathing_restriction）
            'bathing_restriction_yes': 'あり',
            'bathing_restriction_no': 'なし',
            # 排泄介助（excretion_assistance）- MOBILITY_CHOICES
            'excretion_assistance_independent': '自立',
            'excretion_assistance_supervision': '見守り',
            'excretion_assistance_partial_assistance': '一部介助',
            'excretion_assistance_full_assistance': '全介助',
        }

        def get_choice_label(value):
            """選択肢の値を表示名に変換"""
            if not value:
                return ''
            # リストや辞書の場合はそのまま返す（変換しない）
            if isinstance(value, (list, dict)):
                return value
            # 文字列の場合のみ変換
            return CHOICE_LABELS.get(value, value)

        def convert_list_to_text(value_list):
            """リスト型の選択肢を表示名のカンマ区切りテキストに変換"""
            if not value_list or not isinstance(value_list, list):
                return ''
            labels = [get_choice_label(v) for v in value_list]
            return '、'.join(labels)

        # セルへの安全な書き込み関数
        def safe_write_cell(cell_ref, value):
            try:
                if cell_ref and value is not None and value != '':
                    # リスト型の場合は空文字列として扱う（書き込まない）
                    if isinstance(value, list):
                        if len(value) == 0:
                            return  # 空リストは書き込まない
                        # リストの場合はカンマ区切り文字列に変換（ただし選択肢の値のままなので、今回はスキップ）
                        return

                    cell = worksheet[cell_ref]

                    # MergedCellの場合、マージ範囲の最初のセルを見つけて書き込み
                    if isinstance(cell, MergedCell):
                        for merged_range in worksheet.merged_cells.ranges:
                            if cell_ref in merged_range:
                                min_col, min_row, max_col, max_row = merged_range.bounds
                                target_cell = worksheet.cell(row=min_row, column=min_col)
                                target_cell.value = value
                                return
                    else:
                        # 数値型の場合、セルのデータタイプを明示的に設定
                        if isinstance(value, (int, float)):
                            cell.value = value
                            cell.data_type = 'n'  # 数値型を明示
                        else:
                            cell.value = value
            except Exception as e:
                print(f"DEBUG: セル {cell_ref} への書き込みエラー (値: {value}, 型: {type(value)}): {str(e)}")

        # クライアント基本情報
        safe_write_cell(coords.get('client_name'), assessment.client.name)
        safe_write_cell(coords.get('client_furigana'), assessment.client.furigana)
        safe_write_cell(coords.get('client_gender'), assessment.client.get_gender_display())
        # 年齢は数値として書き込み
        if assessment.client.age:
            safe_write_cell(coords.get('client_age'), int(assessment.client.age))
        safe_write_cell(coords.get('client_address'), assessment.client.address)
        safe_write_cell(coords.get('client_contact'), assessment.client.phone)
        if assessment.client.birth_date:
            safe_write_cell(coords.get('birth_date'), to_wareki(assessment.client.birth_date))

        # アセスメント基本情報
        safe_write_cell(coords.get('assessment_date'), to_wareki(assessment.assessment_date) if assessment.assessment_date else '')
        safe_write_cell(coords.get('assessor'), assessment.assessor.profile.get_full_name() if assessment.assessor else '')

        # アセスメントの理由（その他の場合は詳細を書き込む）
        if assessment.assessment_type == 'other' and assessment.assessment_type_other:
            safe_write_cell(coords.get('assessment_type'), assessment.assessment_type_other)
        else:
            safe_write_cell(coords.get('assessment_type'), assessment.get_assessment_type_display())

        # 面談場所（その他の場合は詳細を書き込む）
        if assessment.interview_location == 'other' and assessment.interview_location_other:
            safe_write_cell(coords.get('interview_location'), assessment.interview_location_other)
        else:
            safe_write_cell(coords.get('interview_location'), assessment.get_interview_location_display())

        # 保険情報
        # 被保険者番号は数値として書き込み
        if assessment.client.insurance_number:
            try:
                safe_write_cell(coords.get('insurance_number'), int(assessment.client.insurance_number))
            except (ValueError, TypeError):
                safe_write_cell(coords.get('insurance_number'), assessment.client.insurance_number)
        safe_write_cell(coords.get('care_level_official'), assessment.client.get_care_level_display() if assessment.client.care_level else '')
        if assessment.client.certification_date:
            safe_write_cell(coords.get('certification_date'), to_wareki(assessment.client.certification_date))
        if assessment.client.certification_period_start:
            safe_write_cell(coords.get('certification_period_start'), to_wareki(assessment.client.certification_period_start))
        if assessment.client.certification_period_end:
            safe_write_cell(coords.get('certification_period_end'), to_wareki(assessment.client.certification_period_end))
        # 負担割合（「1割負担」→「1割」に変換）
        if assessment.client.care_burden:
            burden_text = assessment.client.care_burden.replace('負担', '')
            safe_write_cell(coords.get('burden_ratio'), burden_text)
        else:
            safe_write_cell(coords.get('burden_ratio'), '')

        # 保険関連情報（利用者モデルから取得）
        client = assessment.client

        # 医療保険
        safe_write_cell(coords.get('medical_insurance'), client.medical_insurance_type)

        # 身体障がい者手帳
        if client.disability_handbook:
            if client.disability_handbook_type:
                safe_write_cell(coords.get('disability_handbook'), f'あり（{client.disability_handbook_type}）')
            else:
                safe_write_cell(coords.get('disability_handbook'), 'あり')
        else:
            safe_write_cell(coords.get('disability_handbook'), 'なし')

        # 難病申請
        if client.difficult_disease:
            safe_write_cell(coords.get('difficult_disease'), 'あり')
        else:
            safe_write_cell(coords.get('difficult_disease'), 'なし')

        # 生活保護
        if client.life_protection:
            safe_write_cell(coords.get('life_protection'), 'あり')
        else:
            safe_write_cell(coords.get('life_protection'), 'なし')

        # 障がい者日常生活自立度・認知症日常生活自立度
        if client.disability_level:
            safe_write_cell(coords.get('disability_level'), client.get_disability_level_display())
        if client.dementia_level:
            safe_write_cell(coords.get('dementia_level'), client.get_dementia_level_display())

        # 家族状況（利用者登録から取得）
        safe_write_cell(coords.get('family_member1_name'), assessment.client.family_name1)
        safe_write_cell(coords.get('family_member1_relation'), assessment.client.get_family_relationship1_display())
        safe_write_cell(coords.get('family_member1_address'), assessment.client.family_address1)
        safe_write_cell(coords.get('family_member1_contact'), assessment.client.family_contact1)
        safe_write_cell(coords.get('family_member1_care'), assessment.client.get_family_care_status1_display())
        safe_write_cell(coords.get('family_member1_living_together'), assessment.client.get_family_living_status1_display())
        safe_write_cell(coords.get('family_member1_job'), assessment.client.get_family_employment1_display())
        safe_write_cell(coords.get('family_member1_notes'), assessment.client.family_notes1)

        safe_write_cell(coords.get('family_member2_name'), assessment.client.family_name2)
        safe_write_cell(coords.get('family_member2_relation'), assessment.client.get_family_relationship2_display())
        safe_write_cell(coords.get('family_member2_address'), assessment.client.family_address2)
        safe_write_cell(coords.get('family_member2_contact'), assessment.client.family_contact2)
        safe_write_cell(coords.get('family_member2_care'), assessment.client.get_family_care_status2_display())
        safe_write_cell(coords.get('family_member2_living_together'), assessment.client.get_family_living_status2_display())
        safe_write_cell(coords.get('family_member2_job'), assessment.client.get_family_employment2_display())
        safe_write_cell(coords.get('family_member2_notes'), assessment.client.family_notes2)

        # 住居状況（居住状況）
        if assessment.living_situation:
            housing = assessment.living_situation
            # 家庭環境
            home_env = housing.get('home_environment', '')
            if home_env:
                if home_env == 'other':
                    other_detail = housing.get('other_home_environment_detail_text', '')
                    if other_detail:
                        safe_write_cell(coords.get('home_environment'), other_detail)
                    else:
                        safe_write_cell(coords.get('home_environment'), get_choice_label(f'home_{home_env}'))
                else:
                    safe_write_cell(coords.get('home_environment'), get_choice_label(f'home_{home_env}'))
            # 住宅形態（エレベーター情報を含む）
            housing_type = housing.get('housing_type', '')
            if housing_type:
                housing_text = ''
                if housing_type == 'other':
                    other_detail = housing.get('other_housing_type_detail_text', '')
                    housing_text = other_detail if other_detail else get_choice_label(f'housing_{housing_type}')
                else:
                    housing_text = get_choice_label(f'housing_{housing_type}')

                # エレベーター情報を追加（一戸建て以外の場合）
                if housing_type != 'detached_house':
                    has_elevator = housing.get('has_elevator', '')
                    if has_elevator == 'yes':
                        housing_text = f'{housing_text}、エレベーター有'
                    elif has_elevator == 'no':
                        housing_text = f'{housing_text}、エレベーター無'

                safe_write_cell(coords.get('housing_type'), housing_text)

            # 住宅権利
            ownership = housing.get('housing_ownership', '')
            if ownership:
                if ownership == 'other':
                    other_detail = housing.get('other_ownership_detail_text', '')
                    if other_detail:
                        safe_write_cell(coords.get('housing_ownership'), other_detail)
                    else:
                        safe_write_cell(coords.get('housing_ownership'), get_choice_label(f'ownership_{ownership}'))
                else:
                    safe_write_cell(coords.get('housing_ownership'), get_choice_label(f'ownership_{ownership}'))
            # 個室
            private_room = housing.get('private_room', '')
            if private_room:
                safe_write_cell(coords.get('private_room'), get_choice_label(f'room_{private_room}'))
            # エアコン
            air_cond = housing.get('air_conditioning', '')
            if air_cond:
                safe_write_cell(coords.get('air_conditioning'), get_choice_label(f'aircon_{air_cond}'))

            # トイレ（手すり、段差情報を含む）
            toilet = housing.get('toilet_type', '')
            if toilet:
                toilet_text = get_choice_label(f'toilet_{toilet}')

                # 手すり情報を追加
                toilet_handrail = housing.get('toilet_handrail', '')
                if toilet_handrail == 'yes':
                    toilet_text = f'{toilet_text}、手すり有'
                elif toilet_handrail == 'no':
                    toilet_text = f'{toilet_text}、手すり無'

                # 段差情報を追加
                toilet_step = housing.get('toilet_step', '')
                if toilet_step == 'yes':
                    toilet_text = f'{toilet_text}、段差有'
                elif toilet_step == 'no':
                    toilet_text = f'{toilet_text}、段差無'

                safe_write_cell(coords.get('toilet_type'), toilet_text)

            # 浴室（手すり、段差情報を含む）
            bathroom = housing.get('bathroom', '')
            if bathroom:
                bathroom_text = get_choice_label(f'bathroom_{bathroom}')

                # 「あり」の場合のみ、手すりと段差情報を追加
                if bathroom == 'available':
                    # 手すり情報を追加
                    bathroom_handrail = housing.get('bathroom_handrail', '')
                    if bathroom_handrail == 'yes':
                        bathroom_text = f'{bathroom_text}、手すり有'
                    elif bathroom_handrail == 'no':
                        bathroom_text = f'{bathroom_text}、手すり無'

                    # 段差情報を追加
                    bathroom_step = housing.get('bathroom_step', '')
                    if bathroom_step == 'yes':
                        bathroom_text = f'{bathroom_text}、段差有'
                    elif bathroom_step == 'no':
                        bathroom_text = f'{bathroom_text}、段差無'

                safe_write_cell(coords.get('bathroom'), bathroom_text)
            # 就寝環境
            sleeping = housing.get('sleeping_arrangement', '')
            if sleeping:
                if sleeping == 'other':
                    other_detail = housing.get('other_sleeping_detail_text', '')
                    if other_detail:
                        safe_write_cell(coords.get('sleeping_arrangement'), other_detail)
                    else:
                        safe_write_cell(coords.get('sleeping_arrangement'), get_choice_label(f'sleeping_{sleeping}'))
                else:
                    safe_write_cell(coords.get('sleeping_arrangement'), get_choice_label(f'sleeping_{sleeping}'))
            # 段差
            level_diff = housing.get('room_level_difference', '')
            if level_diff:
                safe_write_cell(coords.get('room_level_difference'), get_choice_label(f'level_diff_{level_diff}'))
            # 住宅改修
            modification = housing.get('housing_modification', '')
            if modification:
                safe_write_cell(coords.get('housing_modification'), get_choice_label(f'modification_{modification}'))
            # 住宅改修の必要性
            mod_need = housing.get('housing_modification_need', '')
            if mod_need:
                safe_write_cell(coords.get('housing_modification_need'), get_choice_label(f'modification_need_{mod_need}'))
            # 特記事項
            safe_write_cell(coords.get('special_circumstances'), housing.get('special_circumstances', ''))

        # 健康状態
        if assessment.health_status:
            health = assessment.health_status

            # 疾患名と発症日（6件）
            for i in range(1, 7):
                # 疾患名
                disease_name = health.get(f'disease_name_{i}', '')
                safe_write_cell(coords.get(f'disease_name_{i}'), disease_name)

                # 発症日（和暦変換）
                onset_date_str = health.get(f'onset_date_{i}', '')
                if onset_date_str:
                    try:
                        from datetime import datetime
                        onset_date = datetime.strptime(onset_date_str, '%Y-%m-%d').date()
                        safe_write_cell(coords.get(f'onset_date_{i}'), to_wareki(onset_date))
                    except (ValueError, TypeError):
                        # 日付の変換に失敗した場合は元の文字列を書き込む
                        safe_write_cell(coords.get(f'onset_date_{i}'), onset_date_str)

            # 既往歴
            safe_write_cell(coords.get('medical_history'), health.get('medical_history', ''))

            # 特別な医療処置（リストから文字列に変換し、日本語ラベルに変換）
            special_medical_treatment_status = health.get('special_medical_treatment_status', '')
            special_medical_treatment = health.get('special_medical_treatment', [])

            # V28用の詳細テキスト
            if isinstance(special_medical_treatment, list):
                # 特別な医療処置のラベルマッピング（テンプレートのvalueに対応）
                treatment_labels = {
                    'none': 'なし',
                    'iv_management': '点滴の管理',
                    'central_venous_nutrition': '中心静脈栄養',
                    'dialysis': '透析',
                    'stoma_care': 'ストーマの処置',
                    'oxygen_therapy': '酸素療法',
                    'ventilator': '人工呼吸器',
                    'tracheostomy_care': '気管切開の処置',
                    'pain_nursing': '疼痛の看護',
                    'tube_feeding': '経管栄養',
                    'monitor_measurement': 'モニター測定（血圧、心拍、酸素飽和度等）',
                    'pressure_ulcer_care': '褥瘡の処置',
                    'urinary_catheter': '導尿カテーテル',
                }
                treatment_texts = [treatment_labels.get(t, t) for t in special_medical_treatment if t]
                special_medical_treatment_text = '、'.join(treatment_texts) if treatment_texts else ''
            else:
                special_medical_treatment_text = special_medical_treatment

            # V28に詳細を書き込む（なしの場合も「なし」と記載）
            if special_medical_treatment_status == 'none':
                safe_write_cell('V28', 'なし')
            else:
                safe_write_cell('V28', special_medical_treatment_text)

            # I60には「あり」「なし」のみを書き込む
            if special_medical_treatment_status == 'none':
                safe_write_cell('I60', 'なし')
            elif special_medical_treatment_status == 'available':
                safe_write_cell('I60', 'あり（詳細は1ページ参照）')
            else:
                safe_write_cell('I60', '')

            # 主治医情報（病院名と氏名を分けて記載）
            safe_write_cell(coords.get('main_doctor_hospital'), health.get('main_doctor_hospital', ''))
            safe_write_cell(coords.get('main_doctor_name'), health.get('main_doctor_name', ''))

            # 往診医情報（病院名と氏名を分けて記載）
            safe_write_cell(coords.get('visiting_doctor_hospital'), health.get('visiting_doctor_hospital', ''))
            safe_write_cell(coords.get('visiting_doctor_name'), health.get('visiting_doctor_name', ''))

            # かかりつけ医（1-4）全て病院名
            safe_write_cell(coords.get('family_doctor_1'), health.get('family_doctor_hospital_1', ''))
            safe_write_cell(coords.get('family_doctor_2'), health.get('family_doctor_hospital_2', ''))
            safe_write_cell(coords.get('family_doctor_3'), health.get('family_doctor_hospital_3', ''))
            safe_write_cell(coords.get('family_doctor_4'), health.get('family_doctor_hospital_4', ''))

            # 通院情報（通院状況、通院方法、通院情報の詳細をまとめて記載）
            hospital_visit_parts = []

            # 通院状況
            visit_status = health.get('hospital_visit_status', '')
            if visit_status:
                # 接尾辞付きキーで変換
                label = get_choice_label(f'visit_status_{visit_status}')
                hospital_visit_parts.append(f"通院状況：{label}")

            # 通院方法
            visit_method = health.get('hospital_visit_method', '')
            if visit_method:
                # その他の場合は詳細を含める
                if visit_method == 'other':
                    method_other = health.get('hospital_visit_method_other', '')
                    if method_other:
                        hospital_visit_parts.append(f"通院方法：{method_other}")
                    else:
                        hospital_visit_parts.append(f"通院方法：その他")
                else:
                    # 接尾辞付きキーで変換
                    label = get_choice_label(f'visit_method_{visit_method}')
                    hospital_visit_parts.append(f"通院方法：{label}")

            # 1行目を作成
            first_line = '　'.join(hospital_visit_parts) if hospital_visit_parts else ''

            # 通院情報の詳細
            hospital_notes = health.get('medical_institution_notes', '')

            # 結合して出力
            if first_line and hospital_notes:
                full_hospital_visit_text = f"{first_line}\n{hospital_notes}"
            elif first_line:
                full_hospital_visit_text = first_line
            elif hospital_notes:
                full_hospital_visit_text = hospital_notes
            else:
                full_hospital_visit_text = ''

            safe_write_cell(coords.get('hospital_visit_info'), full_hospital_visit_text)

            # アレルギー
            has_allergy = health.get('has_allergy', '')
            allergy_details = health.get('allergy_details', '')

            if has_allergy == 'yes':
                # 「あり」の場合、F37に「あり」、I37に詳細を記載
                safe_write_cell(coords.get('has_allergy'), 'あり')
                safe_write_cell(coords.get('allergy_details'), allergy_details)
            elif has_allergy == 'no':
                # 「なし」の場合
                safe_write_cell(coords.get('has_allergy'), 'なし')
            elif has_allergy:
                # その他の値の場合（念のため）
                safe_write_cell(coords.get('has_allergy'), has_allergy)

            # 服薬情報（服薬状況、眠剤、下剤、服薬内容をまとめて記載）
            medication_parts = []

            # 服薬状況
            medication_status = health.get('medication_status', '')
            if medication_status:
                medication_parts.append(f"服薬状況：{get_choice_label(f'medication_{medication_status}')}")

            # 眠剤の有無
            has_sleeping = health.get('has_sleeping_medication', '')
            if has_sleeping == 'yes':
                medication_parts.append('眠剤：あり')
            elif has_sleeping == 'no':
                medication_parts.append('眠剤：なし')

            # 下剤の有無
            has_laxative = health.get('has_laxative', '')
            if has_laxative == 'yes':
                medication_parts.append('下剤：あり')
            elif has_laxative == 'no':
                medication_parts.append('下剤：なし')

            # 1行目を作成
            first_line = '　'.join(medication_parts) if medication_parts else ''

            # 服薬内容
            medication_content = health.get('medication_content', '')

            # 結合して出力
            if first_line and medication_content:
                full_medication_text = f"{first_line}\n{medication_content}"
            elif first_line:
                full_medication_text = first_line
            elif medication_content:
                full_medication_text = medication_content
            else:
                full_medication_text = ''

            safe_write_cell(coords.get('medication_content'), full_medication_text)

        # サービス利用状況
        if assessment.services:
            service = assessment.services
            # 介護サービス（リストの各要素にservice_プレフィックスを追加）
            care_services_list = service.get('care_services', [])
            if care_services_list:
                care_labels = [get_choice_label(f'service_{s}') for s in care_services_list]
                safe_write_cell(coords.get('care_services'), '、'.join(care_labels))
            # 福祉用具（リストの各要素にwelfare_プレフィックスを追加）
            welfare_list = service.get('welfare_equipment', [])
            if welfare_list:
                welfare_labels = [get_choice_label(f'welfare_{w}') for w in welfare_list]
                safe_write_cell(coords.get('welfare_equipment'), '、'.join(welfare_labels))
            safe_write_cell(coords.get('other_services'), service.get('other_services', ''))
            # インフォーマルサービス（リストの各要素にinformal_プレフィックスを追加）
            informal_list = service.get('informal_services', [])
            if informal_list:
                informal_labels = []
                for i in informal_list:
                    label = get_choice_label(f'informal_{i}')
                    # 「その他」の場合、詳細を追加
                    if i == 'other_services':
                        other_detail = service.get('other_services_detail_text', '')
                        if other_detail:
                            label = other_detail
                    informal_labels.append(label)
                safe_write_cell(coords.get('informal_services'), '、'.join(informal_labels))
            safe_write_cell(coords.get('social_relationships'), service.get('social_relationships', ''))

        # 本人・家族の希望等（基本情報に含まれる）
        if assessment.basic_info:
            info = assessment.basic_info
            safe_write_cell(coords.get('personal_hopes'), info.get('personal_hopes', ''))
            safe_write_cell(coords.get('family_hopes'), info.get('family_hopes', ''))
            safe_write_cell(coords.get('life_history'), info.get('life_history', ''))
            # 特記・備考（住居備考があれば追記）
            notes_parts = []
            notes_text = info.get('notes', '')
            if notes_text:
                notes_parts.append(notes_text)
            if assessment.living_situation:
                housing_notes = assessment.living_situation.get('housing_notes', '')
                if housing_notes:
                    notes_parts.append(f'【住居備考】{housing_notes}')
            safe_write_cell(coords.get('notes'), '\n'.join(notes_parts) if notes_parts else '')

        # 身体状況
        if assessment.physical_status:
            physical = assessment.physical_status

            # 皮膚疾患
            skin_disease_presence = assessment.health_status.get('has_skin_disease', '')
            if skin_disease_presence == 'no':
                safe_write_cell(coords.get('skin_disease'), 'なし')
            elif skin_disease_presence == 'yes':
                skin_disease_list = assessment.health_status.get('skin_disease', [])
                if skin_disease_list:
                    skin_labels = []
                    for item in skin_disease_list:
                        if item == 'other':
                            other_text = assessment.health_status.get('skin_disease_other', '')
                            if other_text:
                                skin_labels.append(other_text)
                        else:
                            skin_labels.append(get_choice_label(f'skin_{item}'))
                    safe_write_cell(coords.get('skin_disease'), '、'.join(skin_labels))

            # 感染症
            infection_presence = assessment.health_status.get('infection_presence', '')
            if infection_presence == 'no':
                safe_write_cell(coords.get('infection_status'), 'なし')
            elif infection_presence == 'yes':
                infection_list = assessment.health_status.get('infection', [])
                if infection_list:
                    infection_labels = []
                    for item in infection_list:
                        if item == 'other':
                            other_text = assessment.health_status.get('infection_other_text', '')
                            if other_text:
                                infection_labels.append(other_text)
                        else:
                            infection_labels.append(get_choice_label(f'infection_{item}'))
                    safe_write_cell(coords.get('infection_status'), '、'.join(infection_labels))
            safe_write_cell(coords.get('paralysis_location'), physical.get('paralysis_location', ''))
            safe_write_cell(coords.get('pain_location'), physical.get('pain_location', ''))
            # 身長・体重は数値として書き込み
            height = physical.get('height', '')
            if height:
                try:
                    safe_write_cell(coords.get('height'), float(height))
                except (ValueError, TypeError):
                    safe_write_cell(coords.get('height'), height)
            weight = physical.get('weight', '')
            if weight:
                try:
                    safe_write_cell(coords.get('weight'), float(weight))
                except (ValueError, TypeError):
                    safe_write_cell(coords.get('weight'), weight)
            vision = physical.get('vision', '')
            if vision:
                safe_write_cell(coords.get('vision'), get_choice_label(f'vision_{vision}'))
            # 眼鏡等はhealth_statusに保存されている
            uses_glasses = assessment.health_status.get('uses_glasses', '')
            if uses_glasses:
                safe_write_cell(coords.get('uses_glasses'), get_choice_label(f'glasses_{uses_glasses}'))
            hearing = physical.get('hearing', '')
            if hearing:
                safe_write_cell(coords.get('hearing'), get_choice_label(f'hearing_{hearing}'))
            # 補聴器等はhealth_statusに保存されている
            uses_hearing_aid = assessment.health_status.get('uses_hearing_aid', '')
            if uses_hearing_aid:
                safe_write_cell(coords.get('uses_hearing_aid'), get_choice_label(f'hearing_aid_{uses_hearing_aid}'))
            # 身体状況メモ（麻痺・痛みの詳細があれば追記）
            physical_notes_parts = []
            physical_notes_text = physical.get('physical_notes', '')
            if physical_notes_text:
                physical_notes_parts.append(physical_notes_text)
            paralysis_pain_details = physical.get('paralysis_pain_details', '')
            if paralysis_pain_details:
                physical_notes_parts.append(f'【麻痺・痛み】{paralysis_pain_details}')
            safe_write_cell(coords.get('physical_notes'), '\n'.join(physical_notes_parts) if physical_notes_parts else '')

        # 基本動作
        if assessment.basic_activities:
            activity = assessment.basic_activities
            # 寝返り・起き上がり・立ち上がり（basic_*）
            turning = activity.get('turning_over', '')
            if turning:
                safe_write_cell(coords.get('turning_over'), get_choice_label(f'basic_{turning}'))
            getting_up = activity.get('getting_up', '')
            if getting_up:
                safe_write_cell(coords.get('getting_up'), get_choice_label(f'basic_{getting_up}'))
            standing_up = activity.get('standing_up', '')
            if standing_up:
                safe_write_cell(coords.get('standing_up'), get_choice_label(f'basic_{standing_up}'))
            # 座位（sitting_*）
            sitting = activity.get('sitting', '')
            if sitting:
                safe_write_cell(coords.get('sitting'), get_choice_label(f'sitting_{sitting}'))
            # 立位（standing_*）
            standing = activity.get('standing', '')
            if standing:
                safe_write_cell(coords.get('standing'), get_choice_label(f'standing_{standing}'))
            # 移乗・移動（mobility_*）
            transfer = activity.get('transfer', '')
            if transfer:
                safe_write_cell(coords.get('transfer'), get_choice_label(f'mobility_{transfer}'))
            indoor = activity.get('indoor_mobility', '')
            if indoor:
                safe_write_cell(coords.get('indoor_mobility'), get_choice_label(f'mobility_{indoor}'))
            outdoor = activity.get('outdoor_mobility', '')
            if outdoor:
                safe_write_cell(coords.get('outdoor_mobility'), get_choice_label(f'mobility_{outdoor}'))
            # 移動用具（equipment_*）
            indoor_eq = activity.get('indoor_mobility_equipment', '')
            if indoor_eq:
                safe_write_cell(coords.get('indoor_mobility_equipment'), get_choice_label(f'equipment_{indoor_eq}'))
            outdoor_eq = activity.get('outdoor_mobility_equipment', '')
            if outdoor_eq:
                safe_write_cell(coords.get('outdoor_mobility_equipment'), get_choice_label(f'equipment_{outdoor_eq}'))
            safe_write_cell(coords.get('basic_activity_notes'), activity.get('basic_activity_notes', ''))

        # ADL
        if assessment.adl:
            adl = assessment.adl
            # 食事
            eating_method = adl.get('eating_method', '')
            if eating_method:
                safe_write_cell(coords.get('eating_method'), get_choice_label(f'eating_method_{eating_method}'))
            eating_assist = adl.get('eating_assistance', '')
            if eating_assist:
                safe_write_cell(coords.get('eating_assistance'), get_choice_label(f'eating_assistance_{eating_assist}'))
            swallowing = adl.get('swallowing', '')
            if swallowing:
                safe_write_cell(coords.get('swallowing'), get_choice_label(f'swallowing_{swallowing}'))
            meal_main = adl.get('meal_form_main', '')
            if meal_main:
                safe_write_cell(coords.get('meal_form_main'), get_choice_label(f'meal_main_{meal_main}'))

            # 副食の変換
            meal_side = adl.get('meal_form_side', '')
            meal_side_labels = {
                'normal': '普通',
                'soft': '一口大',
                'minced': 'キザミ',
                'paste': 'ペースト',
                'paste_form': 'ペースト',
            }
            if meal_side:
                safe_write_cell(coords.get('meal_form_side'), meal_side_labels.get(meal_side, meal_side))

            water_thick = adl.get('water_thickening', '')
            if water_thick:
                safe_write_cell(coords.get('water_thickening'), get_choice_label(f'water_thickening_{water_thick}'))
            eating_restrict = adl.get('eating_restriction', '')
            if eating_restrict:
                safe_write_cell(coords.get('eating_restriction'), get_choice_label(f'eating_restriction_{eating_restrict}'))

            # 食事用具（リストの各要素にutensil_プレフィックスを追加）
            utensils_list = adl.get('eating_utensils', [])
            if utensils_list:
                utensils_labels = []
                for u in utensils_list:
                    label = get_choice_label(f'utensil_{u}')
                    # 「その他」の場合、詳細を追加
                    if u == 'other':
                        other_detail = adl.get('eating_utensils_other_detail', '')
                        if other_detail:
                            label = other_detail
                    utensils_labels.append(label)
                safe_write_cell(coords.get('eating_utensils'), '、'.join(utensils_labels))
            safe_write_cell(coords.get('eating_notes'), adl.get('eating_notes', ''))

            # 口腔
            oral_assist = adl.get('oral_hygiene_assistance', '')
            if oral_assist:
                safe_write_cell(coords.get('oral_hygiene_assistance'), get_choice_label(f'oral_assistance_{oral_assist}'))
            teeth = adl.get('natural_teeth_presence', '')
            if teeth:
                safe_write_cell(coords.get('natural_teeth_presence'), get_choice_label(f'teeth_{teeth}'))
            denture_type = adl.get('denture_type', '')
            if denture_type:
                safe_write_cell(coords.get('denture_type'), get_choice_label(f'denture_{denture_type}'))
            denture_loc = adl.get('denture_location', '')
            if denture_loc:
                safe_write_cell(coords.get('denture_location'), get_choice_label(f'denture_{denture_loc}'))
            safe_write_cell(coords.get('oral_notes'), adl.get('oral_notes', ''))

            # 入浴・更衣
            bathing_assist = adl.get('bathing_assistance', '')
            if bathing_assist:
                safe_write_cell(coords.get('bathing_assistance'), get_choice_label(f'bathing_assistance_{bathing_assist}'))
            bathing_form = adl.get('bathing_form', '')
            if bathing_form:
                safe_write_cell(coords.get('bathing_form'), get_choice_label(f'bathing_form_{bathing_form}'))
            bathing_restrict = adl.get('bathing_restriction', '')
            if bathing_restrict:
                safe_write_cell(coords.get('bathing_restriction'), get_choice_label(f'bathing_restriction_{bathing_restrict}'))
            dressing_up = adl.get('dressing_upper', '')
            if dressing_up:
                safe_write_cell(coords.get('dressing_upper'), get_choice_label(f'dressing_{dressing_up}'))
            dressing_low = adl.get('dressing_lower', '')
            if dressing_low:
                safe_write_cell(coords.get('dressing_lower'), get_choice_label(f'dressing_{dressing_low}'))
            safe_write_cell(coords.get('bathing_notes'), adl.get('bathing_notes', ''))

            # 排泄
            excretion_assist = adl.get('excretion_assistance', '')
            if excretion_assist:
                safe_write_cell(coords.get('excretion_assistance'), get_choice_label(f'excretion_assistance_{excretion_assist}'))
            urination = adl.get('urination', '')
            if urination:
                safe_write_cell(coords.get('urination'), get_choice_label(f'excretion_{urination}'))
            urinary_incon = adl.get('urinary_incontinence', '')
            if urinary_incon:
                urinary_label = get_choice_label(f'incontinence_{urinary_incon}')
                # 「あり」の場合、詳細（頻度）を追加
                if urinary_incon == 'yes':
                    urinary_freq = adl.get('urinary_incontinence_frequency', '')
                    if urinary_freq:
                        urinary_label = f'{urinary_label}（{urinary_freq}）'
                safe_write_cell(coords.get('urinary_incontinence'), urinary_label)
            defecation = adl.get('defecation', '')
            if defecation:
                safe_write_cell(coords.get('defecation'), get_choice_label(f'excretion_{defecation}'))
            fecal_incon = adl.get('fecal_incontinence', '')
            if fecal_incon:
                fecal_label = get_choice_label(f'incontinence_{fecal_incon}')
                # 「あり」の場合、詳細（頻度）を追加
                if fecal_incon == 'yes':
                    fecal_freq = adl.get('fecal_incontinence_frequency', '')
                    if fecal_freq:
                        fecal_label = f'{fecal_label}（{fecal_freq}）'
                safe_write_cell(coords.get('fecal_incontinence'), fecal_label)

            # 排泄場所（リストの各要素にlocation_プレフィックスを追加）
            daytime_loc_list = adl.get('daytime_location', [])
            if daytime_loc_list:
                daytime_labels = [get_choice_label(f'location_{loc}') for loc in daytime_loc_list]
                safe_write_cell(coords.get('daytime_location'), '、'.join(daytime_labels))
            nighttime_loc_list = adl.get('nighttime_location', [])
            if nighttime_loc_list:
                nighttime_labels = [get_choice_label(f'location_{loc}') for loc in nighttime_loc_list]
                safe_write_cell(coords.get('nighttime_location'), '、'.join(nighttime_labels))

            # 排泄用品（リストの各要素にsupply_プレフィックスを追加）
            supplies_list = adl.get('excretion_supplies', [])
            if supplies_list:
                supplies_labels = [get_choice_label(f'supply_{s}') for s in supplies_list]
                safe_write_cell(coords.get('excretion_supplies'), '、'.join(supplies_labels))
            safe_write_cell(coords.get('excretion_notes'), adl.get('excretion_notes', ''))

        # IADL
        if assessment.iadl:
            iadl = assessment.iadl
            cooking = iadl.get('cooking', '')
            if cooking:
                safe_write_cell(coords.get('cooking'), get_choice_label(f'iadl_{cooking}'))
            washing = iadl.get('washing', '')
            if washing:
                safe_write_cell(coords.get('washing'), get_choice_label(f'iadl_{washing}'))
            money = iadl.get('money_management', '')
            if money:
                safe_write_cell(coords.get('money_management'), get_choice_label(f'iadl_{money}'))
            cleaning = iadl.get('cleaning', '')
            if cleaning:
                safe_write_cell(coords.get('cleaning'), get_choice_label(f'iadl_{cleaning}'))
            shopping = iadl.get('shopping', '')
            if shopping:
                safe_write_cell(coords.get('shopping'), get_choice_label(f'iadl_{shopping}'))
            safe_write_cell(coords.get('iadl_notes'), iadl.get('iadl_notes', ''))

        # 認知機能
        if assessment.cognitive_function:
            cognitive = assessment.cognitive_function
            dementia_pres = cognitive.get('dementia_presence', '')
            if dementia_pres:
                safe_write_cell(coords.get('dementia_presence'), get_choice_label(f'dementia_{dementia_pres}'))
            dementia_sev = cognitive.get('dementia_severity', '')
            if dementia_sev:
                safe_write_cell(coords.get('dementia_severity'), get_choice_label(f'dementia_{dementia_sev}'))
            # BPSD症状
            bpsd_presence = cognitive.get('bpsd_presence', '')
            if bpsd_presence == 'no':
                safe_write_cell(coords.get('bpsd_symptoms'), 'なし')
            elif bpsd_presence == 'yes':
                bpsd_list = cognitive.get('bpsd_symptoms', [])
                if bpsd_list:
                    bpsd_labels = [get_choice_label(f'bpsd_{symptom}') for symptom in bpsd_list]
                    safe_write_cell(coords.get('bpsd_symptoms'), '、'.join(bpsd_labels))
            conversation = cognitive.get('conversation', '')
            if conversation:
                safe_write_cell(coords.get('conversation'), get_choice_label(f'conversation_{conversation}'))
            communication = cognitive.get('communication', '')
            if communication:
                safe_write_cell(coords.get('communication'), get_choice_label(f'communication_{communication}'))
            # 認知機能メモ（認知症詳細があれば追記）
            cognitive_notes_parts = []
            cognitive_notes_text = cognitive.get('cognitive_notes', '')
            if cognitive_notes_text:
                cognitive_notes_parts.append(cognitive_notes_text)
            dementia_details = cognitive.get('dementia_details', '')
            if dementia_details:
                cognitive_notes_parts.append(f'【認知症詳細】{dementia_details}')
            safe_write_cell(coords.get('cognitive_notes'), '\n'.join(cognitive_notes_parts) if cognitive_notes_parts else '')

        # HTTPレスポンスの準備
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="{assessment.client.name}_assessment.xlsx"'

        # Excelファイルを保存
        workbook.save(response)

        return response

    except Exception as e:
        print(f"ERROR: Excel出力エラー: {str(e)}")
        import traceback
        traceback.print_exc()
        raise


@login_required
def assessment_excel_export(request, pk):
    """アセスメント詳細画面からのExcel出力"""
    assessment = get_object_or_404(Assessment, pk=pk)

    try:
        return generate_assessment_excel(assessment)
    except Exception as e:
        messages.error(request, f'Excel出力中にエラーが発生しました: {str(e)}')
        return redirect('client_detail', pk=assessment.client.pk)


@login_required
def assessment_delete(request, pk):
    """アセスメント削除"""
    if request.method == 'POST':
        assessment = get_object_or_404(Assessment, pk=pk)
        client_pk = assessment.client.pk
        assessment.delete()
        # 削除成功メッセージをセッションに保存（警告色で表示）
        messages.warning(request, 'アセスメントを削除しました')
        return JsonResponse({'success': True, 'message': 'アセスメントを削除しました'})
    return JsonResponse({'success': False, 'message': '不正なリクエストです'}, status=400)
