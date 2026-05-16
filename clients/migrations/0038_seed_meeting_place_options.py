from django.db import migrations

DEFAULT_OPTIONS = [
    ('ご利用者様の自宅',         False, 1),
    ('安濃津ろまん相談室',        False, 2),
    ('ご利用者様のフロアホール',  False, 3),
    ('その他',                   True,  99),
]


def seed(apps, schema_editor):
    MeetingPlaceOption = apps.get_model('clients', 'MeetingPlaceOption')
    for name, is_other, sort_order in DEFAULT_OPTIONS:
        MeetingPlaceOption.objects.get_or_create(
            name=name,
            defaults={'is_other': is_other, 'sort_order': sort_order},
        )


def unseed(apps, schema_editor):
    apps.get_model('clients', 'MeetingPlaceOption').objects.filter(
        name__in=[o[0] for o in DEFAULT_OPTIONS]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0037_add_meeting_place_option'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
