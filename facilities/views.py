import json
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Facility
from .forms import FacilityForm


class FacilityListView(LoginRequiredMixin, ListView):
    model = Facility
    template_name = "facilities/facility_list.html"
    context_object_name = "facilities"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        facilities = list(self.get_queryset().values(
            "id", "facility_type", "name", "region", "address", "phone", "town", "fax",
            "homepage_url", "kaigo_kohyo_url",
            "unit_private", "unit_multi",
            "traditional_private", "traditional_multi",
            "capacity", "notes",
            "is_community_based", "is_wide_area", "is_tokutei_shisetsu",
            "is_zaitaku_kyoka",
            "is_keihi_a", "is_keihi_b", "is_keihi_carehouse",
        ))
        context["facilities_json"] = json.dumps(facilities, ensure_ascii=False)
        # 登録済みデータに存在する地域のみ取得
        context["regions"] = (
            Facility.objects.values_list("region", flat=True)
            .distinct()
            .order_by("region")
        )
        FACILITY_TYPE_ORDER = [
            ("特別養護老人ホーム", "特養"),
            ("サービス付き高齢者向け住宅", "サ高住"),
            ("介護老人保健施設", "老健"),
            ("グループホーム", "GH"),
            ("有料老人ホーム", "有料"),
            ("軽費老人ホーム", "軽費"),
            ("養護老人ホーム", "養護"),
            ("介護医療院", "医療院"),
            ("その他", "その他"),
        ]
        existing_types = set(
            Facility.objects.values_list("facility_type", flat=True).distinct()
        )
        context["facility_types"] = [
            {"value": ft, "label": label}
            for ft, label in FACILITY_TYPE_ORDER if ft in existing_types
        ]
        return context


class FacilityCreateView(LoginRequiredMixin, CreateView):
    model = Facility
    form_class = FacilityForm
    template_name = "facilities/facility_form.html"

    def form_valid(self, form):
        messages.success(self.request, "施設を登録しました。")
        return super().form_valid(form)

    def get_success_url(self):
        ft = self.object.facility_type
        return reverse_lazy("facilities:facility_list") + f"?type={ft}"


class FacilityUpdateView(LoginRequiredMixin, UpdateView):
    model = Facility
    form_class = FacilityForm
    template_name = "facilities/facility_form.html"

    def form_valid(self, form):
        messages.success(self.request, "施設情報を更新しました。")
        return super().form_valid(form)

    def get_success_url(self):
        ft = self.object.facility_type
        return reverse_lazy("facilities:facility_list") + f"?type={ft}"


class FacilityDeleteView(LoginRequiredMixin, DeleteView):
    model = Facility
    template_name = "facilities/facility_confirm_delete.html"
    success_url = reverse_lazy("facilities:facility_list")

    def form_valid(self, form):
        messages.success(self.request, "施設を削除しました。")
        return super().form_valid(form)
