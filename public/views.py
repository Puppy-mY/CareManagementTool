import json
from datetime import date
from django.shortcuts import render
from django.http import HttpResponse
from urllib.parse import quote

from clients.models import (
    CareServiceOffice, MedicalInstitution,
    HomeCareSupportOffice, RegionalSupportCenter, FaxMessageTemplate,
)
from clients.views import _generate_fax_cover_sheet_standalone_bytes
from facilities.models import Facility


def fee_simulation(request):
    return render(request, 'public/fee_simulation.html', {})


def fax_cover_sheet(request):
    if request.method == 'POST':
        content = _generate_fax_cover_sheet_standalone_bytes(request, None, '')
        dl_name = 'FAX送付状.xlsx'
        response = HttpResponse(
            content,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )
        response['Content-Disposition'] = (
            f"attachment; filename=\"download.xlsx\"; "
            f"filename*=UTF-8''{quote(dl_name, safe='')}"
        )
        return response

    care_offices     = list(CareServiceOffice.objects.filter(office_type='external'))
    medical_insts    = list(MedicalInstitution.objects.all())
    homecare_offices = list(HomeCareSupportOffice.objects.filter(is_active=True))
    support_centers  = list(RegionalSupportCenter.objects.filter(is_active=True))

    return render(request, 'public/fax_cover_sheet.html', {
        'care_offices':     care_offices,
        'medical_insts':    medical_insts,
        'homecare_offices': homecare_offices,
        'support_centers':  support_centers,
        'today':            date.today(),
        'fax_template_body': FaxMessageTemplate.get_body(),
    })


def facility_list(request):
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
    facilities = list(Facility.objects.values(
        "id", "facility_type", "name", "region", "address", "phone", "town", "fax",
        "homepage_url", "kaigo_kohyo_url",
        "unit_private", "unit_multi",
        "traditional_private", "traditional_multi",
        "capacity", "notes",
        "is_community_based", "is_wide_area", "is_tokutei_shisetsu",
        "is_zaitaku_kyoka",
        "is_keihi_a", "is_keihi_b", "is_keihi_carehouse",
    ))
    existing_types = set(Facility.objects.values_list("facility_type", flat=True).distinct())
    facility_types = [
        {"value": ft, "label": label}
        for ft, label in FACILITY_TYPE_ORDER if ft in existing_types
    ]
    regions = (
        Facility.objects.values_list("region", flat=True)
        .distinct()
        .order_by("region")
    )
    return render(request, 'public/facility_list.html', {
        'facilities':      facilities,
        'facilities_json': json.dumps(facilities, ensure_ascii=False),
        'facility_types':  facility_types,
        'regions':         regions,
    })
