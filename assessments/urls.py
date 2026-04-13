from django.urls import path
from . import views

urlpatterns = [
    path('', views.assessment_list, name='assessment_list'),
    path('my/', views.my_assessment_list, name='my_assessment_list'),
    path('create/', views.detailed_assessment_create, name='assessment_create'),
    path('<int:pk>/', views.assessment_detail, name='assessment_detail'),
    path('<int:pk>/edit/', views.assessment_edit, name='assessment_edit'),
    path('<int:pk>/excel/', views.assessment_excel_export, name='assessment_excel_export'),
    path('<int:pk>/delete/', views.assessment_delete, name='assessment_delete'),
    path('<int:pk>/print/', views.assessment_print_view, name='assessment_print'),
    path('import/', views.assessment_import, name='assessment_import'),
]