import re

from django.core.management.base import BaseCommand
from facilities.models import Facility


def parse_town(address):
    """住所から町名を抽出する（津市以降、最初の「町」「村」まで）"""
    if not address:
        return ""
    # 「津市」を除去
    addr = re.sub(r'^(三重県)?津市', '', address)
    # 最初の「町」「村」までを抽出
    m = re.match(r'^([^町村]+(?:町|村))', addr)
    if m:
        return m.group(1)
    # 丁目の場合は漢数字+丁目を除去
    m = re.match(r'^(.+?)[一二三四五六七八九十\d]+丁目', addr)
    if m:
        return m.group(1)
    # 町・村がない場合、数字の手前までを町名とする
    m = re.match(r'^([^\d]+)', addr)
    if m:
        return m.group(1)
    return ""


FACILITIES_DATA = [
    # 特別養護老人ホーム (29)
    {"facility_type": "特別養護老人ホーム", "name": "特別養護老人ホーム ハートヒルかわげ", "capacity": 60, "address": "津市河芸町浜田860番地", "phone": "059-245-7800", "region": "津市"},
    {"facility_type": "特別養護老人ホーム", "name": "特別養護老人ホーム 青松園", "capacity": 50, "address": "津市高洲町15番43号", "phone": "059-228-2661", "region": "津市"},
    {"facility_type": "特別養護老人ホーム", "name": "特別養護老人ホーム 報徳園", "capacity": 110, "address": "津市河辺町1317番地1", "phone": "059-228-1951", "region": "津市"},
    {"facility_type": "特別養護老人ホーム", "name": "特別養護老人ホーム 慈宗院", "capacity": 110, "address": "津市片田長谷町167番地1", "phone": "059-237-0069", "region": "津市"},
    {"facility_type": "特別養護老人ホーム", "name": "特別養護老人ホーム 津の街", "capacity": 80, "address": "津市一身田平野726番地6", "phone": "059-271-6186", "region": "津市"},
    {"facility_type": "特別養護老人ホーム", "name": "特別養護老人ホーム 豊野みかんの里", "capacity": 80, "address": "津市一身田豊野1659番地", "phone": "059-236-5610", "region": "津市"},
    {"facility_type": "特別養護老人ホーム", "name": "特別養護老人ホーム 高田光寿園", "capacity": 100, "address": "津市大里野田町1124番地1", "phone": "059-230-7811", "region": "津市"},
    {"facility_type": "特別養護老人ホーム", "name": "特別養護老人ホーム みえ愛の里", "capacity": 30, "address": "津市雲出本郷町2128番地", "phone": "059-234-1500", "region": "津市"},
    {"facility_type": "特別養護老人ホーム", "name": "特別養護老人ホーム フルハウス", "capacity": 30, "address": "津市香良洲町1990番地", "phone": "059-292-4888", "region": "津市"},
    {"facility_type": "特別養護老人ホーム", "name": "特別養護老人ホーム 第二フルハウス", "capacity": 50, "address": "津市香良洲町3952番地1", "phone": "059-292-2890", "region": "津市"},
    {"facility_type": "特別養護老人ホーム", "name": "特別養護老人ホーム シルバーケア豊壽園", "capacity": 70, "address": "津市高茶屋小森町4152番地", "phone": "059-235-2102", "region": "津市"},
    {"facility_type": "特別養護老人ホーム", "name": "特別養護老人ホーム グリーンヒル", "capacity": 60, "address": "津市緑が丘一丁目1番地2", "phone": "059-269-5555", "region": "津市"},
    {"facility_type": "特別養護老人ホーム", "name": "しおりの里 広域型特別養護老人ホーム", "capacity": 50, "address": "津市野田2035番地2", "phone": "059-239-1326", "region": "津市"},
    {"facility_type": "特別養護老人ホーム", "name": "特別養護老人ホーム 泉園", "capacity": 80, "address": "津市野田2059番地", "phone": "059-237-2526", "region": "津市"},
    {"facility_type": "特別養護老人ホーム", "name": "特別養護老人ホーム ライフかざはや", "capacity": 60, "address": "津市戸木町4169番地4", "phone": "059-254-6610", "region": "津市"},
    {"facility_type": "特別養護老人ホーム", "name": "特別養護老人ホーム 榊原陽光苑", "capacity": 50, "address": "津市榊原町5684番地", "phone": "059-252-2650", "region": "津市"},
    {"facility_type": "特別養護老人ホーム", "name": "特別養護老人ホーム ときの音色", "capacity": 60, "address": "津市中村町745番地25", "phone": "059-252-8020", "region": "津市"},
    {"facility_type": "特別養護老人ホーム", "name": "特別養護老人ホーム 美里ヒルズ", "capacity": 60, "address": "津市美里町三郷430番地", "phone": "059-279-5100", "region": "津市"},
    {"facility_type": "特別養護老人ホーム", "name": "特別養護老人ホーム げいのう達春園", "capacity": 50, "address": "津市芸濃町椋本5310番地1", "phone": "059-265-5500", "region": "津市"},
    {"facility_type": "特別養護老人ホーム", "name": "特別養護老人ホーム アガペホーム", "capacity": 60, "address": "津市豊が丘五丁目47番8号", "phone": "059-253-6517", "region": "津市"},
    {"facility_type": "特別養護老人ホーム", "name": "特別養護老人ホーム 安濃聖母の家", "capacity": 50, "address": "津市安濃町今徳81番地2", "phone": "059-267-0281", "region": "津市"},
    {"facility_type": "特別養護老人ホーム", "name": "特別養護老人ホーム カサデマドレ", "capacity": 60, "address": "津市安濃町戸島569番地3", "phone": "059-271-5611", "region": "津市"},
    {"facility_type": "特別養護老人ホーム", "name": "特別養護老人ホーム 明合乃里", "capacity": 50, "address": "津市安濃町田端上野970番地3", "phone": "059-268-3333", "region": "津市"},
    {"facility_type": "特別養護老人ホーム", "name": "特別養護老人ホーム きずな", "capacity": 50, "address": "津市白山町二本木1163番地", "phone": "059-264-0222", "region": "津市"},
    {"facility_type": "特別養護老人ホーム", "name": "特別養護老人ホーム 優美", "capacity": 60, "address": "津市白山町二本木4009番地3", "phone": "059-264-0505", "region": "津市"},
    {"facility_type": "特別養護老人ホーム", "name": "特別養護老人ホーム 千年希望の杜美杉", "capacity": 62, "address": "津市美杉町八知729番地1", "phone": "059-272-8800", "region": "津市"},
    # 地域密着型特養 (3)
    {"facility_type": "特別養護老人ホーム", "name": "特別養護老人ホーム フルハウス（地域密着型）", "capacity": 10, "address": "津市香良洲町1990番地", "phone": "059-292-4888", "region": "津市", "notes": "地域密着型"},
    {"facility_type": "特別養護老人ホーム", "name": "しおりの里 特別養護老人ホーム", "capacity": 20, "address": "津市野田2035番地2", "phone": "059-239-1312", "region": "津市", "notes": "地域密着型"},
    {"facility_type": "特別養護老人ホーム", "name": "特別養護老人ホーム 安濃津愛の里", "capacity": 29, "address": "津市安濃町妙法寺727番地", "phone": "059-267-1000", "region": "津市", "notes": "地域密着型"},
    # 養護老人ホーム (2)
    {"facility_type": "養護老人ホーム", "name": "高田慈光院", "capacity": 100, "address": "津市大里野田町1124番地1", "phone": "059-230-7811", "region": "津市"},
    {"facility_type": "養護老人ホーム", "name": "青松園", "capacity": 60, "address": "津市高洲町15番43号", "phone": "059-228-2661", "region": "津市"},
    # 軽費老人ホーム (8)
    {"facility_type": "軽費老人ホーム", "name": "安濃聖母の家", "capacity": 50, "address": "津市安濃町妙法寺892番地", "phone": "059-268-2000", "region": "津市"},
    {"facility_type": "軽費老人ホーム", "name": "ベタニヤハウス", "capacity": 50, "address": "津市豊が丘五丁目47番6号", "phone": "059-230-2500", "region": "津市"},
    {"facility_type": "軽費老人ホーム", "name": "高田ケアハウス", "capacity": 36, "address": "津市一身田町261番地2", "phone": "059-233-5151", "region": "津市", "notes": "介護保険の特定施設入居者生活介護の指定あり"},
    {"facility_type": "軽費老人ホーム", "name": "ケアハウスシルバーケア豊壽園", "capacity": 30, "address": "津市高茶屋小森上野町737番地", "phone": "059-235-5500", "region": "津市", "notes": "介護保険の特定施設入居者生活介護の指定あり"},
    {"facility_type": "軽費老人ホーム", "name": "かざはや苑", "capacity": 50, "address": "津市戸木町4170番地2", "phone": "059-254-4600", "region": "津市", "notes": "介護保険の特定施設入居者生活介護の指定あり"},
    {"facility_type": "軽費老人ホーム", "name": "グリーンヒルかわげ", "capacity": 30, "address": "津市河芸町浜田860番地", "phone": "059-245-7826", "region": "津市"},
    {"facility_type": "軽費老人ホーム", "name": "花紬", "capacity": 30, "address": "津市芸濃町椋本3805番地2", "phone": "059-265-6600", "region": "津市"},
    {"facility_type": "軽費老人ホーム", "name": "ケアハウスしおりの里", "capacity": 54, "address": "津市野田2033番地1", "phone": "059-239-1316", "region": "津市", "notes": "介護保険の特定施設入居者生活介護の指定あり"},
    # 有料老人ホーム
    {"facility_type": "有料老人ホーム", "name": "サンヒルズガーデン", "capacity": 50, "address": "津市一身田上津部田1424番地", "phone": "059-221-4165", "region": "津市"},
    {"facility_type": "有料老人ホーム", "name": "昭和ろまん", "capacity": 70, "address": "津市芸濃町椋本6177番地1", "phone": "059-265-6510", "region": "津市", "notes": "介護保険の特定施設入居者生活介護の指定あり"},
    {"facility_type": "有料老人ホーム", "name": "わが家", "capacity": 30, "address": "津市河芸町上野1902番地", "phone": "059-244-1122", "region": "津市"},
    {"facility_type": "有料老人ホーム", "name": "わが家千里", "capacity": 18, "address": "津市河芸町東千里3887番地1", "phone": "059-271-6620", "region": "津市"},
    {"facility_type": "有料老人ホーム", "name": "ハーモニーハウス津", "capacity": 35, "address": "津市久居明神町2077番地", "phone": "059-254-1122", "region": "津市"},
    {"facility_type": "有料老人ホーム", "name": "陽だまりの丘片田", "capacity": 27, "address": "津市片田井戸町堂坂268番地", "phone": "059-239-0555", "region": "津市"},
    {"facility_type": "有料老人ホーム", "name": "花泉", "capacity": 13, "address": "津市一志町其倉287番地1", "phone": "059-293-3163", "region": "津市"},
    {"facility_type": "有料老人ホーム", "name": "有料老人ホーム 大ちゃん", "capacity": 24, "address": "津市一志町片野223番地2", "phone": "059-295-0026", "region": "津市"},
    {"facility_type": "有料老人ホーム", "name": "住宅型有料老人ホーム いちしの里3", "capacity": 26, "address": "津市一志町日置46番地", "phone": "059-295-0055", "region": "津市"},
    {"facility_type": "有料老人ホーム", "name": "有料老人ホーム 安心戸木", "capacity": 18, "address": "津市戸木町7054番地2", "phone": "059-273-5336", "region": "津市"},
    {"facility_type": "有料老人ホーム", "name": "特定施設入居者生活介護虹の夢 津", "capacity": 60, "address": "津市観音寺町152番地", "phone": "059-225-5001", "region": "津市", "notes": "介護保険の特定施設入居者生活介護の指定あり"},
    {"facility_type": "有料老人ホーム", "name": "ケアポート津高茶屋", "capacity": 150, "address": "津市高茶屋六丁目10番14号", "phone": "059-234-1175", "region": "津市"},
    {"facility_type": "有料老人ホーム", "name": "住宅型有料老人ホーム ヴィーゲ", "capacity": 25, "address": "津市白山町川口3141番地", "phone": "059-264-0056", "region": "津市"},
    {"facility_type": "有料老人ホーム", "name": "住宅型有料老人ホーム ケアスイート藤方", "capacity": 19, "address": "津市藤方1660番地1", "phone": "059-253-7950", "region": "津市"},
    {"facility_type": "有料老人ホーム", "name": "あけぼの荘", "capacity": 12, "address": "津市大園町24番6号", "phone": "059-253-8633", "region": "津市"},
    {"facility_type": "有料老人ホーム", "name": "有料老人ホーム 優喜", "capacity": 8, "address": "津市藤方2255番地3", "phone": "059-253-6547", "region": "津市"},
    {"facility_type": "有料老人ホーム", "name": "有料老人ホーム レモンの里", "capacity": 13, "address": "津市神納417番地", "phone": "059-229-8433", "region": "津市"},
    {"facility_type": "有料老人ホーム", "name": "宅老所 津のうち", "capacity": 7, "address": "津市渋見町554番地18", "phone": "059-225-2574", "region": "津市"},
    {"facility_type": "有料老人ホーム", "name": "やすらぎの家", "capacity": 6, "address": "津市美里町南長野1007番地2", "phone": "059-279-3441", "region": "津市"},
    {"facility_type": "有料老人ホーム", "name": "高齢者専用住宅カトレア", "capacity": 9, "address": "津市垂水2990番地39", "phone": "059-222-0553", "region": "津市"},
    {"facility_type": "有料老人ホーム", "name": "金と銀", "capacity": 12, "address": "津市津興35番地", "phone": "059-229-7240", "region": "津市"},
    {"facility_type": "有料老人ホーム", "name": "有料老人ホーム ゆりの里", "capacity": 34, "address": "津市柳山津興3307番地", "phone": "059-221-2400", "region": "津市"},
    {"facility_type": "有料老人ホーム", "name": "有料老人ホーム 安心", "capacity": 27, "address": "津市下弁財町津興3032番地", "phone": "059-227-0839", "region": "津市"},
    {"facility_type": "有料老人ホーム", "name": "有料老人ホーム 結の里", "capacity": 14, "address": "津市白山町二本木3897番地1", "phone": "059-264-0500", "region": "津市"},
    {"facility_type": "有料老人ホーム", "name": "生活支援サービス付住宅 山の手サザンコート", "capacity": 10, "address": "津市鳥居町167番地10、11", "phone": "059-227-3533", "region": "津市"},
    {"facility_type": "有料老人ホーム", "name": "住宅型有料老人ホーム 虹 A棟", "capacity": 18, "address": "津市末広町1039番地1", "phone": "059-246-5252", "region": "津市"},
    {"facility_type": "有料老人ホーム", "name": "住宅型有料老人ホーム 虹 B棟", "capacity": 14, "address": "津市末広町1040番地2", "phone": "059-246-5252", "region": "津市"},
    {"facility_type": "有料老人ホーム", "name": "住宅型有料老人ホーム 虹 C棟", "capacity": 8, "address": "津市末広町1039番地2", "phone": "059-246-5252", "region": "津市"},
    {"facility_type": "有料老人ホーム", "name": "住宅型有料老人ホーム 虹 D棟", "capacity": 15, "address": "津市末広町1040番地1", "phone": "059-246-5252", "region": "津市"},
    {"facility_type": "有料老人ホーム", "name": "有料老人ホーム グリーンヒル", "capacity": 80, "address": "津市緑が丘一丁目1番地1", "phone": "059-239-1165", "region": "津市"},
    {"facility_type": "有料老人ホーム", "name": "有料老人ホーム「のぞみ」の家", "capacity": 12, "address": "津市白山町三ケ野1260番地1", "phone": "059-261-6625", "region": "津市"},
    {"facility_type": "有料老人ホーム", "name": "住宅型有料老人ホーム 太陽", "capacity": 30, "address": "津市白塚町2216番地", "phone": "059-236-5300", "region": "津市"},
    {"facility_type": "有料老人ホーム", "name": "有料老人ホーム ここよ本店", "capacity": 19, "address": "津市垂水522番地1", "phone": "059-246-5541", "region": "津市"},
    {"facility_type": "有料老人ホーム", "name": "ハーモニーハウス津・大園", "capacity": 29, "address": "津市大園町5番45号", "phone": "059-253-1122", "region": "津市"},
    {"facility_type": "有料老人ホーム", "name": "Sunhills Garden・Annex31", "capacity": 62, "address": "津市一身田上津部田1424番地", "phone": "059-221-4165", "region": "津市"},
    {"facility_type": "有料老人ホーム", "name": "フラワーロード栄", "capacity": 30, "address": "津市栄町四丁目185番地", "phone": "059-222-2119", "region": "津市"},
    {"facility_type": "有料老人ホーム", "name": "有料老人ホーム 安心庄田", "capacity": 36, "address": "津市庄田町3561番地1", "phone": "059-253-7110", "region": "津市"},
    {"facility_type": "有料老人ホーム", "name": "ナーシングホームスウィートナース津", "capacity": 20, "address": "津市中河原西興2051番地", "phone": "059-224-1190", "region": "津市"},
    {"facility_type": "有料老人ホーム", "name": "有料老人ホーム Here", "capacity": 7, "address": "津市垂水522番地6", "phone": "059-253-2488", "region": "津市"},
    {"facility_type": "有料老人ホーム", "name": "シンフォニー高茶屋", "capacity": 35, "address": "津市高茶屋小森町1527番地", "phone": "059-253-4371", "region": "津市"},
    {"facility_type": "有料老人ホーム", "name": "ひまわり会館高田", "capacity": 32, "address": "津市栗真中山町202番地", "phone": "059-231-7170", "region": "津市"},
    {"facility_type": "有料老人ホーム", "name": "からふる庭園芸濃", "capacity": 30, "address": "津市芸濃町楠原107番地1", "phone": "059-265-2771", "region": "津市"},
    {"facility_type": "有料老人ホーム", "name": "シニアハウスなないろ", "capacity": 36, "address": "津市末広町994番地", "phone": "059-253-1265", "region": "津市"},
    {"facility_type": "有料老人ホーム", "name": "有料老人ホームさくら", "capacity": 45, "address": "津市殿村860番地2", "phone": "059-273-5531", "region": "津市"},
    # サービス付き高齢者向け住宅
    {"facility_type": "サービス付き高齢者向け住宅", "name": "サービス付き高齢者向け住宅 安濃津ろまん", "capacity": 230, "address": "津市神戸154番地9", "phone": "059-213-4165", "region": "津市"},
    {"facility_type": "サービス付き高齢者向け住宅", "name": "大園荘", "capacity": 49, "address": "津市大園町4番29号", "phone": "059-222-8686", "region": "津市"},
    {"facility_type": "サービス付き高齢者向け住宅", "name": "高齢者介護ホーム ナゴミガーデン", "capacity": 12, "address": "津市一志町片野367番地1", "phone": "059-293-0753", "region": "津市"},
    {"facility_type": "サービス付き高齢者向け住宅", "name": "ルミナスビレッジ曽根", "capacity": 40, "address": "津市安濃町曽根833番地6", "phone": "059-239-1000", "region": "津市"},
    {"facility_type": "サービス付き高齢者向け住宅", "name": "いちしの里１、２", "capacity": 24, "address": "津市一志町日置46番地", "phone": "059-295-0055", "region": "津市"},
    {"facility_type": "サービス付き高齢者向け住宅", "name": "山水", "capacity": 80, "address": "津市一志町其倉287番地", "phone": "059-268-5101", "region": "津市"},
    {"facility_type": "サービス付き高齢者向け住宅", "name": "サービス付き高齢者向け住宅つみなみ シルバーケア豊壽園", "capacity": 23, "address": "津市高茶屋小森町1316番地3", "phone": "059-234-4888", "region": "津市"},
    {"facility_type": "サービス付き高齢者向け住宅", "name": "サービス付き高齢者向け住宅 カトレア下弁財", "capacity": 10, "address": "津市下弁財町津興816番地", "phone": "059-222-0553", "region": "津市"},
    {"facility_type": "サービス付き高齢者向け住宅", "name": "御伽草子久居明神", "capacity": 28, "address": "津市久居明神町2133番地1", "phone": "059-273-6710", "region": "津市"},
    {"facility_type": "サービス付き高齢者向け住宅", "name": "憩いの里 津ケアホーム", "capacity": 60, "address": "津市一身田平野726番地3", "phone": "059-271-6306", "region": "津市", "notes": "介護保険の特定施設入居者生活介護の指定あり"},
    {"facility_type": "サービス付き高齢者向け住宅", "name": "ハーモニーハウス津アネックス", "capacity": 60, "address": "津市久居明神町2073番地", "phone": "059-226-1900", "region": "津市", "notes": "介護保険の特定施設入居者生活介護の指定あり"},
    {"facility_type": "サービス付き高齢者向け住宅", "name": "せせらぎ", "capacity": 34, "address": "津市芸濃町椋本2782番地1", "phone": "059-268-5101", "region": "津市"},
    {"facility_type": "サービス付き高齢者向け住宅", "name": "サービス付き高齢者向け住宅 明神", "capacity": 19, "address": "津市久居明神町1530番地69", "phone": "059-254-3838", "region": "津市"},
    {"facility_type": "サービス付き高齢者向け住宅", "name": "LaSincerite雲出", "capacity": 20, "address": "津市雲出本郷町1523番地4", "phone": "059-273-6030", "region": "津市"},
    {"facility_type": "サービス付き高齢者向け住宅", "name": "クレインプラザ", "capacity": 36, "address": "津市久居東鷹跡町243番地", "phone": "059-256-2250", "region": "津市"},
    {"facility_type": "サービス付き高齢者向け住宅", "name": "シニアハウス・エミタス", "capacity": 28, "address": "津市高茶屋小森町5番地", "phone": "059-235-1165", "region": "津市"},
    {"facility_type": "サービス付き高齢者向け住宅", "name": "サービス付き高齢者向け住宅 虹", "capacity": 27, "address": "津市末広町918番地・919番地", "phone": "059-246-5252", "region": "津市"},
    {"facility_type": "サービス付き高齢者向け住宅", "name": "エミタスー志高野", "capacity": 33, "address": "津市一志町高野183番地7", "phone": "059-202-8880", "region": "津市"},
    {"facility_type": "サービス付き高齢者向け住宅", "name": "サービス付き高齢者向け住宅 すまいるはうす藤方", "capacity": 44, "address": "津市藤方1529番地", "phone": "059-253-2522", "region": "津市"},
    {"facility_type": "サービス付き高齢者向け住宅", "name": "サービス付き高齢者向け住宅 ケアスイート", "capacity": 18, "address": "津市藤方1660番地1", "phone": "059-253-7950", "region": "津市"},
    {"facility_type": "サービス付き高齢者向け住宅", "name": "アヴェニール 高茶屋", "capacity": 54, "address": "津市高茶屋小森町1895番地", "phone": "059-253-2238", "region": "津市"},
    {"facility_type": "サービス付き高齢者向け住宅", "name": "シニアハウスなないろ", "capacity": 28, "address": "津市末広町994番地", "phone": "059-253-1265", "region": "津市"},
    {"facility_type": "サービス付き高齢者向け住宅", "name": "サービス付き高齢者向け住宅 おおのき", "capacity": 20, "address": "津市一志大仰58番地", "phone": "059-269-5570", "region": "津市"},
    {"facility_type": "サービス付き高齢者向け住宅", "name": "サービス付き高齢者向け住宅 花のん", "capacity": 30, "address": "津市一志町高野160番地657", "phone": "059-273-5756", "region": "津市"},
    {"facility_type": "サービス付き高齢者向け住宅", "name": "ゴールドエイジ久居", "capacity": 55, "address": "津市久居明神町2715番地1", "phone": "059-273-6200", "region": "津市"},
    {"facility_type": "サービス付き高齢者向け住宅", "name": "サービス付き高齢者向け住宅 トマトハウス", "capacity": 45, "address": "津市久居北口町438番地40", "phone": "059-253-1256", "region": "津市"},
    {"facility_type": "サービス付き高齢者向け住宅", "name": "ゴールドエイジ白塚", "capacity": 42, "address": "津市白塚町357番地18", "phone": "059-269-6800", "region": "津市"},
    {"facility_type": "サービス付き高齢者向け住宅", "name": "ゴールドエイジ一身田", "capacity": 55, "address": "津市一身田中野268番1", "phone": "059-269-7300", "region": "津市"},
    {"facility_type": "サービス付き高齢者向け住宅", "name": "ゴールドエイジ高茶屋", "capacity": 89, "address": "津市高茶屋一丁目23番3号", "phone": "059-269-6200", "region": "津市"},
    # 介護老人保健施設
    {"facility_type": "介護老人保健施設", "name": "医療法人緑の風介護老人保健施設 いこいの森", "capacity": 100, "address": "津市河芸町東千里3番地1", "phone": "059-245-6777", "region": "津市"},
    {"facility_type": "介護老人保健施設", "name": "津老人保健施設アルカディア", "capacity": 100, "address": "津市乙部11番5号", "phone": "059-227-6681", "region": "津市"},
    {"facility_type": "介護老人保健施設", "name": "介護老人保健施設 トマト", "capacity": 100, "address": "津市殿村860番地2", "phone": "059-237-5050", "region": "津市"},
    {"facility_type": "介護老人保健施設", "name": "地域総合ケアセンター津介護老人保健施設シルバーケア豊壽園", "capacity": 100, "address": "津市高茶屋小森上野町737番地", "phone": "059-235-5511", "region": "津市"},
    {"facility_type": "介護老人保健施設", "name": "萩の原 介護老人保健施設", "capacity": 50, "address": "津市久居井戸山町759番地", "phone": "059-256-5515", "region": "津市"},
    {"facility_type": "介護老人保健施設", "name": "芹の里 介護老人保健施設", "capacity": 100, "address": "津市久居井戸山町759番地7", "phone": "059-256-8180", "region": "津市"},
    {"facility_type": "介護老人保健施設", "name": "介護老人保健施設 さくら苑", "capacity": 75, "address": "津市榊原町5630番地", "phone": "059-252-2751", "region": "津市"},
    {"facility_type": "介護老人保健施設", "name": "介護老人保健施設 第二さくら苑", "capacity": 80, "address": "津市榊原町5599番地", "phone": "059-252-3230", "region": "津市"},
    {"facility_type": "介護老人保健施設", "name": "医療法人府洲会介護老人保健施設 ロマン", "capacity": 100, "address": "津市芸濃町椋本6176番地", "phone": "059-265-6500", "region": "津市"},
    {"facility_type": "介護老人保健施設", "name": "介護老人保健施設 あのう", "capacity": 100, "address": "津市安濃町東観音寺353番地", "phone": "059-267-1800", "region": "津市"},
    {"facility_type": "介護老人保健施設", "name": "介護老人保健施設 万葉の里", "capacity": 78, "address": "津市一志町高野236番地5", "phone": "059-295-1600", "region": "津市"},
    {"facility_type": "介護老人保健施設", "name": "介護老人保健施設 万葉の里（ユニット型）", "capacity": 22, "address": "津市一志町高野236番地5", "phone": "059-295-1600", "region": "津市"},
    {"facility_type": "介護老人保健施設", "name": "介護老人保健施設 つつじの里", "capacity": 100, "address": "津市白山町二本木1163番地", "phone": "059-264-0111", "region": "津市"},
    # 介護医療院 (3)
    {"facility_type": "介護医療院", "name": "倉本病院介護医療院", "capacity": 27, "address": "津市下弁財町津興3040番地", "phone": "059-227-6712", "region": "津市"},
    {"facility_type": "介護医療院", "name": "幸和病院介護医療院", "capacity": 48, "address": "津市一身田町767番地", "phone": "059-231-6001", "region": "津市"},
    {"facility_type": "介護医療院", "name": "第二岩崎病院介護医療院", "capacity": 20, "address": "津市一身田町387番地", "phone": "059-232-2316", "region": "津市"},
    # グループホーム
    {"facility_type": "グループホーム", "name": "医療法人緑の風 グループホーム くつろぎの家", "capacity": 9, "address": "津市河芸町東千里13番地2", "phone": "059-245-6065", "region": "津市"},
    {"facility_type": "グループホーム", "name": "高齢者グループホームあじさいの家", "capacity": 9, "address": "津市高洲町17番17号", "phone": "059-228-1117", "region": "津市"},
    {"facility_type": "グループホーム", "name": "高齢者グループホーム水仙の家", "capacity": 9, "address": "津市高洲町33番6号", "phone": "059-227-1114", "region": "津市"},
    {"facility_type": "グループホーム", "name": "シルバータウン新町グループホーム", "capacity": 18, "address": "津市南丸之内7番12号", "phone": "059-225-0131", "region": "津市"},
    {"facility_type": "グループホーム", "name": "グループホームレモンの里", "capacity": 9, "address": "津市神納418番地1", "phone": "059-229-8433", "region": "津市"},
    {"facility_type": "グループホーム", "name": "グループホームつくしんぼ一色", "capacity": 9, "address": "津市一色町240番地", "phone": "059-228-0715", "region": "津市"},
    {"facility_type": "グループホーム", "name": "安東苑", "capacity": 18, "address": "津市安東町2004番地", "phone": "059-246-8246", "region": "津市"},
    {"facility_type": "グループホーム", "name": "グループホームとのむら", "capacity": 18, "address": "津市殿村1553番地", "phone": "059-237-3450", "region": "津市"},
    {"facility_type": "グループホーム", "name": "おもいやり介護の会 グループホームつくしんぼ", "capacity": 6, "address": "津市片田志袋町300番地181", "phone": "059-237-5301", "region": "津市"},
    {"facility_type": "グループホーム", "name": "グループホームコロナ", "capacity": 18, "address": "津市大里窪田町1706番地26", "phone": "059-231-7890", "region": "津市"},
    {"facility_type": "グループホーム", "name": "グループホームフルハウス", "capacity": 9, "address": "津市香良洲町1990番地", "phone": "059-292-8545", "region": "津市"},
    {"facility_type": "グループホーム", "name": "グループホーム渚園", "capacity": 18, "address": "津市柳山津興382番地4", "phone": "059-227-7737", "region": "津市"},
    {"facility_type": "グループホーム", "name": "グループホームなのはな", "capacity": 18, "address": "津市柳山津興3306番地", "phone": "059-221-5600", "region": "津市"},
    {"facility_type": "グループホーム", "name": "グループホーム潮風", "capacity": 9, "address": "津市阿漕町津興214番地2", "phone": "059-246-8800", "region": "津市"},
    {"facility_type": "グループホーム", "name": "グループホームたんぽぽ", "capacity": 18, "address": "津市津田140番地6", "phone": "059-223-6677", "region": "津市"},
    {"facility_type": "グループホーム", "name": "八幡園グループホーム", "capacity": 9, "address": "津市津興2947番地", "phone": "059-213-7535", "region": "津市"},
    {"facility_type": "グループホーム", "name": "グループホームおたっしゃ長屋", "capacity": 9, "address": "津市野田165番地", "phone": "059-239-1977", "region": "津市"},
    {"facility_type": "グループホーム", "name": "しおりの里グループホーム", "capacity": 18, "address": "津市野田2033番地1", "phone": "059-239-1318", "region": "津市"},
    {"facility_type": "グループホーム", "name": "地域総合ケアセンター認知症対応型グループホームシルバーケア豊壽園", "capacity": 9, "address": "津市高茶屋小森町4159番地", "phone": "059-235-5660", "region": "津市"},
    {"facility_type": "グループホーム", "name": "シルバータウン久居寿梨庵", "capacity": 18, "address": "津市久居明神町1553番地10", "phone": "059-254-0111", "region": "津市"},
    {"facility_type": "グループホーム", "name": "グループホーム萩の家", "capacity": 6, "address": "津市久居井戸山町751番地1", "phone": "059-259-2888", "region": "津市"},
    {"facility_type": "グループホーム", "name": "グループホームにのみの家", "capacity": 27, "address": "津市新家町1488番地", "phone": "059-254-1616", "region": "津市"},
    {"facility_type": "グループホーム", "name": "グループホームひまわり", "capacity": 27, "address": "津市戸木町4113番地11", "phone": "059-254-0606", "region": "津市"},
    {"facility_type": "グループホーム", "name": "グループホームふるさと", "capacity": 9, "address": "津市戸木町4113番地56", "phone": "059-255-8828", "region": "津市"},
    {"facility_type": "グループホーム", "name": "グループホーム琴葉はつらつ", "capacity": 18, "address": "津市芸濃町椋本5481番地2", "phone": "059-266-1888", "region": "津市"},
    {"facility_type": "グループホーム", "name": "グループホームなごみ苑", "capacity": 9, "address": "津市豊が丘二丁目4番5号", "phone": "059-230-7171", "region": "津市"},
    {"facility_type": "グループホーム", "name": "グループホーム青い鳥", "capacity": 9, "address": "津市豊が丘二丁目38番6号", "phone": "059-230-2381", "region": "津市"},
    {"facility_type": "グループホーム", "name": "シルバータウンあのうグループホーム", "capacity": 18, "address": "津市安濃町田端上野892番地1", "phone": "059-268-5500", "region": "津市"},
    {"facility_type": "グループホーム", "name": "愛の家グループホーム一志", "capacity": 18, "address": "津市一志町井生220番地1", "phone": "059-293-0005", "region": "津市"},
    {"facility_type": "グループホーム", "name": "グループホーム白山", "capacity": 18, "address": "津市白山町南出954番地", "phone": "059-262-5230", "region": "津市"},
    # 高齢者生活福祉センター (その他)
    {"facility_type": "その他", "name": "美杉高齢者生活福祉センター", "capacity": 17, "address": "津市美杉町奥津929番地", "phone": "059-274-0022", "region": "津市", "notes": "高齢者生活福祉センター"},
]


class Command(BaseCommand):
    help = "PDFから読み取った施設データを一括登録します"

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="全施設データを削除して再登録",
        )

    def handle(self, *args, **options):
        if options["reset"]:
            deleted, _ = Facility.objects.all().delete()
            self.stdout.write(f"既存データを {deleted} 件削除しました")

        created = 0
        updated = 0
        for data in FACILITIES_DATA:
            town = parse_town(data.get("address", ""))
            obj, is_new = Facility.objects.get_or_create(
                name=data["name"],
                facility_type=data["facility_type"],
                defaults={
                    "region": data.get("region", "津市"),
                    "address": data.get("address", ""),
                    "phone": data.get("phone", ""),
                    "capacity": data.get("capacity"),
                    "notes": data.get("notes", ""),
                    "town": town,
                },
            )
            if is_new:
                created += 1
            else:
                # 既存データの town を更新
                if not obj.town and town:
                    obj.town = town
                    obj.save(update_fields=["town"])
                    updated += 1

        self.stdout.write(self.style.SUCCESS(
            f"完了: {created} 件登録、{updated} 件town更新"
        ))
