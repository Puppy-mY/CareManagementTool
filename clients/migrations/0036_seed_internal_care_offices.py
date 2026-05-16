from django.db import migrations


INTERNAL_OFFICES = [
    {
        'name':         '訪問看護ステーション安濃津ろまん',
        'furigana':     'ホウモンカンゴステーションアノツロマン',
        'service_type': '訪問看護',
        'phone':        '059-213-4165',
        'fax':          '059-213-4160',
        'persons':      [],
    },
    {
        'name':         'ヘルパーステーション安濃津ろまん',
        'furigana':     'ヘルパーステーションアノツロマン',
        'service_type': '訪問介護',
        'phone':        '059-213-4165',
        'fax':          '059-213-4160',
        'persons':      [],
    },
    {
        'name':         'デイサービス安濃津ろまん',
        'furigana':     'デイサービスアノツロマン',
        'service_type': '通所介護',
        'phone':        '059-213-4165',
        'fax':          '059-213-4160',
        'persons':      [],
    },
    {
        'name':         '福祉用具貸与・販売　安濃津ろまん',
        'furigana':     'フクシヨウグタイヨ・ハンバイ　アノツロマン',
        'service_type': '福祉用具貸与',
        'phone':        '059-213-4165',
        'fax':          '059-213-4160',
        'persons':      [],
    },
    {
        'name':         'ローレル薬局',
        'furigana':     'ローレルヤッキョク',
        'service_type': 'その他',
        'phone':        '059-253-7799',
        'fax':          '059-253-7799',
        'persons':      ['中野先生'],
    },
    {
        'name':         '介護老人保健施設ロマン',
        'furigana':     'カイゴロウジンホケンシセツロマン',
        'service_type': '訪問リハビリテーション',
        'phone':        '059-265-6500',
        'fax':          '059-265-6511',
        'persons':      [],
    },
    {
        'name':         '在宅複合型施設　花紬',
        'furigana':     'ザイタクフクゴウガタシセツ　ハナツムギ',
        'service_type': '訪問介護',
        'phone':        '059-265-6600',
        'fax':          '059-266-1020',
        'persons':      [],
    },
]


def seed_internal_offices(apps, schema_editor):
    CareServiceOffice = apps.get_model('clients', 'CareServiceOffice')
    for data in INTERNAL_OFFICES:
        CareServiceOffice.objects.get_or_create(
            name=data['name'],
            office_type='internal',
            defaults={
                'furigana':     data['furigana'],
                'service_type': data['service_type'],
                'phone':        data['phone'],
                'fax':          data['fax'],
                'persons':      data['persons'],
            },
        )


def unseed_internal_offices(apps, schema_editor):
    CareServiceOffice = apps.get_model('clients', 'CareServiceOffice')
    CareServiceOffice.objects.filter(
        office_type='internal',
        name__in=[d['name'] for d in INTERNAL_OFFICES],
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0035_add_office_type_to_care_service_office'),
    ]

    operations = [
        migrations.RunPython(seed_internal_offices, unseed_internal_offices),
    ]
