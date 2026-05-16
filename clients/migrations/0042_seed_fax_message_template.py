from django.db import migrations

DEFAULT_BODY = (
    'いつもお世話になっております。\n'
    '{office_name}の{user_name}です。\n'
    '\n'
    'サービス担当者会議開催のご案内をお送りします。ご多忙のところ誠に恐れ入りますが、\n'
    'ご確認いただけますようよろしくお願いいたします。'
)


def seed_fax_template(apps, schema_editor):
    FaxMessageTemplate = apps.get_model('clients', 'FaxMessageTemplate')
    FaxMessageTemplate.objects.get_or_create(pk=1, defaults={'body': DEFAULT_BODY})


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0041_add_fax_message_template'),
    ]

    operations = [
        migrations.RunPython(seed_fax_template, migrations.RunPython.noop),
    ]
