from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Client(models.Model):
    GENDER_CHOICES = [
        ('male', '男性'),
        ('female', '女性'),
        ('other', 'その他'),
    ]
    
    CARE_LEVEL_CHOICES = [
        ('independent', '自立'),
        ('support1', '要支援1'),
        ('support2', '要支援2'),
        ('care1', '要介護1'),
        ('care2', '要介護2'),
        ('care3', '要介護3'),
        ('care4', '要介護4'),
        ('care5', '要介護5'),
    ]
    
    CARE_BURDEN_CHOICES = [
        ('1割負担', '1割負担'),
        ('2割負担', '2割負担'),
        ('3割負担', '3割負担'),
    ]

    DISABILITY_LEVEL_CHOICES = [
        ('', '選択してください'),
        ('independent', '自立'),
        ('J1', 'J1'),
        ('J2', 'J2'),
        ('A1', 'A1'),
        ('A2', 'A2'),
        ('B1', 'B1'),
        ('B2', 'B2'),
        ('C1', 'C1'),
        ('C2', 'C2'),
    ]

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

    RELATIONSHIP_CHOICES = [
        ('spouse', '配偶者'),
        ('child', '子'),
        ('parent', '親'),
        ('sibling', '兄弟姉妹'),
        ('grandchild', '孫'),
        ('grandparent', '祖父母'),
        ('other_relative', 'その他親族'),
        ('other', 'その他'),
    ]

    LIVING_STATUS_CHOICES = [
        ('together', '同居'),
        ('separate', '別居'),
    ]

    CARE_STATUS_CHOICES = [
        ('primary_caregiver', '主たる介護者'),
        ('support_caregiver', '介護協力者'),
        ('no_care', '介護なし'),
    ]

    EMPLOYMENT_STATUS_CHOICES = [
        ('', '選択してください'),
        ('employed', '就労中'),
        ('unemployed', '無職'),
        ('retired', '退職'),
        ('homemaker', '専業主婦(夫)'),
        ('student', '学生'),
        ('other', 'その他'),
    ]

    MEDICAL_INSURANCE_CHOICES = [
        ('', '選択してください'),
        ('national_health', '国民健康保険'),
        ('latter_stage_elderly', '後期高齢者医療'),
        ('health_insurance_association', '健康保険（協会けんぽ）'),
        ('health_insurance_union', '健康保険（組合）'),
        ('mutual_aid', '共済組合'),
        ('seamen', '船員保険'),
        ('other', 'その他'),
    ]
    
    # 基本情報
    # id = models.AutoField(primary_key=True)  # Djangoが自動的に追加
    insurance_number = models.CharField('被保険者番号', max_length=10, unique=True)
    name = models.CharField('氏名', max_length=100)
    furigana = models.CharField('ふりがな', max_length=100)
    birth_date = models.DateField('生年月日')
    gender = models.CharField('性別', max_length=10, choices=GENDER_CHOICES)
    phone = models.CharField('電話番号', max_length=15, blank=True)
    postal_code = models.CharField('郵便番号', max_length=10, blank=True)
    address = models.TextField('住所', blank=True)
    
    # 保険情報
    care_level = models.CharField('要介護度', max_length=20, choices=CARE_LEVEL_CHOICES, blank=True)
    certification_date = models.DateField('認定日', blank=True, null=True)
    certification_period_start = models.DateField('認定期間（開始）', blank=True, null=True)
    certification_period_end = models.DateField('認定期間（終了）', blank=True, null=True)
    care_burden = models.CharField('負担割合', max_length=10, choices=CARE_BURDEN_CHOICES, blank=True)
    burden_period_start = models.DateField('負担割合期間（開始）', blank=True, null=True)
    burden_period_end = models.DateField('負担割合期間（終了）', blank=True, null=True)
    
    # 障がい・認知症自立度
    disability_level = models.CharField('障がい者日常生活自立度', max_length=20, choices=DISABILITY_LEVEL_CHOICES, blank=True)
    dementia_level = models.CharField('認知症日常生活自立度', max_length=20, choices=DEMENTIA_LEVEL_CHOICES, blank=True)

    # 手帳・申請・保護
    disability_handbook = models.BooleanField('身体障がい者手帳', default=False)
    disability_handbook_type = models.CharField('障害種別', max_length=100, blank=True)
    difficult_disease = models.BooleanField('難病申請', default=False)
    difficult_disease_name = models.CharField('難病疾患名', max_length=200, blank=True)
    life_protection = models.BooleanField('生活保護', default=False)

    # 公的制度・受給者証（介護保険関係）
    limit_cert = models.CharField('負担限度額認定証', max_length=3, blank=True)  # yes/no
    limit_cert_start = models.DateField('負担限度額 有効期間（開始）', blank=True, null=True)
    limit_cert_end = models.DateField('負担限度額 有効期間（終了）', blank=True, null=True)
    high_cost_care = models.CharField('高額介護サービス費', max_length=3, blank=True)  # yes/no

    # 公的制度・受給者証（障害福祉関係）
    disability_welfare = models.CharField('障害福祉サービス受給者証', max_length=3, blank=True)
    disability_welfare_cert_start = models.DateField('障害福祉 認定有効期間（開始）', blank=True, null=True)
    disability_welfare_cert_end = models.DateField('障害福祉 認定有効期間（終了）', blank=True, null=True)
    disability_welfare_decision_start = models.DateField('障害福祉 支給決定期間（開始）', blank=True, null=True)
    disability_welfare_decision_end = models.DateField('障害福祉 支給決定期間（終了）', blank=True, null=True)

    # 公的制度・受給者証（医療関係）
    specific_medical = models.CharField('特定医療費（指定難病）受給者証', max_length=3, blank=True)
    specific_medical_start = models.DateField('特定医療費 有効期間（開始）', blank=True, null=True)
    specific_medical_end = models.DateField('特定医療費 有効期間（終了）', blank=True, null=True)
    welfare_medical = models.CharField('福祉医療費受給者証', max_length=3, blank=True)
    welfare_medical_start = models.DateField('福祉医療費 有効期間（開始）', blank=True, null=True)
    welfare_medical_end = models.DateField('福祉医療費 有効期間（終了）', blank=True, null=True)
    nhi_limit_cert = models.CharField('国保限度額適用・減額認定証', max_length=3, blank=True)
    nhi_limit_cert_start = models.DateField('国保限度額 有効期間（開始）', blank=True, null=True)
    nhi_limit_cert_end = models.DateField('国保限度額 有効期間（終了）', blank=True, null=True)
    high_cost_combined = models.CharField('高額医療・高額介護合算療養費', max_length=3, blank=True)

    # 医療保険情報
    medical_insurance_type = models.CharField('医療保険種類', max_length=100, choices=MEDICAL_INSURANCE_CHOICES, blank=True)
    medical_insurer_name_issuer = models.CharField('保険者の名称及び交付者名', max_length=200, blank=True)
    medical_insurer_number = models.CharField('医療保険保険者番号', max_length=50, blank=True)
    medical_insurance_symbol = models.CharField('被保険者番号（記号）', max_length=50, blank=True)
    medical_insurance_number = models.CharField('被保険者番号（番号）', max_length=50, blank=True)
    medical_insurance_branch = models.CharField('被保険者番号（枝番）', max_length=10, blank=True)
    
    # 家族情報（1人目）
    family_name1 = models.CharField('家族氏名（1人目）', max_length=100, blank=True)
    family_relationship1 = models.CharField('続柄（1人目）', max_length=20, choices=RELATIONSHIP_CHOICES, blank=True)
    family_address1 = models.TextField('住所（1人目）', blank=True)
    family_living_status1 = models.CharField('同居有無（1人目）', max_length=10, choices=LIVING_STATUS_CHOICES, blank=True)
    family_care_status1 = models.CharField('介護状況（1人目）', max_length=20, choices=CARE_STATUS_CHOICES, blank=True)
    family_employment1 = models.CharField('就労状況（1人目）', max_length=20, choices=EMPLOYMENT_STATUS_CHOICES, blank=True)
    family_contact1 = models.CharField('連絡先（1人目）', max_length=15, blank=True)
    family_notes1 = models.TextField('備考（1人目）', blank=True)
    
    # 家族情報（2人目）
    family_name2 = models.CharField('家族氏名（2人目）', max_length=100, blank=True)
    family_relationship2 = models.CharField('続柄（2人目）', max_length=20, choices=RELATIONSHIP_CHOICES, blank=True)
    family_address2 = models.TextField('住所（2人目）', blank=True)
    family_living_status2 = models.CharField('同居有無（2人目）', max_length=10, choices=LIVING_STATUS_CHOICES, blank=True)
    family_care_status2 = models.CharField('介護状況（2人目）', max_length=20, choices=CARE_STATUS_CHOICES, blank=True)
    family_employment2 = models.CharField('就労状況（2人目）', max_length=20, choices=EMPLOYMENT_STATUS_CHOICES, blank=True)
    family_contact2 = models.CharField('連絡先（2人目）', max_length=15, blank=True)
    family_notes2 = models.TextField('備考（2人目）', blank=True)
    
    # 作成・更新情報
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='作成者')
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)
    
    class Meta:
        verbose_name = '利用者'
        verbose_name_plural = '利用者'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.insurance_number} - {self.name}"
    
    @property
    def client_id(self):
        # 後方互換性のために被保険者番号をclient_idとして返す
        return self.insurance_number
    
    @property
    def age(self):
        from datetime import date
        today = date.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
    
    @property
    def care_limit_units(self):
        """要介護度に基づく限度額（単位）を返す"""
        care_limit_map = {
            'support1': 5032,    # 要支援1
            'support2': 10531,   # 要支援2
            'care1': 16765,      # 要介護1
            'care2': 19705,      # 要介護2
            'care3': 27048,      # 要介護3
            'care4': 30938,      # 要介護4
            'care5': 36217,      # 要介護5
        }
        return care_limit_map.get(self.care_level, 0)


class ServiceType(models.Model):
    """サービス種別"""
    CATEGORY_CHOICES = [
        ('day_service', 'デイサービス'),
        ('home_helper', 'ヘルパー'),
        ('visiting_nurse', '訪問看護'),
        ('welfare_equipment', '福祉用具'),
        ('other', 'その他'),
    ]
    
    name = models.CharField('サービス名', max_length=100)
    category = models.CharField('カテゴリ', max_length=20, choices=CATEGORY_CHOICES, default='other')
    unit_per_minute = models.DecimalField('1分あたりの単位数', max_digits=8, decimal_places=2)
    total_units = models.DecimalField('合計単位数', max_digits=8, decimal_places=2, null=True, blank=True, help_text='時間が含まれている場合の総単位数')
    duration_minutes = models.IntegerField('実施時間（分）', null=True, blank=True, help_text='サービス名に時間が含まれている場合')
    is_active = models.BooleanField('有効', default=True)
    
    class Meta:
        verbose_name = 'サービス種別'
        verbose_name_plural = 'サービス種別'
        ordering = ['category', 'name']
    
    def __str__(self):
        return self.name
    
    def get_service_units(self, minutes=None):
        """サービスの単位数を計算（時間指定がある場合は固定、ない場合は分数×単価）"""
        if self.total_units:
            return self.total_units
        elif minutes:
            return self.unit_per_minute * minutes
        elif self.duration_minutes:
            return self.unit_per_minute * self.duration_minutes
        return 0


class LimitCalculation(models.Model):
    """限度額試算"""
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='利用者')
    year = models.IntegerField('年')
    month = models.IntegerField('月', validators=[MinValueValidator(1), MaxValueValidator(12)])
    care_manager_units = models.DecimalField('ケアマネ設定単位', max_digits=10, decimal_places=2, default=0)
    
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)
    
    class Meta:
        verbose_name = '限度額試算'
        verbose_name_plural = '限度額試算'
        unique_together = ['client', 'year', 'month']
        ordering = ['-year', '-month']
    
    def __str__(self):
        return f"{self.client.name} - {self.year}年{self.month}月"
    
    @property
    def total_used_units(self):
        """使用済み総単位数"""
        from decimal import Decimal
        additional_units = sum(Decimal(str(service.total_units)) for service in self.additional_services.all()) or Decimal('0')
        return Decimal(str(self.care_manager_units)) + additional_units
    
    @property
    def remaining_units(self):
        """残り単位数"""
        from decimal import Decimal
        return Decimal(str(self.client.care_limit_units)) - self.total_used_units
    
    @property
    def is_over_limit(self):
        """限度額超過かどうか"""
        from decimal import Decimal
        return self.total_used_units > Decimal(str(self.client.care_limit_units))


class ServiceProvider(models.Model):
    """事業所（サービス提供事業者）"""
    name = models.CharField('事業所名', max_length=100)
    service_category = models.CharField('サービスカテゴリ', max_length=20, choices=ServiceType.CATEGORY_CHOICES)
    is_active = models.BooleanField('有効', default=True)
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    
    class Meta:
        verbose_name = '事業所'
        verbose_name_plural = '事業所'
    
    def __str__(self):
        return f"{self.name} ({self.get_service_category_display()})"


class ServiceAddOn(models.Model):
    """加算種別"""
    ADDON_TYPE_CHOICES = [
        ('functional_training', '機能訓練加算'),
        ('bathing', '入浴加算'),
        ('dementia', '認知症対応型加算'),
        ('nutrition', '栄養改善加算'),
        ('oral_care', '口腔機能向上加算'),
        ('transportation', '送迎減算'),
        ('large_scale', '大規模減算'),
        ('other', 'その他'),
    ]
    
    name = models.CharField('加算名', max_length=100)
    addon_type = models.CharField('加算タイプ', max_length=30, choices=ADDON_TYPE_CHOICES)
    units = models.DecimalField('単位数', max_digits=8, decimal_places=2)
    is_addition = models.BooleanField('加算/減算', default=True, help_text='True=加算、False=減算')
    description = models.TextField('説明', blank=True)
    is_active = models.BooleanField('有効', default=True)
    
    class Meta:
        verbose_name = '加算種別'
        verbose_name_plural = '加算種別'
    
    def __str__(self):
        sign = '+' if self.is_addition else '-'
        return f"{self.name} ({sign}{self.units}単位)"


class ProviderAddOnSetting(models.Model):
    """事業所別加算設定"""
    provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE, related_name='addon_settings')
    addon = models.ForeignKey(ServiceAddOn, on_delete=models.CASCADE)
    is_enabled = models.BooleanField('有効', default=True)
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    
    class Meta:
        verbose_name = '事業所別加算設定'
        verbose_name_plural = '事業所別加算設定'
        unique_together = ['provider', 'addon']
    
    def __str__(self):
        return f"{self.provider.name} - {self.addon.name}"


class ClientDementiaStatus(models.Model):
    """利用者別認知症対応状況"""
    client = models.OneToOneField(Client, on_delete=models.CASCADE, related_name='dementia_status')
    requires_dementia_care = models.BooleanField('認知症対応が必要', default=False)
    dementia_level = models.CharField('認知症レベル', max_length=10, choices=[
        ('1', 'レベル1'),
        ('2', 'レベル2'),
        ('3', 'レベル3'),
        ('4', 'レベル4'),
    ], blank=True)
    notes = models.TextField('備考', blank=True)
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)
    
    class Meta:
        verbose_name = '利用者別認知症状況'
        verbose_name_plural = '利用者別認知症状況'
    
    def __str__(self):
        return f"{self.client.name} - 認知症対応: {'要' if self.requires_dementia_care else '不要'}"


class AdditionalService(models.Model):
    """追加サービス"""
    limit_calculation = models.ForeignKey(LimitCalculation, on_delete=models.CASCADE, 
                                        related_name='additional_services', verbose_name='限度額試算')
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE, verbose_name='サービス種別')
    provider = models.ForeignKey(ServiceProvider, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='事業所')
    minutes = models.IntegerField('実施時間（分）', null=True, blank=True, help_text='手動入力時のみ使用')
    date_provided = models.DateField('実施日')
    provider_name = models.CharField('事業所名', max_length=100, blank=True, help_text='手動入力用（後方互換性）')
    
    # デイサービス加算項目
    has_functional_training = models.BooleanField('機能訓練加算', default=False)
    has_bathing = models.BooleanField('入浴加算', default=False)
    has_cognitive_function = models.BooleanField('認知機能加算', default=False)
    
    notes = models.TextField('備考', blank=True)
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    
    class Meta:
        verbose_name = '追加サービス'
        verbose_name_plural = '追加サービス'
        ordering = ['-date_provided', '-created_at']
    
    def __str__(self):
        if self.service_type.duration_minutes:
            return f"{self.service_type.name}"
        else:
            return f"{self.service_type.name} - {self.minutes}分"
    
    @property
    def total_units(self):
        """合計単位数（加算を含む）"""
        from decimal import Decimal
        
        # 基本単位数を計算
        base_units = Decimal('0')
        if self.service_type.total_units:
            base_units = Decimal(str(self.service_type.total_units))
        elif self.service_type.duration_minutes:
            base_units = Decimal(str(self.service_type.unit_per_minute)) * Decimal(str(self.service_type.duration_minutes))
        elif self.minutes:
            base_units = Decimal(str(self.service_type.unit_per_minute)) * Decimal(str(self.minutes))
        
        # 加算単位数を計算
        addon_units = Decimal('0')
        
        # デイサービスの場合の加算
        if self.service_type.category == 'day_service':
            # 機能訓練加算
            if self.has_functional_training:
                addon_units += Decimal('12')  # 機能訓練加算I: 12単位/日
            
            # 入浴加算
            if self.has_bathing:
                addon_units += Decimal('40')  # 入浴加算: 40単位/日
            
            # 認知機能加算
            if self.has_cognitive_function:
                addon_units += Decimal('60')  # 認知機能加算: 60単位/日
            
            # 事業所別加算
            if self.provider:
                enabled_addons = self.provider.addon_settings.filter(is_enabled=True)
                for setting in enabled_addons:
                    if setting.addon.is_addition:
                        addon_units += Decimal(str(setting.addon.units))
                    else:
                        addon_units -= Decimal(str(setting.addon.units))
        
        return base_units + addon_units
    
    @property
    def display_minutes(self):
        """表示用の時間"""
        if self.service_type.duration_minutes:
            return self.service_type.duration_minutes
        return self.minutes


class DocumentCreationHistory(models.Model):
    """書類作成履歴"""
    DOCUMENT_TYPE_CHOICES = [
        ('kyotaku_service_plan_request', '居宅サービス計画作成依頼書'),
        ('kyotaku_preventive_service_plan_request', '介護予防サービス計画作成依頼書'),
        ('care_plan', 'ケアプラン'),
        ('assessment', 'アセスメント'),
        ('other', 'その他'),
    ]

    STATUS_CHOICES = [
        ('draft', '下書き'),
        ('completed', '完成'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='document_histories', verbose_name='利用者')
    document_type = models.CharField('書類種別', max_length=50, choices=DOCUMENT_TYPE_CHOICES)
    document_name = models.CharField('書類名', max_length=200)
    form_data = models.JSONField('入力内容', help_text='フォームの入力データ')
    status = models.CharField('ステータス', max_length=20, choices=STATUS_CHOICES, default='draft')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='作成者')
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)

    class Meta:
        verbose_name = '書類作成履歴'
        verbose_name_plural = '書類作成履歴'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.client.name} - {self.document_name} ({self.get_status_display()})"

    @property
    def formatted_created_at(self):
        """作成日時の表示用フォーマット"""
        return self.created_at.strftime('%Y/%m/%d %H:%M')


class UserProfile(models.Model):
    """ユーザープロファイル（カラーテーマ設定など）"""
    THEME_CHOICES = [
        ('current', 'パステルカラー（明るく優しい色合い）'),
    ]

    ROLE_CHOICES = [
        ('admin', '管理者'),
        ('care_manager', 'ケアマネージャー'),
        ('staff', '一般スタッフ'),
    ]

    ORGANIZATION_CHOICES = [
        ('annotsuroman', '居宅介護支援事業所 安濃津ろまん'),
    ]

    JOB_TYPE_CHOICES = [
        ('care_manager', '介護支援専門員'),
        ('social_worker', '社会福祉士'),
        ('nurse', '看護師'),
        ('care_worker', '介護福祉士'),
        ('other', 'その他'),
    ]

    DEPARTMENT_CHOICES = [
        ('kyotaku', '居宅'),
        ('helper', 'ヘルパー'),
        ('helper_general_affairs', 'ヘルパー庶務'),
        ('day_service', 'デイサービス'),
        ('day_service_general_affairs', 'デイサービス庶務'),
        ('visiting_nurse', '訪問看護'),
        ('visiting_nurse_general_affairs', '訪問看護庶務'),
        ('office', '事務所'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name='ユーザー')

    # 基本情報
    last_name = models.CharField('姓', max_length=50, blank=True)
    first_name = models.CharField('名', max_length=50, blank=True)
    last_name_kana = models.CharField('セイ', max_length=50, blank=True)
    first_name_kana = models.CharField('メイ', max_length=50, blank=True)

    # 連絡先
    phone = models.CharField('電話番号', max_length=15, blank=True)
    email = models.EmailField('メールアドレス', blank=True)

    # 役職・所属
    role = models.CharField('役職', max_length=20, choices=ROLE_CHOICES, default='staff')
    organization = models.CharField('事業所', max_length=50, choices=ORGANIZATION_CHOICES, default='annotsuroman')
    job_type = models.CharField('業種', max_length=50, choices=JOB_TYPE_CHOICES, blank=True)
    department = models.CharField('所属部署', max_length=100, choices=DEPARTMENT_CHOICES, blank=True)
    home_care_office = models.ForeignKey('HomeCareSupportOffice', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='所属居宅介護支援事業所', related_name='staff_members')

    # システム設定
    color_theme = models.CharField('カラーテーマ', max_length=20, choices=THEME_CHOICES, default='current')
    is_active = models.BooleanField('有効', default=True, help_text='無効にするとログインできなくなります')

    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)

    class Meta:
        verbose_name = 'ユーザープロファイル'
        verbose_name_plural = 'ユーザープロファイル'

    def __str__(self):
        return f"{self.user.username} - {self.get_full_name()}"

    def get_full_name(self):
        """フルネームを取得"""
        if self.last_name or self.first_name:
            return f"{self.last_name} {self.first_name}".strip()
        return self.user.username

    def get_full_name_kana(self):
        """フルネーム（カナ）を取得"""
        if self.last_name_kana or self.first_name_kana:
            return f"{self.last_name_kana} {self.first_name_kana}".strip()
        return ""


class Feedback(models.Model):
    """ユーザーからのフィードバック（要望・不具合報告）"""

    CATEGORY_CHOICES = [
        ('bug', '不具合報告'),
        ('feature', '新機能提案'),
        ('improvement', '改善要望'),
        ('other', 'その他'),
    ]

    PRIORITY_CHOICES = [
        ('high', '高'),
        ('medium', '中'),
        ('low', '低'),
    ]

    STATUS_CHOICES = [
        ('new', '未対応'),
        ('in_progress', '対応中'),
        ('completed', '完了'),
        ('rejected', '却下'),
    ]

    # 基本情報
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='投稿者')
    category = models.CharField('カテゴリ', max_length=20, choices=CATEGORY_CHOICES)
    title = models.CharField('タイトル', max_length=200)
    content = models.TextField('詳細内容')
    priority = models.CharField('優先度', max_length=20, choices=PRIORITY_CHOICES, default='medium')

    # ステータス管理
    status = models.CharField('ステータス', max_length=20, choices=STATUS_CHOICES, default='new')

    # 追加情報
    page_url = models.CharField('報告元ページURL', max_length=500, blank=True)

    # セキュリティ
    password = models.CharField('閲覧パスワード', max_length=4, default='0000', help_text='4桁の数字')

    # 日時
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)

    class Meta:
        verbose_name = 'フィードバック'
        verbose_name_plural = 'フィードバック'
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.get_category_display()}] {self.title} - {self.user.username}"

    def get_vote_count(self):
        """投票数を取得（フェーズ3で実装）"""
        return 0  # 将来的にFeedbackVoteモデルと連携


class FeedbackReply(models.Model):
    """フィードバックへの返信"""

    # 基本情報
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE,
                                 related_name='replies', verbose_name='フィードバック')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='返信者')
    content = models.TextField('返信内容')

    # 日時
    created_at = models.DateTimeField('作成日時', auto_now_add=True)

    class Meta:
        verbose_name = 'フィードバック返信'
        verbose_name_plural = 'フィードバック返信'
        ordering = ['created_at']  # 古い順（スレッド表示のため）

    def __str__(self):
        return f"{self.feedback.title}への返信 - {self.user.username}"


class HomeCareSupportOffice(models.Model):
    """居宅介護支援事業所"""

    name = models.CharField('事業所名', max_length=100)
    office_number = models.CharField('事業所番号', max_length=20, unique=True)
    postal_code = models.CharField('郵便番号', max_length=10, blank=True)
    address = models.CharField('住所', max_length=200, blank=True)
    phone = models.CharField('電話番号', max_length=20, blank=True)
    fax = models.CharField('FAX', max_length=20, blank=True)
    manager_name = models.CharField('管理者名', max_length=100, blank=True)
    is_active = models.BooleanField('有効', default=True)
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)

    class Meta:
        verbose_name = '居宅介護支援事業所'
        verbose_name_plural = '居宅介護支援事業所'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.office_number})"


class RegionalSupportCenter(models.Model):
    """地域包括支援センター"""

    AREA_CHOICES = [
        ('tsu', '津市'),
        ('suzuka', '鈴鹿市'),
        ('kameyama', '亀山市'),
        ('matsusaka', '松阪市'),
        ('ise', '伊勢市'),
        ('yokkaichi', '四日市市'),
        ('kuwana', '桑名市'),
        ('iga', '伊賀市'),
        ('nabari', '名張市'),
        ('inabe', 'いなべ市'),
        ('kumano', '熊野市'),
        ('owase', '尾鷲市'),
        ('toba', '鳥羽市'),
        ('other', 'その他'),
    ]

    name = models.CharField('事業所名', max_length=100)
    office_number = models.CharField('事業所番号', max_length=20, unique=True)
    postal_code = models.CharField('郵便番号', max_length=10, blank=True)
    address = models.CharField('所在地', max_length=200, blank=True)
    phone = models.CharField('電話番号', max_length=20, blank=True)
    area = models.CharField('地域区分', max_length=20, choices=AREA_CHOICES, default='other')
    is_active = models.BooleanField('有効', default=True)
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)

    class Meta:
        verbose_name = '地域包括支援センター'
        verbose_name_plural = '地域包括支援センター'
        ordering = ['area', 'office_number']

    def __str__(self):
        return f"{self.name} ({self.office_number})"


# シグナルハンドラー: ログイン時に1ヶ月以上ログインがないユーザーを自動無効化
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from datetime import timedelta
from django.utils import timezone

@receiver(user_logged_in)
def check_inactive_users(sender, request, user, **kwargs):
    """ログイン時に1ヶ月以上ログインがないユーザーを自動無効化"""
    from django.contrib.auth.models import User

    # 1ヶ月前の日時を計算
    one_month_ago = timezone.now() - timedelta(days=30)

    # 1ヶ月以上ログインがないユーザーを取得
    inactive_users = User.objects.filter(
        last_login__lt=one_month_ago,
        profile__is_active=True
    ).exclude(pk=user.pk)  # 現在ログインしているユーザーは除外

    # 該当ユーザーを無効化
    for inactive_user in inactive_users:
        try:
            profile = inactive_user.profile
            profile.is_active = False
            profile.save()
        except UserProfile.DoesNotExist:
            pass
