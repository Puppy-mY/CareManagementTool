from django.db import migrations


def to_tax_exclusive(apps, schema_editor):
    PaidService = apps.get_model('clients', 'PaidService')
    for svc in PaidService.objects.all():
        # price が 11 の倍数なら ÷1.1
        if svc.price and svc.price % 11 == 0:
            svc.price = svc.price * 10 // 11
        # extra_prices の各 value も同様
        new_eps = []
        for ep in (svc.extra_prices or []):
            ep = dict(ep)
            v = ep.get('value', 0)
            if v and v % 11 == 0:
                ep['value'] = v * 10 // 11
            new_eps.append(ep)
        svc.extra_prices = new_eps
        svc.save()


def to_tax_inclusive(apps, schema_editor):
    PaidService = apps.get_model('clients', 'PaidService')
    for svc in PaidService.objects.all():
        if svc.price:
            svc.price = svc.price * 11 // 10
        new_eps = []
        for ep in (svc.extra_prices or []):
            ep = dict(ep)
            v = ep.get('value', 0)
            if v:
                ep['value'] = v * 11 // 10
            new_eps.append(ep)
        svc.extra_prices = new_eps
        svc.save()


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0052_seed_paid_services'),
    ]

    operations = [
        migrations.RunPython(to_tax_exclusive, to_tax_inclusive),
    ]
