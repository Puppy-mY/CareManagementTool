from django import forms
from .models import Facility


class FacilityForm(forms.ModelForm):
    class Meta:
        model = Facility
        fields = [
            "facility_type", "name", "region", "town", "address", "phone", "fax",
            "homepage_url", "kaigo_kohyo_url",
            "unit_private", "unit_multi",
            "traditional_private", "traditional_multi",
            "capacity",
            "is_community_based", "is_wide_area",
            "is_tokutei_shisetsu",
            "is_zaitaku_kyoka",
            "is_keihi_a", "is_keihi_b", "is_keihi_carehouse",
        ]
        widgets = {
            "facility_type": forms.Select(attrs={"class": "form-select"}),
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "施設名を入力"}),
            "region": forms.Select(attrs={"class": "form-select"}),
            "address": forms.TextInput(attrs={"class": "form-control", "placeholder": "住所を入力"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "例: 052-123-4567"}),
            "town": forms.TextInput(attrs={"class": "form-control", "placeholder": "例: ○○町△△"}),
            "fax": forms.TextInput(attrs={"class": "form-control", "placeholder": "例: 052-123-4568"}),
            "homepage_url": forms.URLInput(attrs={"class": "form-control", "placeholder": "https://..."}),
            "kaigo_kohyo_url": forms.URLInput(attrs={"class": "form-control", "placeholder": "https://..."}),
            "unit_private": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "unit_multi": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "traditional_private": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "traditional_multi": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "capacity": forms.NumberInput(attrs={"class": "form-control", "placeholder": "例: 50"}),
            "is_community_based": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "is_wide_area": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "is_tokutei_shisetsu": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "is_zaitaku_kyoka": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "is_keihi_a": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "is_keihi_b": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "is_keihi_carehouse": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("facility_type") == "軽費老人ホーム":
            if not cleaned_data.get("is_keihi_a") and not cleaned_data.get("is_keihi_b") and not cleaned_data.get("is_keihi_carehouse"):
                raise forms.ValidationError("軽費老人ホームの場合、A型・B型・ケアハウスのいずれかを選択してください。")
        return cleaned_data
