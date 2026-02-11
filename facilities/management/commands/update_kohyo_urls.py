"""取得済みの介護サービス情報公表システムURLをDBに反映するコマンド"""
from django.core.management.base import BaseCommand
from facilities.models import Facility

# 施設名 → URL のマッピング
KOHYO_URLS = {
    # 特別養護老人ホーム (29件)
    "特別養護老人ホーム ハートヒルかわげ": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_detail_024_kihon=true&JigyosyoCd=2472400221-00&ServiceCd=510",
    "特別養護老人ホーム 青松園": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_detail_024_kihon=true&JigyosyoCd=2470500451-00&ServiceCd=510",
    "特別養護老人ホーム 報徳園": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_detail_024_kihon=true&JigyosyoCd=2470500485-00&ServiceCd=510",
    "特別養護老人ホーム 慈宗院": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_detail_024_kihon=true&JigyosyoCd=2470500238-00&ServiceCd=510",
    "特別養護老人ホーム 津の街": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_detail_024_kihon=true&JigyosyoCd=2470504727-00&ServiceCd=510",
    "特別養護老人ホーム 豊野みかんの里": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_detail_024_kihon=true&JigyosyoCd=2470502044-00&ServiceCd=510",
    "特別養護老人ホーム 高田光寿園": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_detail_024_kihon=true&JigyosyoCd=2470500493-00&ServiceCd=510",
    "特別養護老人ホーム みえ愛の里": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_detail_024_kihon=true&JigyosyoCd=2470502648-00&ServiceCd=510",
    "特別養護老人ホーム フルハウス": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_detail_024_kihon=true&JigyosyoCd=2472500137-00&ServiceCd=510",
    "特別養護老人ホーム 第二フルハウス": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_detail_024_kihon=true&JigyosyoCd=2470503596-00&ServiceCd=510",
    "特別養護老人ホーム シルバーケア豊壽園": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_detail_024_kihon=true&JigyosyoCd=2470500477-00&ServiceCd=510",
    "特別養護老人ホーム グリーンヒル": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_detail_024_kihon=true&JigyosyoCd=2470505567-00&ServiceCd=510",
    "しおりの里 広域型特別養護老人ホーム": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_detail_024_kihon=true&JigyosyoCd=2470503604-00&ServiceCd=510",
    "特別養護老人ホーム 泉園": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_detail_024_kihon=true&JigyosyoCd=2470500469-00&ServiceCd=510",
    "特別養護老人ホーム ライフかざはや": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_detail_024_kihon=true&JigyosyoCd=2470502374-00&ServiceCd=510",
    "特別養護老人ホーム 榊原陽光苑": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_detail_024_kihon=true&JigyosyoCd=2470600160-00&ServiceCd=510",
    "特別養護老人ホーム ときの音色": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_detail_024_kihon=true&JigyosyoCd=2470506045-00&ServiceCd=510",
    "特別養護老人ホーム 美里ヒルズ": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_detail_024_kihon=true&JigyosyoCd=2472400445-00&ServiceCd=510",
    "特別養護老人ホーム げいのう達春園": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_detail_024_kihon=true&JigyosyoCd=2472400205-00&ServiceCd=510",
    "特別養護老人ホーム アガペホーム": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_detail_024_kihon=true&JigyosyoCd=2470504578-00&ServiceCd=510",
    "特別養護老人ホーム 安濃聖母の家": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_detail_024_kihon=true&JigyosyoCd=2470503935-00&ServiceCd=510",
    "特別養護老人ホーム カサデマドレ": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_detail_024_kihon=true&JigyosyoCd=2470505211-00&ServiceCd=510",
    "特別養護老人ホーム 明合乃里": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_detail_024_kihon=true&JigyosyoCd=2472400213-00&ServiceCd=510",
    "特別養護老人ホーム きずな": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_detail_024_kihon=true&JigyosyoCd=2470502036-00&ServiceCd=510",
    "特別養護老人ホーム 優美": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_detail_024_kihon=true&JigyosyoCd=2470504958-00&ServiceCd=510",
    "特別養護老人ホーム 千年希望の杜美杉": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_detail_024_kihon=true&JigyosyoCd=2470506516-00&ServiceCd=510",
    "特別養護老人ホーム フルハウス（地域密着型）": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_detail_026_kihon=true&JigyosyoCd=2490500267-00&ServiceCd=540",
    "しおりの里 特別養護老人ホーム": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_detail_026_kihon=true&JigyosyoCd=2490500010-00&ServiceCd=540",
    "特別養護老人ホーム 安濃津愛の里": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_detail_026_kihon=true&JigyosyoCd=2490500143-00&ServiceCd=540",
    # 介護老人保健施設 (13件)
    "医療法人緑の風介護老人保健施設 いこいの森": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_detail_027_kihon=true&JigyosyoCd=2452480029-00&ServiceCd=520",
    "津老人保健施設アルカディア": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_detail_027_kihon=true&JigyosyoCd=2450580028-00&ServiceCd=520",
    "介護老人保健施設 トマト": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_detail_027_kihon=true&JigyosyoCd=2450580010-00&ServiceCd=520",
    "地域総合ケアセンター津介護老人保健施設シルバーケア豊壽園": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_detail_027_kihon=true&JigyosyoCd=2450580036-00&ServiceCd=520",
    "萩の原 介護老人保健施設": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_detail_027_kani=true&JigyosyoCd=2450680034-00&ServiceCd=520",
    "芹の里 介護老人保健施設": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_detail_027_kani=true&JigyosyoCd=2450680018-00&ServiceCd=520",
    "介護老人保健施設 さくら苑": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_detail_027_kihon=true&JigyosyoCd=2450680059-00&ServiceCd=520",
    "介護老人保健施設 第二さくら苑": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_detail_028_kihon=true&JigyosyoCd=2450580051-00&ServiceCd=220",
    "医療法人府洲会介護老人保健施設 ロマン": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_detail_027_kani=true&JigyosyoCd=2452480011-00&ServiceCd=520",
    "介護老人保健施設 あのう": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_detail_028_kihon=true&JigyosyoCd=2452480037-00&ServiceCd=220",
    "介護老人保健施設 万葉の里": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_detail_027_kihon=true&JigyosyoCd=2452580034-00&ServiceCd=520",
    "介護老人保健施設 万葉の里（ユニット型）": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_detail_028_kihon=true&JigyosyoCd=2452580034-00&ServiceCd=220",
    "介護老人保健施設 つつじの里": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_detail_028_kani=true&JigyosyoCd=2450580044-00&ServiceCd=220",
    # 介護医療院 (3件)
    "倉本病院介護医療院": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_detail_034_kihon=true&JigyosyoCd=24B0500031-00&ServiceCd=550",
    "幸和病院介護医療院": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_detail_034_kihon=true&JigyosyoCd=24B0500015-00&ServiceCd=550",
    "第二岩崎病院介護医療院": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_detail_034_kani=true&JigyosyoCd=24B0500023-00&ServiceCd=550",
    # グループホーム (26件 - 4件見つからず)
    "医療法人緑の風 グループホーム くつろぎの家": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_detail_022_kani=true&JigyosyoCd=2472400262-00&ServiceCd=320",
    "高齢者グループホームあじさいの家": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_detail_022_kani=true&JigyosyoCd=2470501582-00&ServiceCd=320",
    "高齢者グループホーム水仙の家": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_detail_022_kihon=true&JigyosyoCd=2470500758-00&ServiceCd=320",
    "グループホームレモンの里": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_detail_022_kani=true&JigyosyoCd=2490500564-00&ServiceCd=320",
    "グループホームつくしんぼ一色": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_detail_022_kihon=true&JigyosyoCd=2470501608-00&ServiceCd=320",
    "グループホームとのむら": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_detail_022_kihon=true&JigyosyoCd=2470501541-00&ServiceCd=320",
    "おもいやり介護の会 グループホームつくしんぼ": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_detail_022_kihon=true&JigyosyoCd=2470500667-00&ServiceCd=320",
    "グループホームコロナ": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_detail_022_kani=true&JigyosyoCd=2470501509-00&ServiceCd=320",
    "グループホームフルハウス": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_detail_022_kani=true&JigyosyoCd=2472500137-00&ServiceCd=320",
    "グループホーム渚園": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_detail_022_kihon=true&JigyosyoCd=2470500675-00&ServiceCd=320",
    "グループホームなのはな": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_detail_022_kihon=true&JigyosyoCd=2470501574-00&ServiceCd=320",
    "グループホーム潮風": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_detail_022_kihon=true&JigyosyoCd=2470501418-00&ServiceCd=320",
    "グループホームたんぽぽ": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_detail_022_kihon=true&JigyosyoCd=2490500028-00&ServiceCd=320",
    "八幡園グループホーム": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_detail_022_kihon=true&JigyosyoCd=2470500782-00&ServiceCd=320",
    "グループホームおたっしゃ長屋": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_detail_022_kani=true&JigyosyoCd=2470501657-00&ServiceCd=320",
    "しおりの里グループホーム": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_detail_022_kihon=true&JigyosyoCd=2490500051-00&ServiceCd=320",
    "地域総合ケアセンター認知症対応型グループホームシルバーケア豊壽園": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_detail_022_kihon=true&JigyosyoCd=2470500188-00&ServiceCd=320",
    "グループホームにのみの家": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_detail_022_kihon=true&JigyosyoCd=2470600418-00&ServiceCd=320",
    "グループホームひまわり": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_detail_022_kihon=true&JigyosyoCd=2470600368-00&ServiceCd=320",
    "グループホームふるさと": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_detail_022_kihon=true&JigyosyoCd=2470600285-00&ServiceCd=320",
    "グループホーム琴葉はつらつ": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_detail_022_kihon=true&JigyosyoCd=2490500713-00&ServiceCd=320",
    "グループホームなごみ苑": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_detail_022_kihon=true&JigyosyoCd=2490500184-00&ServiceCd=320",
    "グループホーム青い鳥": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_detail_022_kihon=true&JigyosyoCd=2470501640-00&ServiceCd=320",
    "シルバータウンあのうグループホーム": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_detail_022_kihon=true&JigyosyoCd=2472400361-00&ServiceCd=320",
    "愛の家グループホーム一志": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_detail_022_kihon=true&JigyosyoCd=2490500135-00&ServiceCd=320",
    "グループホーム白山": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_detail_022_kani=true&JigyosyoCd=2470501939-00&ServiceCd=320",
    # 有料老人ホーム (15件 - 残りは未取得)
    "サンヒルズガーデン": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_pref_seikatu_detail_920_detail=true&FacilityId=50370&CityCd=242012&ServiceCd=920",
    "昭和ろまん": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_detail_010_kihon=true&JigyosyoCd=2472400411-00&ServiceCd=331",
    "わが家": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_detail_010_kihon=true&JigyosyoCd=2470502416-00&ServiceCd=331",
    "わが家千里": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_pref_seikatu_detail_920_detail=true&FacilityId=64696&CityCd=242012&ServiceCd=920&SearchType=nursinghome",
    "ハーモニーハウス津": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_pref_seikatu_detail_920_detail=true&FacilityId=48821&CityCd=242012&ServiceCd=920&SearchType=nursinghome",
    "陽だまりの丘片田": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_pref_seikatu_detail_920_detail=true&FacilityId=65978&CityCd=242012&ServiceCd=920&SearchType=nursinghome",
    "有料老人ホーム 大ちゃん": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_pref_seikatu_detail_920_detail=true&FacilityId=49048&CityCd=242012&ServiceCd=920&SearchType=nursinghome",
    "有料老人ホーム 安心戸木": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_pref_seikatu_detail_920_detail=true&FacilityId=48822&CityCd=242012&ServiceCd=920&SearchType=nursinghome",
    "特定施設入居者生活介護虹の夢 津": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_detail_010_kihon=true&JigyosyoCd=2470504941-00&ServiceCd=331",
    "ケアポート津高茶屋": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_pref_seikatu_detail_920_detail=true&FacilityId=49582&CityCd=242012&ServiceCd=920&SearchType=nursinghome",
    "住宅型有料老人ホーム ケアスイート藤方": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_detail_2018_001_kihon=true&JigyosyoCd=2470505047-00&PrefCd=24&VersionCd=001",
    "あけぼの荘": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_pref_seikatu_detail_920_detail=true&FacilityId=64701&CityCd=242012&ServiceCd=920&SearchType=nursinghome",
    "有料老人ホーム レモンの里": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_pref_seikatu_detail_920_detail=true&FacilityId=111421&CityCd=242012&ServiceCd=920&SearchType=nursinghome",
    "有料老人ホーム ゆりの里": "https://www.kaigokensaku.mhlw.go.jp/24/index.php?action_kouhyou_pref_seikatu_detail_920_detail=true&FacilityId=111194&CityCd=242047&ServiceCd=920&SearchType=nursinghome",
}


class Command(BaseCommand):
    help = "取得済みの介護サービス情報公表システムURLをDBに反映します"

    def handle(self, *args, **options):
        updated = 0
        not_found = 0
        for name, url in KOHYO_URLS.items():
            try:
                facility = Facility.objects.get(name=name)
                facility.kaigo_kohyo_url = url
                facility.save(update_fields=["kaigo_kohyo_url"])
                updated += 1
            except Facility.DoesNotExist:
                not_found += 1
                self.stdout.write(self.style.WARNING(f"DB未登録: {name}"))
            except Facility.MultipleObjectsReturned:
                facility = Facility.objects.filter(name=name).first()
                facility.kaigo_kohyo_url = url
                facility.save(update_fields=["kaigo_kohyo_url"])
                updated += 1

        total = Facility.objects.exclude(kaigo_kohyo_url="").count()
        remaining = Facility.objects.filter(kaigo_kohyo_url="").count()
        self.stdout.write(self.style.SUCCESS(
            f"完了: {updated} 件URL登録 (DB未登録: {not_found}件)\n"
            f"URL登録済: {total}件 / 未登録: {remaining}件"
        ))
