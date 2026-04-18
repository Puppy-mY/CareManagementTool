from django.urls import path
from . import views
from . import api_views

urlpatterns = [
    path('', views.client_list, name='client_list'),
    path('all/', views.all_client_list, name='all_client_list'),

    # 具体的なパスを先に配置（<str:pk>より前に）
    path('create/', views.client_create, name='client_create'),

    # 限度額試算関連
    path('limits/', views.limit_calculation_list, name='limit_calculation_list'),
    path('limits/<int:pk>/', views.limit_calculation_detail, name='limit_calculation_detail'),

    # 事業所設定
    path('providers/', views.provider_settings, name='provider_settings'),
    path('providers/<int:provider_id>/addons/', views.provider_addon_settings, name='provider_addon_settings'),

    # 書類作成
    path('documents/<int:pk>/delete/', views.document_delete, name='document_delete'),
    path('documents/history/<int:pk>/excel/', views.document_history_excel, name='document_history_excel'),

    # サービス削除
    path('services/<int:pk>/delete/', views.delete_additional_service, name='delete_additional_service'),

    # カラーテーマ設定
    path('color-theme-settings/', views.color_theme_settings, name='color_theme_settings'),

    # カラー参照
    path('color-reference/', views.color_reference, name='color_reference'),

    # 書類ファイル名管理
    path('document-file-management/', views.document_file_management, name='document_file_management'),

    # ユーザー管理
    path('users/', views.user_list, name='user_list'),
    path('users/create/', views.user_create, name='user_create'),
    path('users/<int:pk>/edit/', views.user_edit, name='user_edit'),
    path('users/<int:pk>/delete/', views.user_delete, name='user_delete'),
    # path('user/<int:pk>/reset-password/', views.user_password_reset, name='user_password_reset'),  # 一時的にコメントアウト

    # フィードバックシステム
    path('feedback/submit/', views.feedback_submit, name='feedback_submit'),
    path('feedback/admin/', views.feedback_list_admin, name='feedback_list_admin'),
    path('feedback/admin/<int:pk>/', views.feedback_detail_admin, name='feedback_detail_admin'),
    path('feedback/admin/<int:pk>/edit/', views.feedback_edit_admin, name='feedback_edit_admin'),
    path('feedback/admin/<int:pk>/delete/', views.feedback_delete_admin, name='feedback_delete_admin'),
    path('feedback/admin/<int:pk>/status/', views.feedback_status_update, name='feedback_status_update'),
    path('feedback/admin/<int:pk>/reply/', views.feedback_reply_submit, name='feedback_reply_submit'),
    path('feedback/reply/<int:pk>/edit/', views.feedback_reply_edit, name='feedback_reply_edit'),
    path('feedback/reply/<int:pk>/delete/', views.feedback_reply_delete, name='feedback_reply_delete'),
    path('feedback/my/', views.my_feedback_list, name='my_feedback_list'),
    path('feedback/my/<int:pk>/', views.my_feedback_detail, name='my_feedback_detail'),

    # 地域包括支援センター管理
    path('support-centers/', views.support_center_list, name='support_center_list'),
    path('support-centers/create/', views.support_center_create, name='support_center_create'),
    path('support-centers/<int:pk>/edit/', views.support_center_edit, name='support_center_edit'),
    path('support-centers/<int:pk>/delete/', views.support_center_delete, name='support_center_delete'),
    path('support-centers/api/', views.support_center_api, name='support_center_api'),

    # 居宅介護支援事業所管理
    path('home-care-offices/', views.home_care_office_list, name='home_care_office_list'),
    path('home-care-offices/create/', views.home_care_office_create, name='home_care_office_create'),
    path('home-care-offices/<int:pk>/edit/', views.home_care_office_edit, name='home_care_office_edit'),
    path('home-care-offices/<int:pk>/delete/', views.home_care_office_delete, name='home_care_office_delete'),

    # 更新認定申請書・区分変更申請書
    path('<str:client_id>/document/ltc-renewal/', views.document_create_ltc_renewal, name='document_ltc_renewal'),
    path('<str:client_id>/document/ltc-change/', views.document_create_ltc_change, name='document_ltc_change'),
    path('<str:client_id>/document/ltc-withdrawal/', views.document_create_ltc_withdrawal, name='document_ltc_withdrawal'),
    path('<str:client_id>/cert-info/update/', views.client_cert_info_update, name='client_cert_info_update'),
    path('<str:client_id>/medical-info/update/', views.client_medical_info_update, name='client_medical_info_update'),

    # マスタデータ更新API
    path('office/<int:pk>/update-master/', api_views.update_office_master, name='update_office_master'),
    path('center/<int:pk>/update-master/', api_views.update_center_master, name='update_center_master'),

    # 利用者関連（<str:pk>パターンは最後に配置）
    path('<str:pk>/', views.client_detail, name='client_detail'),
    path('<str:pk>/edit/', views.client_edit, name='client_edit'),
    path('<str:pk>/delete/', views.client_delete, name='client_delete'),
    path('<str:pk>/schedule/', views.schedule_management, name='schedule_management'),
    path('<str:pk>/dementia/', views.update_dementia_status, name='update_dementia_status'),
    path('<int:pk>/update-master/', api_views.update_client_master, name='update_client_master'),
    path('<int:pk>/update-insurance/', api_views.update_client_insurance, name='update_client_insurance'),
    path('<str:client_id>/limits/create/', views.limit_calculation_create, name='limit_calculation_create'),
    path('<str:client_id>/documents/create/<str:document_type>/', views.document_create, name='document_create'),
]