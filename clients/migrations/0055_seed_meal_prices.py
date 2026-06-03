from django.db import migrations

MEAL_ITEMS = [
    {'order': 100, 'item_key': 'meal_morning', 'name': '朝食', 'price_type': 'per_day', 'price': 486,
     'extra_prices': [], 'notes': '', 'is_visible': False},
    {'order': 101, 'item_key': 'meal_lunch',   'name': '昼食', 'price_type': 'per_day', 'price': 594,
     'extra_prices': [], 'notes': '', 'is_visible': False},
    {'order': 102, 'item_key': 'meal_dinner',  'name': '夕食', 'price_type': 'per_day', 'price': 770,
     'extra_prices': [], 'notes': '', 'is_visible': False},
]


def seed(apps, schema_editor):
    PaidService = apps.get_model('clients', 'PaidService')
    for item in MEAL_ITEMS:
        PaidService.objects.get_or_create(item_key=item['item_key'], defaults=item)


def unseed(apps, schema_editor):
    PaidService = apps.get_model('clients', 'PaidService')
    PaidService.objects.filter(item_key__in=[i['item_key'] for i in MEAL_ITEMS]).delete()


class Migration(migrations.Migration):
    dependencies = [('clients', '0054_update_excretion_sputum_extra_prices')]
    operations = [migrations.RunPython(seed, unseed)]
