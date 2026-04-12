from django.contrib import admin
from .models import Client, ServiceType, LimitCalculation, AdditionalService, Feedback, FeedbackReply


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['insurance_number', 'name', 'furigana', 'birth_date', 'gender', 'care_level', 'created_at']
    list_filter = ['gender', 'care_level', 'created_at']
    search_fields = ['insurance_number', 'name', 'furigana']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('基本情報', {
            'fields': ('insurance_number', 'name', 'furigana', 'birth_date', 'gender', 'phone', 'address')
        }),
        ('保険情報', {
            'fields': ('care_level', 'certification_date', 'certification_period_start', 'certification_period_end', 
                      'care_burden', 'burden_period_start', 'burden_period_end')
        }),
        ('家族情報（1人目）', {
            'fields': ('family_name1', 'family_relationship1', 'family_relationship_detail1', 'family_address1', 'family_living_status1',
                      'family_care_status1', 'family_employment1', 'family_contact1', 'family_notes1'),
            'classes': ('collapse',)
        }),
        ('家族情報（2人目）', {
            'fields': ('family_name2', 'family_relationship2', 'family_relationship_detail2', 'family_address2', 'family_living_status2',
                      'family_care_status2', 'family_employment2', 'family_contact2', 'family_notes2'),
            'classes': ('collapse',)
        }),
        ('システム情報', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(ServiceType)
class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'unit_per_minute', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name']


class AdditionalServiceInline(admin.TabularInline):
    model = AdditionalService
    extra = 0
    readonly_fields = ['total_units']
    
    def total_units(self, obj):
        if obj.id:
            return f"{obj.total_units:.1f}単位"
        return "-"
    total_units.short_description = '単位数'


@admin.register(LimitCalculation)
class LimitCalculationAdmin(admin.ModelAdmin):
    list_display = ['client', 'year', 'month', 'care_manager_units', 'total_used_units', 'remaining_units', 'is_over_limit']
    list_filter = ['year', 'month']
    search_fields = ['client__name', 'client__insurance_number']
    inlines = [AdditionalServiceInline]
    
    def total_used_units(self, obj):
        return f"{obj.total_used_units:.1f}単位"
    total_used_units.short_description = '使用済み単位'
    
    def remaining_units(self, obj):
        return f"{obj.remaining_units:.1f}単位"
    remaining_units.short_description = '残り単位'
    
    def is_over_limit(self, obj):
        return "超過" if obj.is_over_limit else "範囲内"
    is_over_limit.short_description = '限度額状況'
    is_over_limit.boolean = True


@admin.register(AdditionalService)
class AdditionalServiceAdmin(admin.ModelAdmin):
    list_display = ['limit_calculation', 'service_type', 'minutes', 'total_units', 'date_provided', 'provider_name']
    list_filter = ['service_type', 'date_provided']
    search_fields = ['limit_calculation__client__name', 'provider_name']

    def total_units(self, obj):
        return f"{obj.total_units:.1f}単位"
    total_units.short_description = '単位数'


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['id', 'category_badge', 'title', 'user', 'priority', 'status_badge', 'created_at']
    list_filter = ['category', 'status', 'priority', 'created_at']
    search_fields = ['title', 'content', 'user__username']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('基本情報', {
            'fields': ('user', 'category', 'title', 'content', 'priority')
        }),
        ('ステータス', {
            'fields': ('status',)
        }),
        ('追加情報', {
            'fields': ('page_url',)
        }),
        ('システム情報', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    def category_badge(self, obj):
        colors = {
            'bug': '#dc3545',
            'feature': '#0d6efd',
            'improvement': '#198754',
            'other': '#6c757d',
        }
        color = colors.get(obj.category, '#6c757d')
        return f'<span style="background-color: {color}; color: white; padding: 3px 8px; border-radius: 3px; font-size: 11px;">{obj.get_category_display()}</span>'
    category_badge.short_description = 'カテゴリ'
    category_badge.allow_tags = True

    def status_badge(self, obj):
        colors = {
            'new': '#0dcaf0',
            'in_progress': '#ffc107',
            'completed': '#198754',
            'rejected': '#6c757d',
        }
        color = colors.get(obj.status, '#6c757d')
        return f'<span style="background-color: {color}; color: white; padding: 3px 8px; border-radius: 3px; font-size: 11px;">{obj.get_status_display()}</span>'
    status_badge.short_description = 'ステータス'
    status_badge.allow_tags = True


@admin.register(FeedbackReply)
class FeedbackReplyAdmin(admin.ModelAdmin):
    list_display = ['id', 'feedback', 'user', 'created_at', 'content_preview']
    list_filter = ['created_at', 'user']
    search_fields = ['content', 'feedback__title', 'user__username']
    readonly_fields = ['created_at']

    fieldsets = (
        ('基本情報', {
            'fields': ('feedback', 'user', 'content')
        }),
        ('システム情報', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )

    def content_preview(self, obj):
        """返信内容のプレビュー（最初の50文字）"""
        if len(obj.content) > 50:
            return obj.content[:50] + '...'
        return obj.content
    content_preview.short_description = '返信内容'
