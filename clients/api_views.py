from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
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
        client.insurance_number = data.get('insurance_number', client.insurance_number)
        client.save()

        return JsonResponse({'success': True, 'message': '利用者マスタデータを更新しました。'})
    except Exception as e:
        logger.error(f'Error updating client master: {e}')
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
