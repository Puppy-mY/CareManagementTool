from django.db import migrations

INITIAL_SERVICES = [
    {
        'order': 1, 'item_key': 'ms', 'name': '食事支援',
        'price_type': 'per_day', 'price': 165, 'extra_prices': [],
        'notes': 'お部屋への声掛け・食堂までのご誘導・配膳・下膳・食器の配置の変更\n※介護サービスで食事介助を受ける場合は不要',
        'is_visible': True,
    },
    {
        'order': 2, 'item_key': 'linen', 'name': 'リネンリース',
        'price_type': 'per_day', 'price': 165, 'extra_prices': [],
        'notes': '掛け布団・ベッドパッド・枕・シーツをリース（週1回交換）。持ち込みの場合、汚れ時の交換はご本人・ご家族様での対応となります。',
        'is_visible': True,
    },
    {
        'order': 3, 'item_key': 'excretion', 'name': '排泄支援',
        'price_type': 'multi', 'price': 0,
        'extra_prices': [
            {'label': '1回/日（深夜帯のみ）', 'value': 275},
            {'label': '2回/日（深夜帯・早朝帯）', 'value': 440},
            {'label': '4回/日（深夜・早朝・午前・午後）', 'value': 715},
        ],
        'notes': '介護保険サービス外の自費の排泄支援。毎日の排泄でお手伝いが必要な場合は、介護保険サービスだけでは賄いきれないため、有償の排泄支援が必要。',
        'is_visible': True,
    },
    {
        'order': 4, 'item_key': 'mince', 'name': '刻み・ペースト食',
        'price_type': 'per_meal', 'price': 44, 'extra_prices': [],
        'notes': '食事の形態を一口大・キザミ・ペーストへ変更します。\n※お粥への変更は無料',
        'is_visible': True,
    },
    {
        'order': 5, 'item_key': 'therapy', 'name': '療養食',
        'price_type': 'per_meal', 'price': 77, 'extra_prices': [],
        'notes': '医師の指示に基づく特別食を提供します（糖尿病食・心臓食・腎食・胃潰瘍食・貧血食など）。',
        'is_visible': True,
    },
    {
        'order': 6, 'item_key': 'sputum', 'name': '喀痰吸引',
        'price_type': 'multi', 'price': 0,
        'extra_prices': [
            {'label': '1回/日（深夜帯）', 'value': 275},
            {'label': '2回/日（深夜帯・早朝帯）', 'value': 440},
            {'label': '4回/日（深夜・早朝・午前・午後）', 'value': 715},
        ],
        'notes': '介護保険サービス外の自費の喀痰吸引。毎日の喀痰吸引が必要な場合は、介護保険サービスだけでは賄いきれないため、有償の喀痰吸引が必要。',
        'is_visible': True,
    },
    {
        'order': 7, 'item_key': 'parking', 'name': '駐車場代',
        'price_type': 'per_month', 'price': 3300, 'extra_prices': [],
        'notes': '',
        'is_visible': True,
    },
    {
        'order': 8, 'item_key': 'cleaning', 'name': '居室内清掃',
        'price_type': 'per_month', 'price': 550, 'extra_prices': [],
        'notes': 'クリーンスタッフによる居室清掃。介護保険サービスで居室清掃も可能です。',
        'is_visible': True,
    },
    {
        'order': 9, 'item_key': 'laundry', 'name': '衣類洗濯',
        'price_type': 'multi', 'price': 0, 'extra_prices': [],
        'notes': '衣類・タオル類のお洗濯代行。料金・回数など詳細は施設スタッフにご確認ください。',
        'is_visible': True,
    },
    {
        'order': 10, 'item_key': 'bed', 'name': 'ベッドリース',
        'price_type': 'per_month', 'price': 3300, 'extra_prices': [],
        'notes': '介護用ベッドのリース。自前でご用意いただく場合は不要です。',
        'is_visible': True,
    },
]


def seed_paid_services(apps, schema_editor):
    PaidService = apps.get_model('clients', 'PaidService')
    for svc in INITIAL_SERVICES:
        PaidService.objects.get_or_create(
            item_key=svc['item_key'],
            defaults=svc,
        )


def unseed_paid_services(apps, schema_editor):
    PaidService = apps.get_model('clients', 'PaidService')
    PaidService.objects.filter(item_key__in=[s['item_key'] for s in INITIAL_SERVICES]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0051_add_paid_service'),
    ]

    operations = [
        migrations.RunPython(seed_paid_services, unseed_paid_services),
    ]
