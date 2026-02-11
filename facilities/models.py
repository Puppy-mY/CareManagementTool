from django.db import models


class Facility(models.Model):
    FACILITY_TYPE_CHOICES = [
        ("特別養護老人ホーム", "特別養護老人ホーム"),
        ("養護老人ホーム", "養護老人ホーム"),
        ("軽費老人ホーム", "軽費老人ホーム"),
        ("有料老人ホーム", "有料老人ホーム"),
        ("サービス付き高齢者向け住宅", "サービス付き高齢者向け住宅"),
        ("介護老人保健施設", "介護老人保健施設"),
        ("介護医療院", "介護医療院"),
        ("グループホーム", "グループホーム"),
        ("その他", "その他"),
    ]

    REGION_CHOICES = [
        ("津市", "津市"),
        ("四日市市", "四日市市"),
        ("伊勢市", "伊勢市"),
        ("松阪市", "松阪市"),
        ("桑名市", "桑名市"),
        ("鈴鹿市", "鈴鹿市"),
        ("名張市", "名張市"),
        ("尾鷲市", "尾鷲市"),
        ("亀山市", "亀山市"),
        ("鳥羽市", "鳥羽市"),
        ("熊野市", "熊野市"),
        ("いなべ市", "いなべ市"),
        ("志摩市", "志摩市"),
        ("伊賀市", "伊賀市"),
        ("桑名郡木曽岬町", "桑名郡木曽岬町"),
        ("員弁郡東員町", "員弁郡東員町"),
        ("三重郡菰野町", "三重郡菰野町"),
        ("三重郡朝日町", "三重郡朝日町"),
        ("三重郡川越町", "三重郡川越町"),
        ("多気郡多気町", "多気郡多気町"),
        ("多気郡明和町", "多気郡明和町"),
        ("多気郡大台町", "多気郡大台町"),
        ("度会郡玉城町", "度会郡玉城町"),
        ("度会郡度会町", "度会郡度会町"),
        ("度会郡大紀町", "度会郡大紀町"),
        ("度会郡南伊勢町", "度会郡南伊勢町"),
        ("北牟婁郡紀北町", "北牟婁郡紀北町"),
        ("南牟婁郡御浜町", "南牟婁郡御浜町"),
        ("南牟婁郡紀宝町", "南牟婁郡紀宝町"),
        ("その他", "その他"),
    ]

    facility_type = models.CharField(
        "施設種別", max_length=50, choices=FACILITY_TYPE_CHOICES,
        default="特別養護老人ホーム",
    )
    name = models.CharField("施設名", max_length=200)
    region = models.CharField("地域", max_length=50, choices=REGION_CHOICES)
    address = models.CharField("住所", max_length=300, blank=True)
    phone = models.CharField("電話番号", max_length=20, blank=True)
    town = models.CharField("町名", max_length=100, blank=True)
    fax = models.CharField("FAX番号", max_length=20, blank=True)
    homepage_url = models.URLField("ホームページURL", max_length=500, blank=True)
    kaigo_kohyo_url = models.URLField("介護サービス情報公表システムURL", max_length=500, blank=True)
    unit_private = models.BooleanField("ユニット型個室", default=False)
    unit_multi = models.BooleanField("ユニット型多床室", default=False)
    traditional_private = models.BooleanField("従来型個室", default=False)
    traditional_multi = models.BooleanField("多床室", default=False)
    capacity = models.IntegerField("定員数", null=True, blank=True)
    is_community_based = models.BooleanField("地域密着型", default=False)
    is_wide_area = models.BooleanField("広域型", default=False)
    is_tokutei_shisetsu = models.BooleanField("特定施設入居者生活介護指定あり", default=False)
    is_zaitaku_kyoka = models.BooleanField("在宅強化型", default=False)
    is_keihi_a = models.BooleanField("A型", default=False)
    is_keihi_b = models.BooleanField("B型", default=False)
    is_keihi_carehouse = models.BooleanField("ケアハウス", default=False)
    notes = models.TextField("備考", blank=True)
    created_at = models.DateTimeField("登録日", auto_now_add=True)
    updated_at = models.DateTimeField("更新日", auto_now=True)

    class Meta:
        verbose_name = "施設"
        verbose_name_plural = "施設"
        ordering = ["region", "name"]

    def __str__(self):
        return self.name

    def room_types_display(self):
        """部屋タイプの表示用リストを返す"""
        types = []
        if self.unit_private:
            types.append("ユニット型個室")
        if self.unit_multi:
            types.append("ユニット型多床室")
        if self.traditional_private:
            types.append("従来型個室")
        if self.traditional_multi:
            types.append("多床室")
        return types
