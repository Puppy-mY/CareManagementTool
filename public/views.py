import json
import re
import time
import unicodedata
from datetime import date
from django.db.models import Case, When, IntegerField
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from urllib.parse import quote

from clients.models import (
    CareServiceOffice, MedicalInstitution,
    HomeCareSupportOffice, RegionalSupportCenter, FaxMessageTemplate,
)
from clients.views import _generate_fax_cover_sheet_standalone_bytes
from facilities.models import Facility


def care_simulator(request):
    care_levels = ['要支援1','要支援2','要介護1','要介護2','要介護3','要介護4','要介護5']
    return render(request, 'public/care_simulator.html', {'care_levels': care_levels})


def fee_simulation(request):
    import json as _json
    from clients.models import PaidService
    services = list(PaidService.objects.all())
    can_edit = request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser)
    return render(request, 'public/fee_simulation.html', {
        'paid_services_json': _json.dumps([s.to_dict() for s in services], ensure_ascii=False),
        'can_edit': can_edit,
    })


def fax_cover_sheet(request):
    if request.method == 'POST':
        class _MockOffice:
            def __init__(self, name, company_name, postal_code, address, phone, fax):
                self.name = name
                self.company_name = company_name
                self.postal_code = postal_code
                self.address = address
                self.phone = phone
                self.fax = fax

        submitter_type = request.POST.get('submitter_type', 'office')
        if submitter_type == 'person':
            sender_name  = request.POST.get('staff_name', '').strip()
            office_name  = sender_name
            office_phone = request.POST.get('office_phone', '').strip()
            office_fax   = request.POST.get('relation', '').strip()
            office_company = ''
            office_postal  = ''
            office_address = ''
        else:
            office_name    = request.POST.get('office_name', '').strip()
            office_phone   = request.POST.get('office_phone', '').strip()
            office_fax     = request.POST.get('office_fax', '').strip()
            sender_name    = request.POST.get('staff_name_office', '').strip()
            office_company = request.POST.get('office_company_name', '').strip()
            office_postal  = request.POST.get('office_postal_code', '').strip()
            office_address = request.POST.get('office_address', '').strip()

        mock_office = _MockOffice(office_name, office_company, office_postal, office_address, office_phone, office_fax) if office_name else None
        content = _generate_fax_cover_sheet_standalone_bytes(request, mock_office, sender_name)
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

    care_offices     = list(CareServiceOffice.objects.filter(office_type='external').order_by('service_type', 'name'))
    medical_insts    = list(MedicalInstitution.objects.all())
    homecare_offices = list(HomeCareSupportOffice.objects.filter(is_active=True))
    support_centers  = list(RegionalSupportCenter.objects.filter(is_active=True))

    own_office = HomeCareSupportOffice.objects.filter(
        is_active=True, name__icontains='安濃津ろまん'
    ).first()

    own_office_json = json.dumps({
        'id': own_office.id, 'name': own_office.name, 'furigana': own_office.furigana or '',
        'company_name': own_office.company_name or '',
        'office_number': own_office.office_number or '',
        'postal_code': own_office.postal_code or '', 'address': own_office.address or '',
        'phone': own_office.phone or '', 'fax': own_office.fax or '',
        'manager_name': own_office.manager_name or '',
        'staff_names': [s for s in (own_office.staff_names or []) if s],
    } if own_office else None, ensure_ascii=False)

    return render(request, 'public/fax_cover_sheet.html', {
        'care_offices':        care_offices,
        'medical_insts':       medical_insts,
        'homecare_offices':    homecare_offices,
        'support_centers':     support_centers,
        'own_office':          own_office,
        'own_office_json':     own_office_json,
        'today':               date.today(),
        'fax_template_body':   FaxMessageTemplate.get_body(),
        'service_type_choices': CareServiceOffice.SERVICE_TYPE_CHOICES,
        'area_choices':         RegionalSupportCenter.AREA_CHOICES,
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


@require_POST
def homecare_office_create(request):
    name    = request.POST.get('name', '').strip()
    furigana = request.POST.get('furigana', '').strip()
    phone   = request.POST.get('phone', '').strip()
    fax     = request.POST.get('fax', '').strip()
    if not name:
        return JsonResponse({'status': 'error', 'message': '事業所名は必須です'}, status=400)
    office_number = f'HC{int(time.time() * 1000)}'
    office = HomeCareSupportOffice.objects.create(
        name=name, furigana=furigana, phone=phone, fax=fax,
        office_number=office_number, is_active=True,
    )
    return JsonResponse({
        'status': 'ok',
        'id': office.id,
        'name': office.name,
        'furigana': office.furigana,
        'phone': office.phone,
        'fax': office.fax,
    })


@require_POST
def support_center_create(request):
    name  = request.POST.get('name', '').strip()
    phone = request.POST.get('phone', '').strip()
    area  = request.POST.get('area', 'other').strip()
    if not name:
        return JsonResponse({'status': 'error', 'message': 'センター名は必須です'}, status=400)
    office_number = f'SC{int(time.time() * 1000)}'
    center = RegionalSupportCenter.objects.create(
        name=name, phone=phone, area=area,
        office_number=office_number, is_active=True,
    )
    area_labels = dict(RegionalSupportCenter.AREA_CHOICES)
    return JsonResponse({
        'status': 'ok',
        'id': center.id,
        'name': center.name,
        'phone': center.phone,
        'area': center.area,
        'area_label': area_labels.get(center.area, center.area),
    })


# ==============================================================================
# 公開マスタ管理ページ（居宅介護支援事業所 / 包括支援センター / 介護サービス / 医療機関）
# ==============================================================================

# ---- 居宅介護支援事業所 ----

def pub_homecare_office_list(request):
    offices = HomeCareSupportOffice.objects.all().order_by('name')
    for o in offices:
        staff = [n for n in (o.staff_names or []) if n]
        o.all_staff_names = staff
        o.staff_names_json = json.dumps(staff, ensure_ascii=False)
    return render(request, 'public/homecare_office_list.html', {'offices': offices})


@require_POST
def pub_homecare_office_create(request):
    name = request.POST.get('name', '').strip()
    office_number = request.POST.get('office_number', '').strip()
    if not name or not office_number:
        return JsonResponse({'success': False, 'error': '事業所名と事業所番号は必須です。'})
    if HomeCareSupportOffice.objects.filter(office_number=office_number).exists():
        return JsonResponse({'success': False, 'error': 'この事業所番号は既に登録されています。'})
    office = HomeCareSupportOffice.objects.create(
        company_name=request.POST.get('company_name', '').strip(),
        name=name,
        furigana=request.POST.get('furigana', '').strip(),
        office_number=office_number,
        postal_code=request.POST.get('postal_code', '').strip(),
        address=request.POST.get('address', '').strip(),
        phone=request.POST.get('phone', '').strip(),
        fax=request.POST.get('fax', '').strip(),
        manager_name=request.POST.get('manager_name', '').strip().replace('　', ' '),
        staff_names=[s.strip().replace('　', ' ') for s in request.POST.getlist('staff_names[]') if s.strip()],
        is_active=True,
    )
    return JsonResponse({
        'success': True, 'pk': office.pk,
        'name': office.name, 'furigana': office.furigana or '',
        'office_number': office.office_number,
        'postal_code': office.postal_code or '', 'address': office.address or '',
        'phone': office.phone or '', 'fax': office.fax or '',
        'staff_names': office.staff_names or [],
    })


@require_POST
def pub_homecare_office_edit(request, pk):
    office = get_object_or_404(HomeCareSupportOffice, pk=pk)
    name = request.POST.get('name', '').strip()
    office_number = request.POST.get('office_number', '').strip()
    if not name or not office_number:
        return JsonResponse({'success': False, 'error': '事業所名と事業所番号は必須です。'})
    if HomeCareSupportOffice.objects.filter(office_number=office_number).exclude(pk=pk).exists():
        return JsonResponse({'success': False, 'error': 'この事業所番号は既に登録されています。'})
    office.company_name = request.POST.get('company_name', '').strip()
    office.name = name
    office.furigana = request.POST.get('furigana', '').strip()
    office.office_number = office_number
    office.postal_code = request.POST.get('postal_code', '').strip()
    office.address = request.POST.get('address', '').strip()
    office.phone = request.POST.get('phone', '').strip()
    office.fax = request.POST.get('fax', '').strip()
    office.manager_name = request.POST.get('manager_name', '').strip().replace('　', ' ')
    office.staff_names = [s.strip().replace('　', ' ') for s in request.POST.getlist('staff_names[]') if s.strip()]
    office.is_active = request.POST.get('is_active') == 'true'
    office.save()
    return JsonResponse({'success': True, 'staff_names': office.staff_names or []})


@require_POST
def pub_homecare_office_delete(request, pk):
    get_object_or_404(HomeCareSupportOffice, pk=pk).delete()
    return JsonResponse({'success': True})


# ---- 地域包括支援センター ----

def pub_support_center_list(request):
    area_order = Case(
        When(area='tsu', then=1), When(area='suzuka', then=2), When(area='kameyama', then=3),
        When(area='matsusaka', then=4), When(area='ise', then=5), When(area='yokkaichi', then=6),
        When(area='kuwana', then=7), When(area='iga', then=8), When(area='nabari', then=9),
        When(area='inabe', then=10), When(area='kumano', then=11), When(area='owase', then=12),
        When(area='toba', then=13), When(area='other', then=14),
        output_field=IntegerField(),
    )
    centers = RegionalSupportCenter.objects.all().order_by(area_order, 'name')
    return render(request, 'public/support_center_list.html', {
        'centers': centers,
        'area_choices': RegionalSupportCenter.AREA_CHOICES,
    })


@require_POST
def pub_support_center_create(request):
    name = request.POST.get('name', '').strip()
    office_number = request.POST.get('office_number', '').strip()
    if not name or not office_number:
        return JsonResponse({'success': False, 'error': '事業所名と事業所番号は必須です。'})
    if RegionalSupportCenter.objects.filter(office_number=office_number).exists():
        return JsonResponse({'success': False, 'error': 'この事業所番号は既に登録されています。'})
    center = RegionalSupportCenter.objects.create(
        name=name,
        office_number=office_number,
        postal_code=request.POST.get('postal_code', '').strip(),
        address=request.POST.get('address', '').strip(),
        phone=request.POST.get('phone', '').strip(),
        fax=request.POST.get('fax', '').strip(),
        persons=[p.strip() for p in request.POST.getlist('staff_names[]') if p.strip()],
        area=request.POST.get('area', 'other'),
        is_active=True,
    )
    return JsonResponse({'success': True, 'id': center.pk,
                         'area_label': center.get_area_display()})


@require_POST
def pub_support_center_edit(request, pk):
    center = get_object_or_404(RegionalSupportCenter, pk=pk)
    name = request.POST.get('name', '').strip()
    office_number = request.POST.get('office_number', '').strip()
    if not name or not office_number:
        return JsonResponse({'success': False, 'error': '事業所名と事業所番号は必須です。'})
    if RegionalSupportCenter.objects.filter(office_number=office_number).exclude(pk=pk).exists():
        return JsonResponse({'success': False, 'error': 'この事業所番号は既に登録されています。'})
    center.name = name
    center.office_number = office_number
    center.postal_code = request.POST.get('postal_code', '').strip()
    center.address = request.POST.get('address', '').strip()
    center.phone = request.POST.get('phone', '').strip()
    center.fax = request.POST.get('fax', '').strip()
    center.persons = [p.strip() for p in request.POST.getlist('staff_names[]') if p.strip()]
    center.area = request.POST.get('area', 'other')
    center.save()
    return JsonResponse({'success': True})


@require_POST
def pub_support_center_delete(request, pk):
    get_object_or_404(RegionalSupportCenter, pk=pk).delete()
    return JsonResponse({'success': True})


# ---- 介護サービス事業所 ----

def pub_care_service_office_list(request):
    svc_labels = dict(CareServiceOffice.SERVICE_TYPE_CHOICES)
    offices = list(CareServiceOffice.objects.filter(office_type='external').order_by('name'))
    for o in offices:
        o.service_type_label = svc_labels.get(o.service_type, o.service_type)
    return render(request, 'public/care_service_office_list.html', {
        'offices': offices,
        'service_type_choices': CareServiceOffice.SERVICE_TYPE_CHOICES,
    })


@require_POST
def pub_care_service_office_create(request):
    name = request.POST.get('name', '').strip()
    service_type = request.POST.get('service_type', '').strip()
    phone = request.POST.get('phone', '').strip()
    fax = request.POST.get('fax', '').strip()
    if not name:
        return JsonResponse({'success': False, 'error': '事業所名は必須です。'})
    if not service_type:
        return JsonResponse({'success': False, 'error': '事業所種類を選択してください。'})
    if not phone or not fax:
        return JsonResponse({'success': False, 'error': '電話番号とFAX番号は必須です。'})
    office = CareServiceOffice.objects.create(
        company_name=request.POST.get('company_name', '').strip(),
        name=name,
        furigana=request.POST.get('furigana', '').strip(),
        service_type=service_type,
        office_type='external',
        office_number=request.POST.get('office_number', '').strip(),
        postal_code=request.POST.get('postal_code', '').strip(),
        address=request.POST.get('address', '').strip(),
        phone=phone,
        fax=fax,
        persons=[p.strip().replace('　', ' ') for p in request.POST.getlist('staff_names[]') if p.strip()],
    )
    return JsonResponse({'success': True, 'id': office.pk})


@require_POST
def pub_care_service_office_update(request, pk):
    office = get_object_or_404(CareServiceOffice, pk=pk)
    name = request.POST.get('name', office.name).strip()
    service_type = request.POST.get('service_type', '').strip()
    phone = request.POST.get('phone', office.phone).strip()
    fax = request.POST.get('fax', office.fax).strip()
    if not name:
        return JsonResponse({'success': False, 'error': '事業所名は必須です。'})
    if not service_type:
        return JsonResponse({'success': False, 'error': '事業所種類を選択してください。'})
    if not phone or not fax:
        return JsonResponse({'success': False, 'error': '電話番号とFAX番号は必須です。'})
    office.company_name = request.POST.get('company_name', office.company_name).strip()
    office.name = name
    office.furigana = request.POST.get('furigana', office.furigana).strip()
    office.service_type = service_type
    office.office_number = request.POST.get('office_number', office.office_number).strip()
    office.postal_code = request.POST.get('postal_code', office.postal_code).strip()
    office.address = request.POST.get('address', office.address).strip()
    office.phone = phone
    office.fax = fax
    office.persons = [p.strip().replace('　', ' ') for p in request.POST.getlist('staff_names[]') if p.strip()]
    office.save()
    return JsonResponse({'success': True})


@require_POST
def pub_care_service_office_delete(request, pk):
    get_object_or_404(CareServiceOffice, pk=pk).delete()
    return JsonResponse({'success': True})


# ---- 主治医・医療機関 ----

def pub_medical_institution_list(request):
    institutions = MedicalInstitution.objects.all().order_by('hospital_name')
    return render(request, 'public/medical_institution_list.html', {'institutions': institutions})


@require_POST
def pub_medical_institution_create(request):
    hospital_name = request.POST.get('hospital_name', '').strip()
    if not hospital_name:
        return JsonResponse({'success': False, 'error': '医療機関名は必須です。'})
    inst = MedicalInstitution.objects.create(
        corp_name=re.sub(r'[ 　]+', ' ', request.POST.get('corp_name', '').strip()),
        hospital_name=hospital_name,
        hospital_furigana=unicodedata.normalize('NFKC', request.POST.get('hospital_furigana', '').strip()),
        doctors=[' '.join(n.split()) for n in request.POST.getlist('doctor_name') if n.strip()],
        phone=request.POST.get('phone', '').strip(),
        fax=request.POST.get('fax', '').strip(),
        postal_code=request.POST.get('postal_code', '').strip(),
        address=request.POST.get('address', '').strip(),
    )
    return JsonResponse({'success': True, 'id': inst.pk})


@require_POST
def pub_medical_institution_update(request, pk):
    inst = get_object_or_404(MedicalInstitution, pk=pk)
    hospital_name = request.POST.get('hospital_name', '').strip()
    if not hospital_name:
        return JsonResponse({'success': False, 'error': '医療機関名は必須です。'})
    inst.corp_name = re.sub(r'[ 　]+', ' ', request.POST.get('corp_name', '').strip())
    inst.hospital_name = hospital_name
    inst.hospital_furigana = unicodedata.normalize('NFKC', request.POST.get('hospital_furigana', '').strip())
    inst.doctors = [' '.join(n.split()) for n in request.POST.getlist('doctor_name') if n.strip()]
    inst.phone = request.POST.get('phone', '').strip()
    inst.fax = request.POST.get('fax', '').strip()
    inst.postal_code = request.POST.get('postal_code', '').strip()
    inst.address = request.POST.get('address', '').strip()
    inst.save()
    return JsonResponse({'success': True})


@require_POST
def pub_medical_institution_delete(request, pk):
    get_object_or_404(MedicalInstitution, pk=pk).delete()
    return JsonResponse({'success': True})
