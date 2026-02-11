from django import forms
from django.contrib.auth.models import User
from .models import Assessment
from clients.models import Client


class AssessmentForm(forms.ModelForm):
    class Meta:
        model = Assessment
        fields = [
            'client', 'assessment_date', 'assessment_type', 'interview_location', 
            'general_assessment', 'support_goals', 'status'
        ]
        
        widgets = {
            'client': forms.Select(attrs={'class': 'form-select'}),
            'assessment_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'assessment_type': forms.Select(attrs={'class': 'form-select'}),
            'interview_location': forms.Select(attrs={'class': 'form-select'}),
            'general_assessment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'support_goals': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # 必須フィールドの設定
        required_fields = ['client', 'assessment_date', 'assessment_type', 'interview_location']
        for field_name in required_fields:
            if field_name in self.fields:
                self.fields[field_name].widget.attrs['required'] = True


class DetailedAssessmentForm(forms.Form):
    """詳細なアセスメント項目のフォーム"""

    # アセスメント基本情報
    created_date = forms.DateField(
        label='作成日',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        required=False
    )
    creator = forms.CharField(
        label='作成者',
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),
        required=False
    )
    assessment_type = forms.CharField(
        label='アセスメント理由',
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False
    )
    assessment_type_other = forms.CharField(
        label='その他のアセスメント理由',
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
        required=False
    )
    interview_location = forms.CharField(
        label='面談場所',
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False
    )
    interview_location_other = forms.CharField(
        label='その他の面談場所',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )

    # 基本情報
    life_history = forms.CharField(
        label='生活歴',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        required=False
    )
    personal_hopes = forms.CharField(
        label='本人の希望',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        required=False
    )
    family_hopes = forms.CharField(
        label='家族の希望',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        required=False
    )
    
    # 保険情報
    CARE_LEVEL_CHOICES = [
        ('', '選択してください'),
        ('independent', '自立'),
        ('support1', '要支援1'),
        ('support2', '要支援2'),
        ('care1', '要介護1'),
        ('care2', '要介護2'),
        ('care3', '要介護3'),
        ('care4', '要介護4'),
        ('care5', '要介護5'),
        ('J1', 'J1'),
        ('J2', 'J2'),
        ('A1', 'A1'),
        ('A2', 'A2'),
        ('B1', 'B1'),
        ('B2', 'B2'),
        ('C1', 'C1'),
        ('C2', 'C2'),
    ]
    
    care_level = forms.ChoiceField(
        label='障がい者日常生活自立度',
        choices=CARE_LEVEL_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False
    )
    
    DEMENTIA_LEVEL_CHOICES = [
        ('', '選択してください'),
        ('independent', '自立'),
        ('I', 'I'),
        ('IIa', 'IIa'),
        ('IIb', 'IIb'),
        ('IIIa', 'IIIa'),
        ('IIIb', 'IIIb'),
        ('IV', 'IV'),
        ('M', 'M'),
    ]
    
    dementia_level = forms.ChoiceField(
        label='認知症日常生活自立度',
        choices=DEMENTIA_LEVEL_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False
    )
    
    burden_ratio = forms.ChoiceField(
        label='負担割合',
        choices=[('', '選択してください'), ('1', '1割負担'), ('2', '2割負担'), ('3', '3割負担')],
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False
    )
    
    medical_insurance = forms.CharField(
        label='医療保険',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )
    
    disability_handbook = forms.BooleanField(
        label='身体障がい者手帳の有無',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        required=False
    )
    
    difficulty_certificate = forms.BooleanField(
        label='難病申請',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        required=False
    )
    
    life_protection = forms.BooleanField(
        label='生活保護',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        required=False
    )
    
    # 家族状況
    family_member1 = forms.CharField(
        label='家族氏名-1',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )
    
    family_member2 = forms.CharField(
        label='家族氏名-2',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )
    
    # 居住状況
    HOUSEHOLD_TYPE_CHOICES = [
        ('', '選択してください'),
        ('family_together', '家族同居'),
        ('single', '一人暮らし'),
        ('elderly', '高齢所帯'),
        ('day_alone', '日中独居'),
        ('three_generation', '三世帯住宅'),
    ]
    
    household_type = forms.ChoiceField(
        label='家庭環境',
        choices=HOUSEHOLD_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False
    )
    
    HOME_ENVIRONMENT_CHOICES = [
        ('family_cohabitation', '家族と同居'),
        ('living_alone', '一人暮らし'),
        ('elderly_household', '高齢世帯'),
        ('daytime_alone', '日中独居'),
        ('two_generation_house', '二世帯住宅'),
        ('other', 'その他'),
    ]

    home_environment = forms.ChoiceField(
        label='家庭環境',
        choices=HOME_ENVIRONMENT_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'btn-check'}),
        required=False
    )

    HOUSING_TYPE_CHOICES = [
        ('detached_house', '一戸建て'),
        ('apartment_complex', '集合住宅'),
        ('public_housing', '公営住宅'),
        ('condominium', 'マンション'),
        ('other', 'その他'),
    ]

    housing_type = forms.ChoiceField(
        label='住宅形態',
        choices=HOUSING_TYPE_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'btn-check'}),
        required=False
    )

    HOUSING_OWNERSHIP_CHOICES = [
        ('owned', '所有'),
        ('rental', '賃貸'),
        ('lodging', '間借り'),
        ('other', 'その他'),
    ]

    housing_ownership = forms.ChoiceField(
        label='住宅権利',
        choices=HOUSING_OWNERSHIP_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'btn-check'}),
        required=False
    )
    
    PRIVATE_ROOM_CHOICES = [
        ('available', 'あり'),
        ('not_available', 'なし'),
    ]

    private_room = forms.ChoiceField(
        label='専用居室',
        choices=PRIVATE_ROOM_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'btn-check'}),
        required=False
    )

    AIR_CONDITIONING_CHOICES = [
        ('available', 'あり'),
        ('not_available', 'なし'),
    ]

    air_conditioning = forms.ChoiceField(
        label='冷暖房',
        choices=AIR_CONDITIONING_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'btn-check'}),
        required=False
    )

    TOILET_TYPE_CHOICES = [
        ('western', '洋式'),
        ('japanese', '和式'),
    ]

    toilet_type = forms.ChoiceField(
        label='トイレ',
        choices=TOILET_TYPE_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'btn-check'}),
        required=False
    )

    BATHROOM_CHOICES = [
        ('available', 'あり'),
        ('not_available', 'なし'),
    ]

    bathroom = forms.ChoiceField(
        label='浴室',
        choices=BATHROOM_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'btn-check'}),
        required=False
    )

    SLEEPING_ARRANGEMENT_CHOICES = [
        ('tatami_floor', '畳・床'),
        ('regular_bed', 'ベッド'),
        ('care_bed', '介護用ベッド'),
        ('other', 'その他'),
    ]

    sleeping_arrangement = forms.ChoiceField(
        label='就寝環境',
        choices=SLEEPING_ARRANGEMENT_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'btn-check'}),
        required=False
    )

    other_sleeping_detail_text = forms.CharField(
        label='その他の就寝環境',
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
        required=False
    )

    other_home_environment_detail_text = forms.CharField(
        label='その他の家庭環境',
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
        required=False
    )

    other_housing_type_detail_text = forms.CharField(
        label='その他の住宅形態',
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
        required=False
    )

    other_ownership_detail_text = forms.CharField(
        label='その他の住宅権利',
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
        required=False
    )

    ROOM_LEVEL_DIFFERENCE_CHOICES = [
        ('available', 'あり'),
        ('not_available', 'なし'),
    ]

    room_level_difference = forms.ChoiceField(
        label='居室段差',
        choices=ROOM_LEVEL_DIFFERENCE_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'btn-check'}),
        required=False
    )

    HOUSING_MODIFICATION_CHOICES = [
        ('completed', 'あり'),
        ('not_completed', 'なし'),
    ]

    housing_modification = forms.ChoiceField(
        label='住宅改修',
        choices=HOUSING_MODIFICATION_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'btn-check'}),
        required=False
    )

    HOUSING_MODIFICATION_NEED_CHOICES = [
        ('needed', 'あり'),
        ('not_needed', 'なし'),
    ]

    housing_modification_need = forms.ChoiceField(
        label='住宅改修の必要性',
        choices=HOUSING_MODIFICATION_NEED_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'btn-check'}),
        required=False
    )

    housing_notes = forms.CharField(
        label='住居環境の詳細',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        required=False
    )

    BEDDING_TYPE_CHOICES = [
        ('', '選択してください'),
        ('futon', '畳・床'),
        ('bed', 'ベッド'),
        ('reclining', 'リクライニングベッド'),
    ]
    
    bedding_type = forms.ChoiceField(
        label='就寝',
        choices=BEDDING_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False
    )
    
    has_stairs = forms.BooleanField(
        label='居室段差',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        required=False
    )
    
    home_renovation_needed = forms.BooleanField(
        label='住宅改修',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        required=False
    )
    
    home_renovation_necessity = forms.BooleanField(
        label='住宅改修の必要性',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        required=False
    )
    
    # サービス利用状況
    CARE_SERVICES_CHOICES = [
        ('home_help', '訪問介護'),
        ('visit_bath', '訪問入浴'),
        ('visit_nursing', '訪問看護'),
        ('visit_rehab', '訪問リハビリ'),
        ('day_service', '通所介護'),
        ('day_rehab', '通所リハビリ'),
        ('short_stay', 'ショートステイ'),
        ('small_scale_multi', '小規模多機能'),
    ]

    care_services = forms.MultipleChoiceField(
        label='介護サービス',
        choices=CARE_SERVICES_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False
    )
    
    WELFARE_EQUIPMENT_CHOICES = [
        ('wheelchair', '車いす'),
        ('walker', '車いす付属品'),
        ('special_bed', '特殊寝台'),
        ('special_bed_accessories', '特殊寝台付属品'),
        ('fall_prevention', '床ずれ防止用具'),
        ('position_changer', '体位変換器'),
        ('walking_aid', '手すり'),
        ('slope', 'スロープ'),
        ('walking_frame', '歩行器'),
        ('walking_support', '歩行補助つえ'),
        ('detect_sensor', '排個感知機器'),
        ('mobility_lift', '移動用リフト'),
        ('automatic_drainage', '自動排泄処理装置'),
    ]
    
    welfare_equipment = forms.MultipleChoiceField(
        label='福祉用具',
        choices=WELFARE_EQUIPMENT_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False
    )
    
    other_services = forms.CharField(
        label='上記以外のサービス',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        required=False
    )

    INFORMAL_SERVICES_CHOICES = [
        # 一般的支援
        ('family_support', '家族による支援'),
        ('neighbor_support', '近隣による支援'),
        ('volunteer', 'ボランティア'),
        ('community_group', '地域活動グループ'),
        ('friend_support', '友人による支援'),
        ('npo_support', 'NPO団体支援'),
        ('religious_support', '宗教団体支援'),
        # アールビーサポート自費サービス
        ('meal_support', '食事支援'),
        ('excretion_support', '排泄支援'),
        ('linen_lease', 'リネンリース'),
        ('laundry', '洗濯'),
        ('room_cleaning', '居室清掃'),
        ('sputum_suction', '喀痰吸引'),
        # 市独自サービス
        ('diaper_supply', 'オムツ支給'),
        ('taxi_voucher', 'タクシー券'),
        ('massage_voucher', 'マッサージ券'),
        # その他サービス
        ('fire_alarm', '火災報知器'),
        ('auto_fire_extinguisher', '自動消火器'),
        ('elderly_phone', '老人用電話'),
        ('bedding_disinfection', '寝具乾燥消毒'),
        ('induction_cooker', '電磁調理器'),
        ('emergency_alert', '緊急通報装置'),
        ('meal_delivery', '配食サービス'),
        ('other_services', 'その他'),
    ]

    informal_services = forms.MultipleChoiceField(
        label='インフォーマルサービス',
        choices=INFORMAL_SERVICES_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False
    )

    other_services_detail_text = forms.CharField(
        label='その他サービスの詳細',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        required=False
    )

    social_relationships = forms.CharField(
        label='社会との関り',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        required=False
    )
    
    # 健康状態
    disease_name_1 = forms.CharField(
        label='疾患名1',
        widget=forms.TextInput(attrs={'class': 'form-control mb-2 disease-field', 'data-field': '1', 'placeholder': '疾患名1'}),
        required=False
    )
    disease_name_2 = forms.CharField(
        label='疾患名2',
        widget=forms.TextInput(attrs={'class': 'form-control mb-2 disease-field', 'data-field': '2', 'placeholder': '疾患名2'}),
        required=False
    )
    disease_name_3 = forms.CharField(
        label='疾患名3',
        widget=forms.TextInput(attrs={'class': 'form-control mb-2 disease-field', 'data-field': '3', 'placeholder': '疾患名3'}),
        required=False
    )
    disease_name_4 = forms.CharField(
        label='疾患名4',
        widget=forms.TextInput(attrs={'class': 'form-control mb-2 disease-field', 'data-field': '4', 'placeholder': '疾患名4'}),
        required=False
    )
    disease_name_5 = forms.CharField(
        label='疾患名5',
        widget=forms.TextInput(attrs={'class': 'form-control mb-2 disease-field', 'data-field': '5', 'placeholder': '疾患名5'}),
        required=False
    )
    disease_name_6 = forms.CharField(
        label='疾患名6',
        widget=forms.TextInput(attrs={'class': 'form-control disease-field', 'data-field': '6', 'placeholder': '疾患名6'}),
        required=False
    )

    onset_date_1 = forms.DateField(
        label='発症日1',
        widget=forms.DateInput(attrs={'class': 'form-control mb-2 onset-field', 'data-field': '1', 'type': 'date'}),
        required=False
    )
    onset_date_2 = forms.DateField(
        label='発症日2',
        widget=forms.DateInput(attrs={'class': 'form-control mb-2 onset-field', 'data-field': '2', 'type': 'date'}),
        required=False
    )
    onset_date_3 = forms.DateField(
        label='発症日3',
        widget=forms.DateInput(attrs={'class': 'form-control mb-2 onset-field', 'data-field': '3', 'type': 'date'}),
        required=False
    )
    onset_date_4 = forms.DateField(
        label='発症日4',
        widget=forms.DateInput(attrs={'class': 'form-control mb-2 onset-field', 'data-field': '4', 'type': 'date'}),
        required=False
    )
    onset_date_5 = forms.DateField(
        label='発症日5',
        widget=forms.DateInput(attrs={'class': 'form-control mb-2 onset-field', 'data-field': '5', 'type': 'date'}),
        required=False
    )
    onset_date_6 = forms.DateField(
        label='発症日6',
        widget=forms.DateInput(attrs={'class': 'form-control onset-field', 'data-field': '6', 'type': 'date'}),
        required=False
    )


    medical_history = forms.CharField(
        label='既往歴',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        required=False
    )

    health_basic_info_details = forms.CharField(
        label='基本情報の詳細',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        required=False
    )

    # 関係医療機関フィールド
    main_doctor_hospital = forms.CharField(
        label='主治医病院',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )
    main_doctor_name = forms.CharField(
        label='主治医名',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )
    visiting_doctor_hospital = forms.CharField(
        label='往診医病院',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )
    visiting_doctor_name = forms.CharField(
        label='往診医名',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )

    # 服薬・アレルギーフィールド
    MEDICATION_STATUS_CHOICES = [
        ('', '選択してください'),
        ('self', '自己管理'),
        ('family', '家族管理'),
        ('support', '支援あり'),
        ('none', '服薬なし'),
    ]

    medication_status = forms.ChoiceField(
        label='服薬状況',
        choices=MEDICATION_STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False
    )
    medication_content = forms.CharField(
        label='服薬内容',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        required=False
    )
    allergy_details = forms.CharField(
        label='アレルギー詳細',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        required=False
    )

    # 服薬・アレルギー関連フィールド
    has_sleeping_medication = forms.CharField(
        label='眠剤の有無',
        widget=forms.RadioSelect(choices=[('yes', 'あり'), ('no', 'なし')]),
        required=False
    )

    has_laxative = forms.CharField(
        label='下剤の有無',
        widget=forms.RadioSelect(choices=[('yes', 'あり'), ('no', 'なし')]),
        required=False
    )

    has_allergy = forms.CharField(
        label='アレルギーの有無',
        widget=forms.RadioSelect(choices=[('yes', 'あり'), ('no', 'なし')]),
        required=False
    )

    medication_allergy_notes = forms.CharField(
        label='服薬・アレルギーの詳細',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        required=False
    )

    # 身体状況フィールド
    has_skin_disease = forms.CharField(
        label='皮膚疾患の有無',
        widget=forms.RadioSelect(choices=[('yes', 'あり'), ('no', 'なし')]),
        required=False
    )

    skin_disease = forms.MultipleChoiceField(
        label='皮膚疾患',
        choices=[
            ('bedsore', '床ずれ'),
            ('eczema', '湿疹'),
            ('itching', 'かゆみ'),
            ('athletes_foot', '水虫'),
            ('shingles', '帯状疱疹'),
            ('other', 'その他'),
        ],
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    skin_disease_other = forms.CharField(
        label='その他の皮膚疾患',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )

    infection_presence = forms.CharField(
        label='感染症の有無',
        widget=forms.RadioSelect(choices=[('yes', 'あり'), ('no', 'なし')]),
        required=False
    )

    infection = forms.MultipleChoiceField(
        label='感染症',
        choices=[
            ('tuberculosis', '結核'),
            ('pneumonia', '肺炎'),
            ('hepatitis', '肝炎'),
            ('scabies', '疥癬'),
            ('mrsa', 'MRSA'),
            ('other', 'その他'),
        ],
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    infection_other_text = forms.CharField(
        label='その他の感染症',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )

    skin_infection_details = forms.CharField(
        label='皮膚疾患・感染症の詳細',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        required=False
    )

    has_paralysis = forms.CharField(
        label='麻痺の有無',
        widget=forms.RadioSelect(choices=[('yes', 'あり'), ('no', 'なし')]),
        required=False
    )

    has_pain = forms.CharField(
        label='痛みの有無',
        widget=forms.RadioSelect(choices=[('yes', 'あり'), ('no', 'なし')]),
        required=False
    )

    paralysis_pain_details = forms.CharField(
        label='麻痺・痛みの詳細',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        required=False
    )

    uses_hearing_aid = forms.CharField(
        label='補聴器の使用',
        widget=forms.RadioSelect(choices=[('yes', '使用'), ('no', '未使用')]),
        required=False
    )

    sensory_function_details = forms.CharField(
        label='視聴覚機能の詳細',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        required=False
    )

    uses_glasses = forms.CharField(
        label='眼鏡等の使用',
        widget=forms.RadioSelect(choices=[('yes', '使用'), ('no', '未使用')]),
        required=False
    )

    # かかりつけ医フィールド
    family_doctor_hospital_1 = forms.CharField(
        label='かかりつけ医病院1',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )
    family_doctor_name_1 = forms.CharField(
        label='かかりつけ医名1',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )
    family_doctor_hospital_2 = forms.CharField(
        label='かかりつけ医病院2',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )
    family_doctor_name_2 = forms.CharField(
        label='かかりつけ医名2',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )
    family_doctor_hospital_3 = forms.CharField(
        label='かかりつけ医病院3',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )
    family_doctor_name_3 = forms.CharField(
        label='かかりつけ医名3',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )
    family_doctor_hospital_4 = forms.CharField(
        label='かかりつけ医病院4',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )
    family_doctor_name_4 = forms.CharField(
        label='かかりつけ医名4',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )

    # 通院情報フィールド
    hospital_visit_status = forms.CharField(
        label='通院状況',
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False
    )
    hospital_visit_method = forms.CharField(
        label='通院方法',
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False
    )
    hospital_visit_method_other = forms.CharField(
        label='その他の通院方法',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )
    medical_institution_notes = forms.CharField(
        label='関係医療機関の詳細',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        required=False
    )


    main_doctor = forms.CharField(
        label='主治医※安室通うまん入院後（中）| 病院・医院',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )
    
    outpatient_clinic = forms.CharField(
        label='往診医｜病院・医院',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )
    
    medication = forms.CharField(
        label='かかりつけ医ひ',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )
    
    hospital = forms.CharField(
        label='通院',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )
    
    medication_details = forms.CharField(
        label='服薬',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        required=False
    )
    
    allergies = forms.BooleanField(
        label='アレルギー｜有無',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        required=False
    )
    
    # 身体状況
    SKIN_CONDITIONS = [
        ('none', '無'),
        ('bedsore', '床ずれ'),
        ('eczema', '湿疹'),
        ('itching', 'かゆみ'),
        ('insect_bite', '水虫'),
    ]
    
    skin_condition = forms.MultipleChoiceField(
        label='皮膚疾患',
        choices=SKIN_CONDITIONS,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False
    )
    
    INFECTION_STATUS = [
        ('none', '無'),
        ('tuberculosis', '結核'),
        ('pneumonia', '肺炎'),
        ('hepatitis', '肝炎'),
        ('scabies', '疥癬'),
        ('mrsa', 'MRSA'),
    ]
    
    infection_status = forms.MultipleChoiceField(
        label='感染症',
        choices=INFECTION_STATUS,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False
    )
    
    SPECIAL_TREATMENTS = [
        ('none', '無'),
        ('stoma_management', '点滴の管理'),
        ('central_venous', '中心静脈栄養'),
        ('dialysis', '透析'),
        ('stoma_treatment', 'ストマの処置'),
        ('oxygen_therapy', '酸素療法'),
        ('ventilator', 'レスピレーター（人工呼吸器）'),
        ('tracheostomy', '気管切開の処置'),
        ('pain_management', '疼痛の看護'),
        ('nutritional_management', '経管栄養'),
        ('monitoring', 'モニター測定'),
        ('sputum_suction', '喀痰の処置'),
        ('catheter', 'カテーテル'),
    ]
    
    special_treatment = forms.MultipleChoiceField(
        label='特別な医療処置',
        choices=SPECIAL_TREATMENTS,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False
    )
    
    pain_location = forms.CharField(
        label='痛みの有無｜（部位：右上肢、右下肢　等）',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        required=False
    )
    
    pain_existence = forms.CharField(
        label='痛みの有無',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        required=False
    )
    
    height = forms.DecimalField(
        label='身長｜（例）160 ※cm不要',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '0'}),
        required=False
    )
    
    weight = forms.DecimalField(
        label='体重｜（例）42 ※kg不要',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '0'}),
        required=False
    )
    
    VISION_CHOICES = [
        ('', '選択してください'),
        ('normal', '正常'),
        ('large_letters_ok', '大きい字は可'),
        ('barely_visible', 'ほぼ見えない'),
        ('blind', '失明'),
    ]
    
    vision = forms.ChoiceField(
        label='視力',
        choices=VISION_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False
    )
    
    HEARING_CHOICES = [
        ('', '選択してください'),
        ('normal', '正常'),
        ('loud_voice_ok', '大きい声は可'),
        ('barely_audible', 'ほぼ聞こえない'),
        ('deaf', '失聴'),
    ]
    
    hearing = forms.ChoiceField(
        label='聴力',
        choices=HEARING_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False
    )
    
    physical_notes = forms.CharField(
        label='身体状況｜特記事項',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        required=False
    )
    
    # 認知機能
    dementia_symptoms = forms.BooleanField(
        label='認知症の有無',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        required=False
    )
    
    BPSD_SYMPTOMS = [
        ('none', '無'),
        ('persecution_delusion', '被害妄想'),
        ('confabulation', '作話'),
        ('mood_instability', '感情の不安定'),
        ('day_night_reversal', '昼夜逆転'),
        ('wandering', '帰宅願望'),
        ('loud_voice', '大声・奇声'),
        ('violence', '暴力'),
        ('loud_music', '暴言'),
        ('collection', '収集癖'),
        ('care_resistance', '介護抵抗'),
        ('unable_to_settle', '落ち着きがない'),
        ('wandering_behavior', '徘徊'),
        ('destructive_behavior', '破壊行為'),
        ('pica', 'ひどい物忘れ'),
        ('self_harm', '自分勝手な行動'),
        ('unstable', '不穏'),
        ('fainting', '警傾向'),
    ]
    
    bpsd_symptoms = forms.MultipleChoiceField(
        label='BPSD',
        choices=BPSD_SYMPTOMS,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False
    )
    
    CONVERSATION_CHOICES = [
        ('', '選択してください'),
        ('possible', '可能'),
        ('unclear', '不明瞭'),
        ('somewhat_difficult', 'やや不自由'),
        ('completely_impossible', '全くできない'),
    ]
    
    conversation = forms.ChoiceField(
        label='会話',
        choices=CONVERSATION_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False
    )
    
    COMMUNICATION_CHOICES = [
        ('', '選択してください'),
        ('possible', '可能'),
        ('only_sometimes', 'その場のみ可'),
        ('somewhat_difficult', 'やや不自由'),
        ('completely_impossible', '全くできない'),
    ]
    
    communication = forms.ChoiceField(
        label='意思疎通',
        choices=COMMUNICATION_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False
    )
    
    cognitive_notes = forms.CharField(
        label='認知機能｜特記事項',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        required=False
    )
    
    # 基本動作
    BASIC_ACTIVITY_CHOICES = [
        ('', '選択してください'),
        ('no_assistance', 'つかまらないでできる'),
        ('with_assistance', '何かにつかまればできる'),
        ('cannot', 'できない'),
    ]
    
    turning_over = forms.ChoiceField(
        label='寝返り',
        choices=BASIC_ACTIVITY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False
    )
    
    getting_up = forms.ChoiceField(
        label='起き上がり',
        choices=BASIC_ACTIVITY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False
    )
    
    SITTING_CHOICES = [
        ('', '選択してください'),
        ('can_do', 'できる'),
        ('self_support', '自分の手で支えればできる'),
        ('support_needed', '支えてもらえればできる'),
        ('cannot', 'できない'),
    ]
    
    sitting = forms.ChoiceField(
        label='座位',
        choices=SITTING_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False
    )
    
    standing_up = forms.ChoiceField(
        label='立ち上がり',
        choices=BASIC_ACTIVITY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False
    )
    
    standing = forms.ChoiceField(
        label='立位',
        choices=[
            ('', '選択してください'),
            ('no_support', '支えなしでできる'),
            ('with_something', '何か支えがあればできる'),
            ('cannot', 'できない'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False
    )
    
    MOBILITY_CHOICES = [
        ('', '選択してください'),
        ('independent', '自立'),
        ('supervision', '見守り'),
        ('partial_assistance', '一部介助'),
        ('full_assistance', '全介助'),
    ]
    
    transfer = forms.ChoiceField(
        label='移乗',
        choices=MOBILITY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False
    )
    
    indoor_mobility = forms.ChoiceField(
        label='屋内移動',
        choices=MOBILITY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False
    )
    
    MOBILITY_EQUIPMENT_CHOICES = [
        ('', '選択してください'),
        ('none', 'なし'),
        ('wheelchair', '車椅子'),
        ('walker', '歩行器'),
        ('cane', '杖'),
        ('crutches', '松葉杖'),
        ('other', 'その他'),
    ]
    
    indoor_mobility_equipment = forms.ChoiceField(
        label='屋内移動使用用具',
        choices=MOBILITY_EQUIPMENT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False
    )
    
    outdoor_mobility = forms.ChoiceField(
        label='屋外移動',
        choices=MOBILITY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False
    )
    
    outdoor_mobility_equipment = forms.ChoiceField(
        label='屋外移動使用用具',
        choices=MOBILITY_EQUIPMENT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False
    )
    
    basic_activity_notes = forms.CharField(
        label='基本動作｜特記事項',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        required=False
    )
    
    # ADL
    eating_method = forms.ChoiceField(
        label='食事方法',
        choices=[
            ('', '選択してください'),
            ('oral', '経口摂取'),
            ('tube_oral', '経管栄養+経口摂取'),
            ('tube_only', '経管栄養（胃ろう）'),
            ('tube_nasal', '経管栄養（経鼻）'),
            ('tube_gastronomy', '経管栄養（腸ろう）'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False
    )
    
    eating_assistance = forms.ChoiceField(
        label='食事動作',
        choices=MOBILITY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False
    )
    
    swallowing = forms.ChoiceField(
        label='嚥下',
        choices=[
            ('', '選択してください'),
            ('can_do', 'できる'),
            ('supervision_needed', '見守り等が必要'),
            ('cannot', 'できない'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False
    )
    
    MEAL_FORM_MAIN_CHOICES = [
        ('', '選択してください'),
        ('normal', '普通'),
        ('soft', '軟飯'),
        ('porridge', '全粥'),
        ('paste', 'ペースト'),
    ]
    
    meal_form_main = forms.ChoiceField(
        label='食事形態｜主食',
        choices=MEAL_FORM_MAIN_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False
    )
    
    MEAL_FORM_SIDE_CHOICES = [
        ('', '選択してください'),
        ('normal', '普通'),
        ('soft', '一口大'),
        ('minced', '粗きザミ'),
        ('paste', 'キザミ'),
        ('paste_form', 'ペースト'),
    ]
    
    meal_form_side = forms.ChoiceField(
        label='食事形態｜副食',
        choices=MEAL_FORM_SIDE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False
    )
    
    water_thickening = forms.ChoiceField(
        label='水分とろみの有無',
        choices=[
            ('', ''),
            ('yes', 'あり'),
            ('no', 'なし'),
        ],
        widget=forms.RadioSelect(),
        required=False
    )

    water_thickening_level = forms.ChoiceField(
        label='とろみの濃さ',
        choices=[
            ('', ''),
            ('thick', '濃い'),
            ('medium', '中'),
            ('thin', '薄い'),
        ],
        widget=forms.RadioSelect(),
        required=False
    )
    
    eating_restriction = forms.ChoiceField(
        label='食事制限の有無',
        choices=[
            ('', '選択してください'),
            ('yes', 'あり'),
            ('no', 'なし'),
            ('unknown', '不明'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False
    )
    
    EATING_UTENSILS = [
        ('chopsticks', '箸'),
        ('spoon', 'スプーン'),
        ('apron', 'エプロン'),
        ('assistive', '補助具'),
        ('other', 'その他'),
    ]
    
    eating_utensils = forms.MultipleChoiceField(
        label='道具・用具',
        choices=EATING_UTENSILS,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False
    )

    eating_restriction_detail = forms.CharField(
        label='食事制限詳細',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '制限内容を入力してください'}),
        required=False
    )

    eating_utensils_other_detail = forms.CharField(
        label='道具・用具その他詳細',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'その他の内容を入力してください'}),
        required=False
    )

    eating_notes = forms.CharField(
        label='食事｜特記事項',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        required=False
    )
    
    # 口腔
    oral_hygiene_assistance = forms.ChoiceField(
        label='口腔衛生',
        choices=MOBILITY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False
    )
    
    natural_teeth_presence = forms.ChoiceField(
        label='自歯の有無',
        choices=[('yes', 'あり'), ('no', 'なし')],
        widget=forms.RadioSelect(),
        required=False
    )
    
    denture_presence = forms.ChoiceField(
        label='義歯の有無',
        choices=[('yes', 'あり'), ('no', 'なし')],
        widget=forms.RadioSelect(),
        required=False
    )
    
    DENTURE_LOCATION_CHOICES = [
        ('upper', '上顎'),
        ('lower', '下顎'),
        ('both', '上下'),
    ]
    
    denture_type = forms.ChoiceField(
        label='義歯の種類',
        choices=[('partial', '部分義歯'), ('complete', '総義歯')],
        widget=forms.RadioSelect(),
        required=False
    )

    denture_location = forms.ChoiceField(
        label='義歯の場所',
        choices=DENTURE_LOCATION_CHOICES,
        widget=forms.RadioSelect(),
        required=False
    )
    
    oral_notes = forms.CharField(
        label='口腔｜特記事項',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        required=False
    )
    
    # 入浴・更衣
    bathing_assistance = forms.ChoiceField(
        label='入浴動作',
        choices=MOBILITY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False
    )
    
    BATHING_FORM_CHOICES = [
        ('', '選択してください'),
        ('regular_bath', '一般浴'),
        ('sitting_bath', '寝台浴'),
        ('shower_bath', 'シャワー浴'),
        ('chair_bath', 'チェアー浴'),
    ]
    
    bathing_form = forms.ChoiceField(
        label='形態',
        choices=BATHING_FORM_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False
    )
    
    bathing_restriction = forms.ChoiceField(
        label='入浴の制限',
        choices=[('yes', 'あり'), ('no', 'なし')],
        widget=forms.RadioSelect(),
        required=False
    )

    bathing_restriction_detail = forms.CharField(
        label='入浴制限詳細',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '制限内容を入力してください'}),
        required=False
    )
    
    dressing_upper = forms.ChoiceField(
        label='上衣',
        choices=MOBILITY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False
    )
    
    dressing_lower = forms.ChoiceField(
        label='下衣',
        choices=MOBILITY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False
    )
    
    bathing_notes = forms.CharField(
        label='入浴・更衣｜特記事項',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        required=False
    )
    
    # 排泄
    excretion_assistance = forms.ChoiceField(
        label='排泄動作',
        choices=MOBILITY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False
    )
    
    urination = forms.ChoiceField(
        label='尿意',
        choices=[('yes', 'あり'), ('no', 'なし')],
        widget=forms.RadioSelect(),
        required=False
    )
    
    urinary_incontinence = forms.ChoiceField(
        label='尿失禁',
        choices=[('yes', 'あり'), ('no', 'なし')],
        widget=forms.RadioSelect(),
        required=False
    )
    
    defecation = forms.ChoiceField(
        label='便意',
        choices=[('yes', 'あり'), ('no', 'なし')],
        widget=forms.RadioSelect(),
        required=False
    )
    
    fecal_incontinence = forms.ChoiceField(
        label='便失禁',
        choices=[('yes', 'あり'), ('no', 'なし')],
        widget=forms.RadioSelect(),
        required=False
    )

    urinary_incontinence_frequency = forms.CharField(
        label='尿失禁頻度',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '頻度を入力してください'}),
        required=False
    )

    fecal_incontinence_frequency = forms.CharField(
        label='便失禁頻度',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '頻度を入力してください'}),
        required=False
    )
    
    DAYTIME_LOCATION_CHOICES = [
        ('toilet', 'トイレ'),
        ('portable_toilet', 'Pトイレ'),
        ('bed', 'ベッド'),
    ]
    
    daytime_location = forms.MultipleChoiceField(
        label='場所｜日中',
        choices=DAYTIME_LOCATION_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False
    )
    
    nighttime_location = forms.MultipleChoiceField(
        label='場所｜夜間',
        choices=DAYTIME_LOCATION_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False
    )

    EXCRETION_METHOD_CHOICES = [
        ('urinal', '尿器'),
        ('diaper', 'オムツ'),
        ('catheter', 'カテーテル'),
        ('stoma', 'ストマ'),
    ]

    daytime_method = forms.MultipleChoiceField(
        label='方法｜日中',
        choices=EXCRETION_METHOD_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False
    )

    nighttime_method = forms.MultipleChoiceField(
        label='方法｜夜間',
        choices=EXCRETION_METHOD_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False
    )
    
    EXCRETION_SUPPLIES = [
        ('rehabilitation_pants', 'リハビリパンツ'),
        ('paper_diaper', '紙おむつ'),
        ('small_pad', '小パット'),
        ('large_pad', '大パット'),
    ]
    
    excretion_supplies = forms.MultipleChoiceField(
        label='排泄用品',
        choices=EXCRETION_SUPPLIES,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False
    )
    
    excretion_notes = forms.CharField(
        label='排泄｜特記事項',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        required=False
    )
    
    # IADL
    cooking = forms.ChoiceField(
        label='調理',
        choices=MOBILITY_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'btn-check'}),
        required=False
    )
    
    cleaning = forms.ChoiceField(
        label='掃除',
        choices=MOBILITY_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'btn-check'}),
        required=False
    )
    
    washing = forms.ChoiceField(
        label='洗濯',
        choices=MOBILITY_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'btn-check'}),
        required=False
    )
    
    shopping = forms.ChoiceField(
        label='買い物',
        choices=MOBILITY_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'btn-check'}),
        required=False
    )
    
    money_management = forms.ChoiceField(
        label='金銭管理',
        choices=MOBILITY_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'btn-check'}),
        required=False
    )
    
    iadl_notes = forms.CharField(
        label='IADL｜詳細',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        required=False
    )
    
    # 認知機能
    dementia_presence = forms.ChoiceField(
        label='認知症の有無',
        choices=[('', '選択してください'), ('yes', 'あり'), ('no', 'なし')],
        widget=forms.RadioSelect(attrs={'class': 'btn-check'}),
        required=False
    )

    dementia_severity = forms.ChoiceField(
        label='認知症の程度',
        choices=[('', '選択してください'), ('mild', '軽度'), ('moderate', '中等度'), ('severe', '重度')],
        widget=forms.RadioSelect(attrs={'class': 'btn-check'}),
        required=False
    )

    dementia_details = forms.CharField(
        label='認知症の詳細',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        required=False
    )
    
    bpsd_presence = forms.ChoiceField(
        label='BPSDの有無',
        choices=[('', '選択してください'), ('yes', 'あり'), ('no', 'なし')],
        widget=forms.RadioSelect(attrs={'class': 'btn-check'}),
        required=False
    )
    
    BPSD_SYMPTOMS_CHOICES = [
        ('none', 'なし'),
        ('persecution_delusion', '被害妄想'),
        ('confabulation', '作話'),
        ('mood_instability', '感情の不安定'),
        ('day_night_reversal', '昼夜逆転'),
        ('home_return_desire', '帰宅願望'),
        ('loud_voice', '大声・奇声'),
        ('violence', '暴力・暴言'),
        ('collection_habit', '収集癖'),
        ('care_resistance', '介護抵抗'),
        ('restlessness', '落ち着きがない'),
        ('wandering', '徘徊'),
        ('destructive_behavior', '破壊行為'),
        ('severe_forgetfulness', 'ひどい物忘れ'),
        ('selfish_behavior', '自分勝手な行動'),
        ('agitation', '不穏'),
        ('depression_tendency', 'うつ傾向'),
    ]
    
    bpsd_symptoms = forms.MultipleChoiceField(
        label='BPSD症状',
        choices=BPSD_SYMPTOMS_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False
    )

    bpsd_details = forms.CharField(
        label='BPSDの詳細',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        required=False
    )
    
    CONVERSATION_CHOICES = [
        ('', '選択してください'),
        ('possible', '可能'),
        ('unclear', '不明瞭'),
        ('somewhat_difficult', 'やや不自由'),
        ('impossible', '全くできない'),
    ]
    
    conversation = forms.ChoiceField(
        label='会話',
        choices=CONVERSATION_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'btn-check'}),
        required=False
    )
    
    COMMUNICATION_CHOICES = [
        ('', '選択してください'),
        ('possible', '可能'),
        ('only_sometimes', 'その場のみ可能'),
        ('somewhat_difficult', 'やや不自由'),
        ('impossible', '全くできない'),
    ]
    
    communication = forms.ChoiceField(
        label='意思疎通',
        choices=COMMUNICATION_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'btn-check'}),
        required=False
    )
    
    cognitive_notes = forms.CharField(
        label='認知機能｜詳細',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        required=False
    )