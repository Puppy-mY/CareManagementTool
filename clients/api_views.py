from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
import json
import logging

from .models import Client, HomeCareSupportOffice, RegionalSupportCenter

logger = logging.getLogger(__name__)


@login_required
def update_client_master(request, pk):
    """利用者マスタデータ更新API"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'POSTメソッドのみ対応しています。'})

    try:
        client = get_object_or_404(Client, pk=pk)
        data = json.loads(request.body)

        # データを更新
        client.name = data.get('name', client.name)
        client.furigana = data.get('furigana', client.furigana)
        client.birth_date = data.get('birth_date', client.birth_date)
        client.address = data.get('address', client.address)
        if 'postal_code' in data:
            client.postal_code = data['postal_code']
        if 'gender' in data:
            g = data['gender']
            client.gender = g if g in ('male', 'female') else ('male' if g == '男' else ('female' if g == '女' else g))
        if 'phone' in data:
            client.phone = data['phone']
        if 'charge_manager_id' in data:
            mgr_id = data['charge_manager_id']
            if mgr_id:
                try:
                    client.charge_manager = User.objects.get(pk=int(mgr_id))
                    client.charge_manager_other = ''
                except (User.DoesNotExist, ValueError):
                    client.charge_manager = None
            else:
                client.charge_manager = None
        if 'charge_manager_other' in data:
            client.charge_manager_other = data['charge_manager_other'] or ''
        client.save()

        profile = getattr(client.charge_manager, 'profile', None) if client.charge_manager else None
        mgr_display = (profile.get_full_name() if profile and profile.get_full_name().strip() else (client.charge_manager.username if client.charge_manager else '')) or client.charge_manager_other or ''

        return JsonResponse({'success': True, 'message': '利用者マスタデータを更新しました。', 'charge_manager_display': mgr_display})
    except Exception as e:
        logger.error(f'Error updating client master: {e}')
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def update_client_insurance(request, pk):
    """利用者介護保険情報更新API"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'POSTメソッドのみ対応しています。'})

    try:
        from datetime import date as date_cls
        client = get_object_or_404(Client, pk=pk)
        data = json.loads(request.body)

        client.insurance_number = data.get('insurance_number', client.insurance_number)
        if 'care_level' in data:
            client.care_level = data['care_level']
        if 'care_burden' in data:
            client.care_burden = data['care_burden']

        def parse_date(val):
            if not val:
                return None
            try:
                from datetime import datetime
                return datetime.strptime(val, '%Y-%m-%d').date()
            except Exception:
                return None

        if 'certification_date' in data:
            client.certification_date = parse_date(data['certification_date'])
        if 'certification_period_start' in data:
            client.certification_period_start = parse_date(data['certification_period_start'])
        if 'certification_period_end' in data:
            client.certification_period_end = parse_date(data['certification_period_end'])

        client.save()

        def to_wareki(d):
            if not d:
                return '', ''
            iso = d.strftime('%Y-%m-%d')
            y, m, day = d.year, d.month, d.day
            for era_name, era_start in [('令和', 2019), ('平成', 1989), ('昭和', 1926), ('大正', 1912), ('明治', 1868)]:
                if y >= era_start:
                    return era_name + str(y - era_start + 1) + '年' + str(m) + '月' + str(day) + '日', iso
            return iso, iso

        cert_date_disp, _ = to_wareki(client.certification_date)
        cert_start_disp, _ = to_wareki(client.certification_period_start)
        cert_end_disp, _ = to_wareki(client.certification_period_end)

        return JsonResponse({
            'success': True,
            'message': '介護保険情報を更新しました。',
            'care_level_display': client.get_care_level_display() if client.care_level else '',
            'certification_date_display': cert_date_disp,
            'certification_period_start_display': cert_start_disp,
            'certification_period_end_display': cert_end_disp,
        })
    except Exception as e:
        logger.error(f'Error updating client insurance: {e}')
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def update_office_master(request, pk):
    """事業所マスタデータ更新API"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'POSTメソッドのみ対応しています。'})

    try:
        office = get_object_or_404(HomeCareSupportOffice, pk=pk)
        data = json.loads(request.body)

        # データを更新
        office.office_number = data.get('office_number', office.office_number)
        office.postal_code = data.get('postal_code', office.postal_code)
        office.address = data.get('address', office.address)
        office.phone = data.get('phone', office.phone)
        office.save()

        return JsonResponse({'success': True, 'message': '事業所マスタデータを更新しました。'})
    except Exception as e:
        logger.error(f'Error updating office master: {e}')
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def update_center_master(request, pk):
    """地域包括支援センターマスタデータ更新API"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'POSTメソッドのみ対応しています。'})

    try:
        center = get_object_or_404(RegionalSupportCenter, pk=pk)
        data = json.loads(request.body)

        # データを更新
        center.office_number = data.get('office_number', center.office_number)
        center.postal_code = data.get('postal_code', center.postal_code)
        center.address = data.get('address', center.address)
        center.phone = data.get('phone', center.phone)
        center.save()

        return JsonResponse({'success': True, 'message': '地域包括支援センターマスタデータを更新しました。'})
    except Exception as e:
        logger.error(f'Error updating center master: {e}')
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def api_users_list(request):
    """ユーザー一覧API（担当ケアマネージャー選択用）"""
    from .models import UserProfile
    users = []
    for u in User.objects.filter(is_active=True).select_related('profile').order_by('profile__last_name', 'profile__first_name'):
        profile = getattr(u, 'profile', None)
        name = profile.get_full_name() if profile else ''
        if not name.strip():
            name = u.username
        users.append({'id': u.id, 'name': name})
    return JsonResponse({'users': users})

