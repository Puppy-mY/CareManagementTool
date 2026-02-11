from django.db import models
from django.contrib.auth.models import User
from clients.models import Client
from django.utils import timezone


class Assessment(models.Model):
    ASSESSMENT_TYPE_CHOICES = [
        ('new', '新規'),
        ('update', '更新'),
        ('change', '区分変更'),
        ('discharge', '退院'),
        ('information', '情報提供'),
        ('other', 'その他'),
    ]
    
    INTERVIEW_LOCATION_CHOICES = [
        ('room', '居室'),
        ('home', '自宅'),
        ('hospital', '病院'),
        ('facility', '施設'),
        ('other', 'その他'),
    ]
    
    STATUS_CHOICES = [
        ('draft', '下書き'),
        ('completed', '完了'),
    ]
    
    # 基本情報
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='利用者', related_name='assessments')
    assessment_date = models.DateField('作成日', default=timezone.now)
    assessor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='作成者')
    assessment_type = models.CharField('アセスメントの理由', max_length=20, choices=ASSESSMENT_TYPE_CHOICES)
    assessment_type_other = models.CharField('アセスメントの理由その他', max_length=100, blank=True, null=True)
    interview_location = models.CharField('面談場所', max_length=30, choices=INTERVIEW_LOCATION_CHOICES)
    interview_location_other = models.CharField('面談場所その他', max_length=100, blank=True, null=True)
    
    # アセスメント項目のデータ（JSON形式で格納）
    basic_info = models.JSONField('基本情報', default=dict, blank=True, help_text='生活歴、本人・家族の希望等')
    insurance_info = models.JSONField('保険情報', default=dict, blank=True, help_text='介護度、負担割合、医療保険等')
    family_situation = models.JSONField('家族状況', default=dict, blank=True, help_text='家族情報')
    living_situation = models.JSONField('居住状況', default=dict, blank=True, help_text='住居環境、設備等')
    services = models.JSONField('利用サービス', default=dict, blank=True, help_text='介護サービス、福祉用具等')
    health_status = models.JSONField('健康状態', default=dict, blank=True, help_text='疾患、医師、服薬、アレルギー等')
    physical_status = models.JSONField('身体状況', default=dict, blank=True, help_text='皮膚疾患、感染症、身長体重等')
    cognitive_function = models.JSONField('認知機能', default=dict, blank=True, help_text='認知症、BPSD、会話等')
    basic_activities = models.JSONField('基本動作', default=dict, blank=True, help_text='寝返り、起き上がり、移乗等')
    adl = models.JSONField('ADL', default=dict, blank=True, help_text='食事、入浴、排泄等')
    iadl = models.JSONField('IADL', default=dict, blank=True, help_text='調理、掃除、洗濯等')
    
    # 総合評価
    general_assessment = models.TextField('総合所見', blank=True)
    support_goals = models.TextField('支援目標', blank=True)
    total_score = models.IntegerField('総合得点', null=True, blank=True)
    
    # 管理情報
    status = models.CharField('ステータス', max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)
    
    class Meta:
        verbose_name = 'アセスメント'
        verbose_name_plural = 'アセスメント'
        ordering = ['-assessment_date', '-created_at']
    
    def __str__(self):
        return f"{self.client.name} - {self.assessment_date} ({self.get_assessment_type_display()})"
    
    def save(self, *args, **kwargs):
        # デフォルトのJSON構造を設定
        if not self.basic_info:
            self.basic_info = {
                'life_history': '',
                'personal_hopes': '',
                'family_hopes': ''
            }
        
        if not self.insurance_info:
            self.insurance_info = {
                'care_level': '',
                'burden_ratio': '',
                'medical_insurance': '',
                'disability_handbook': False
            }
        
        if not self.health_status:
            self.health_status = {
                'diseases': [],
                'medical_history': '',
                'main_doctor': '',
                'outpatient_clinic': '',
                'medications': '',
                'allergies': False
            }
        
        super().save(*args, **kwargs)
