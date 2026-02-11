from django import template
from datetime import date

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """辞書から指定されたキーの値を取得"""
    if dictionary is None:
        return None
    return dictionary.get(key)

@register.filter
def wareki(value):
    """西暦の日付を和暦に変換"""
    if not value:
        return ""

    from datetime import datetime

    if isinstance(value, str):
        # 文字列の場合は日付オブジェクトに変換
        try:
            value = datetime.strptime(value, '%Y-%m-%d').date()
        except:
            return value
    elif isinstance(value, datetime):
        # datetime オブジェクトの場合は date に変換
        value = value.date()

    year = value.year
    month = value.month
    day = value.day

    # 令和: 2019年5月1日以降
    if value >= date(2019, 5, 1):
        wareki_year = year - 2018
        era = "令和"
    # 平成: 1989年1月8日～2019年4月30日
    elif value >= date(1989, 1, 8):
        wareki_year = year - 1988
        era = "平成"
    # 昭和: 1926年12月25日～1989年1月7日
    elif value >= date(1926, 12, 25):
        wareki_year = year - 1925
        era = "昭和"
    # 大正: 1912年7月30日～1926年12月24日
    elif value >= date(1912, 7, 30):
        wareki_year = year - 1911
        era = "大正"
    # 明治: 1868年1月25日～1912年7月29日
    elif value >= date(1868, 1, 25):
        wareki_year = year - 1867
        era = "明治"
    else:
        # それ以前は西暦で表示
        return f"{year}年{month}月{day}日"

    # 元年の場合
    if wareki_year == 1:
        return f"{era}元年{month}月{day}日"
    else:
        return f"{era}{wareki_year}年{month}月{day}日"
