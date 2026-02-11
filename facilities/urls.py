from django.urls import path
from . import views

app_name = "facilities"

urlpatterns = [
    path("", views.FacilityListView.as_view(), name="facility_list"),
    path("create/", views.FacilityCreateView.as_view(), name="facility_create"),
    path("<int:pk>/edit/", views.FacilityUpdateView.as_view(), name="facility_edit"),
    path("<int:pk>/delete/", views.FacilityDeleteView.as_view(), name="facility_delete"),
]
