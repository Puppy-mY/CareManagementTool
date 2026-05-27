from django.urls import path, include
from . import views

app_name = 'public'

urlpatterns = [
    path('fee-simulation/', views.fee_simulation, name='fee_simulation'),
    path('fax-cover-sheet/', views.fax_cover_sheet, name='fax_cover_sheet'),
    path('facilities/', views.facility_list, name='facility_list'),
    # FAX送付状用（既存）
    path('homecare-office/create/', views.homecare_office_create, name='homecare_office_create'),
    path('support-center/create/', views.support_center_create, name='support_center_create'),
    # 居宅介護支援事業所マスタ管理
    path('homecare-offices/', views.pub_homecare_office_list, name='pub_homecare_office_list'),
    path('homecare-offices/create/', views.pub_homecare_office_create, name='pub_homecare_office_create'),
    path('homecare-offices/<int:pk>/edit/', views.pub_homecare_office_edit, name='pub_homecare_office_edit'),
    path('homecare-offices/<int:pk>/delete/', views.pub_homecare_office_delete, name='pub_homecare_office_delete'),
    # 地域包括支援センターマスタ管理
    path('support-centers/', views.pub_support_center_list, name='pub_support_center_list'),
    path('support-centers/create/', views.pub_support_center_create, name='pub_support_center_create'),
    path('support-centers/<int:pk>/edit/', views.pub_support_center_edit, name='pub_support_center_edit'),
    path('support-centers/<int:pk>/delete/', views.pub_support_center_delete, name='pub_support_center_delete'),
    # 介護サービス事業所マスタ管理
    path('care-service-offices/', views.pub_care_service_office_list, name='pub_care_service_office_list'),
    path('care-service-offices/create/', views.pub_care_service_office_create, name='pub_care_service_office_create'),
    path('care-service-offices/<int:pk>/update/', views.pub_care_service_office_update, name='pub_care_service_office_update'),
    path('care-service-offices/<int:pk>/delete/', views.pub_care_service_office_delete, name='pub_care_service_office_delete'),
    # 主治医・医療機関マスタ管理
    path('medical-institutions/', views.pub_medical_institution_list, name='pub_medical_institution_list'),
    path('medical-institutions/create/', views.pub_medical_institution_create, name='pub_medical_institution_create'),
    path('medical-institutions/<int:pk>/update/', views.pub_medical_institution_update, name='pub_medical_institution_update'),
    path('medical-institutions/<int:pk>/delete/', views.pub_medical_institution_delete, name='pub_medical_institution_delete'),
]
