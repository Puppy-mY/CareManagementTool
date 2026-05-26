from django.urls import path, include
from . import views

app_name = 'public'

urlpatterns = [
    path('fee-simulation/', views.fee_simulation, name='fee_simulation'),
    path('fax-cover-sheet/', views.fax_cover_sheet, name='fax_cover_sheet'),
    path('facilities/', views.facility_list, name='facility_list'),
]
