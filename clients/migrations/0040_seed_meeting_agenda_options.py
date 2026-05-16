from django.db import migrations

DEFAULT_OPTIONS = [
    ('安濃津ろまん入居に伴う、介護サービスの検討及び事業所契約', False, 1),
    ('現在の生活状況やサービス利用状況、今後の生活について',     False, 2),
    ('その他',                                                  True,  99),
]


def seed(apps, schema_editor):
    MeetingAgendaOption = apps.get_model('clients', 'MeetingAgendaOption')
    for name, is_other, sort_order in DEFAULT_OPTIONS:
        MeetingAgendaOption.objects.get_or_create(
            name=name,
            defaults={'is_other': is_other, 'sort_order': sort_order},
        )


def unseed(apps, schema_editor):
    apps.get_model('clients', 'MeetingAgendaOption').objects.filter(
        name__in=[o[0] for o in DEFAULT_OPTIONS]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0039_add_meeting_agenda_option'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
