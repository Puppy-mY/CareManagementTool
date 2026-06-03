from django.db import migrations

UNIT_PRICES = [
    {'label': '日中',       'value': 100},
    {'label': '夜間・早朝', 'value': 200},
    {'label': '深夜',       'value': 250},
]

OLD_EXCRETION = [
    {'label': '1回/日（深夜帯のみ）',          'value': 250},
    {'label': '2回/日（深夜帯・早朝帯）',      'value': 400},
    {'label': '4回/日（深夜・早朝・午前・午後）', 'value': 650},
]


def update(apps, schema_editor):
    PaidService = apps.get_model('clients', 'PaidService')
    for key in ('excretion', 'sputum'):
        try:
            svc = PaidService.objects.get(item_key=key)
            svc.extra_prices = UNIT_PRICES
            svc.save()
        except PaidService.DoesNotExist:
            pass


def revert(apps, schema_editor):
    PaidService = apps.get_model('clients', 'PaidService')
    for key in ('excretion', 'sputum'):
        try:
            svc = PaidService.objects.get(item_key=key)
            svc.extra_prices = OLD_EXCRETION
            svc.save()
        except PaidService.DoesNotExist:
            pass


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0053_update_paid_service_prices_to_tax_exclusive'),
    ]

    operations = [
        migrations.RunPython(update, revert),
    ]
