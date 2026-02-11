"""介護サービス情報公表システムのURLをWeb検索で取得するコマンド"""
import time
import re
import urllib.request
import urllib.parse
import urllib.error

from django.core.management.base import BaseCommand
from facilities.models import Facility


def search_kohyo_url(facility_name):
    """Google検索で介護サービス情報公表システムのURLを取得"""
    query = urllib.parse.quote(f"site:kaigokensaku.mhlw.go.jp/24/ {facility_name} 三重県")
    url = f"https://www.google.com/search?q={query}&num=3"
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    })
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
        # kaigokensaku URLを抽出
        pattern = r'https://www\.kaigokensaku\.mhlw\.go\.jp/24/index\.php\?action_kouhyou_detail_\d+_kihon=true&JigyosyoCd=[^&"]+&ServiceCd=\d+'
        matches = re.findall(pattern, html)
        if matches:
            return matches[0]
        # 生活関連情報の詳細ページパターンも試す
        pattern2 = r'https://www\.kaigokensaku\.mhlw\.go\.jp/24/index\.php\?action_kouhyou_pref_seikatu_detail[^"&\s]+'
        matches2 = re.findall(pattern2, html)
        if matches2:
            return matches2[0]
    except Exception as e:
        return None
    return None


class Command(BaseCommand):
    help = "介護サービス情報公表システムのURLを検索して登録します"

    def add_arguments(self, parser):
        parser.add_argument(
            "--overwrite",
            action="store_true",
            help="既にURLがある施設も上書き",
        )
        parser.add_argument(
            "--type",
            type=str,
            default="",
            help="施設種別でフィルタ（例: 特別養護老人ホーム）",
        )

    def handle(self, *args, **options):
        qs = Facility.objects.all()
        if options["type"]:
            qs = qs.filter(facility_type=options["type"])
        if not options["overwrite"]:
            qs = qs.filter(kaigo_kohyo_url="")

        facilities = list(qs.order_by("facility_type", "name"))
        total = len(facilities)
        self.stdout.write(f"対象施設: {total} 件")

        updated = 0
        failed = 0
        for i, f in enumerate(facilities, 1):
            self.stdout.write(f"[{i}/{total}] {f.facility_type} - {f.name} ... ", ending="")
            url = search_kohyo_url(f.name)
            if url:
                f.kaigo_kohyo_url = url
                f.save(update_fields=["kaigo_kohyo_url"])
                updated += 1
                self.stdout.write(self.style.SUCCESS("OK"))
            else:
                failed += 1
                self.stdout.write(self.style.WARNING("NOT FOUND"))
            # Google検索のレート制限対策
            time.sleep(3)

        self.stdout.write(self.style.SUCCESS(
            f"\n完了: {updated} 件URL登録、{failed} 件見つからず"
        ))
