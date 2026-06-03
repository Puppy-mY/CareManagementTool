from django.db import migrations

MEAL_TAX_EXCLUSIVE = {
    'meal_morning': 480,
    'meal_lunch':   580,
    'meal_dinner':  730,
}

MEAL_TAX_INCLUSIVE = {
    'meal_morning': 486,
    'meal_lunch':   594,
    'meal_dinner':  770,
}


def to_exclusive(apps, schema_editor):
    PaidService = apps.get_model('clients', 'PaidService')
    for key, price in MEAL_TAX_EXCLUSIVE.items():
        PaidService.objects.filter(item_key=key).update(price=price)


def to_inclusive(apps, schema_editor):
    PaidService = apps.get_model('clients', 'PaidService')
    for key, price in MEAL_TAX_INCLUSIVE.items():
        PaidService.objects.filter(item_key=key).update(price=price)


class Migration(migrations.Migration):
    dependencies = [('clients', '0055_seed_meal_prices')]
    operations = [migrations.RunPython(to_exclusive, to_inclusive)]
