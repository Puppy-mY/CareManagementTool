from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("clients", "0025_add_ltc_reissue_application_document_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="documentcreationhistory",
            name="document_type",
            field=models.CharField(
                choices=[
                    ("kyotaku_service_plan_request", "居宅サービス計画作成依頼書"),
                    ("kyotaku_preventive_service_plan_request", "介護予防サービス計画作成依頼書"),
                    ("ltc_renewal", "更新認定申請書"),
                    ("ltc_change", "区分変更申請書"),
                    ("ltc_withdrawal", "認定申請取下書"),
                    ("ltc_doctor_change", "認定申請主治医変更届出書"),
                    ("ltc_address_change", "介護保険被保険者証送付先変更届"),
                    ("ltc_burden_address_change", "介護保険負担限度額・割合証送付先変更届"),
                    ("ltc_reissue_application", "介護保険関係・再交付申請書"),
                    ("kyotaku_selection_confirmation", "居宅サービス事業所の選択に関する説明に係る確認書"),
                    ("careplan_info_request", "介護サービス計画作成に係る資料提供申請書"),
                    ("care_plan", "ケアプラン"),
                    ("assessment", "アセスメント"),
                    ("other", "その他"),
                ],
                max_length=50,
                verbose_name="書類種別",
            ),
        ),
    ]
