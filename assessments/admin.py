from django.contrib import admin
from .models import Assessment


@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ['client', 'assessment_date', 'assessor', 'assessment_type', 'status', 'created_at']
    list_filter = ['assessment_type', 'status', 'assessment_date', 'interview_location']
    search_fields = ['client__name', 'client__client_id']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('基本情報', {
            'fields': ('client', 'assessment_date', 'assessor', 'assessment_type', 'interview_location', 'status')
        }),
        ('アセスメント項目', {
            'fields': ('basic_info', 'insurance_info', 'family_situation', 'living_situation', 'services')
        }),
        ('健康・身体状況', {
            'fields': ('health_status', 'physical_status', 'cognitive_function')
        }),
        ('日常生活動作', {
            'fields': ('basic_activities', 'adl', 'iadl')
        }),
        ('総合評価', {
            'fields': ('general_assessment', 'support_goals', 'total_score')
        }),
        ('管理情報', {
            'fields': ('created_at', 'updated_at')
        })
    )
