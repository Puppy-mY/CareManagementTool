import json
import os
from datetime import datetime
from django.conf import settings
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont


class PDFGenerator:
    """効率的なPDF生成のためのヘルパークラス"""

    def __init__(self, document_type):
        self.document_type = document_type
        self.coordinates = self.load_coordinates()
        self.canvas = None
        self.width, self.height = A4

    def load_coordinates(self):
        """座標設定をJSONから読み込み"""
        config_path = os.path.join(settings.BASE_DIR, 'static', 'config', 'pdf_coordinates.json')
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                return config.get(self.document_type, {})
        except FileNotFoundError:
            return {}

    def setup_canvas(self, response):
        """キャンバスの初期設定"""
        self.canvas = canvas.Canvas(response, pagesize=A4)

        # 日本語フォント設定
        try:
            pdfmetrics.registerFont(UnicodeCIDFont('HeiseiKakuGo-W5'))
            self.font_name = 'HeiseiKakuGo-W5'
        except:
            self.font_name = 'Helvetica'

        # 背景画像を配置
        background_path = os.path.join(
            settings.BASE_DIR, 'static', 'images', 'backgrounds',
            f'{self.document_type}-1.png'
        )
        if os.path.exists(background_path):
            self.canvas.drawImage(
                background_path, 0, 0,
                width=self.width, height=self.height,
                preserveAspectRatio=False
            )

    def convert_to_reiwa(self, date_string):
        """西暦から令和に変換"""
        try:
            if isinstance(date_string, str):
                date_obj = datetime.strptime(date_string, '%Y-%m-%d')
            else:
                date_obj = date_string

            reiwa_year = date_obj.year - 2018  # 令和元年は2019年
            return f'令和{reiwa_year}年{date_obj.month}月{date_obj.day}日'
        except:
            return str(date_string)

    def draw_text(self, field_name, value, client_data=None, form_data=None):
        """設定に基づいてテキストを描画"""
        if field_name not in self.coordinates:
            return

        config = self.coordinates[field_name]
        x = config.get('x', 0)
        y = self.height - config.get('y', 0)  # Y座標を反転
        font_size = config.get('font_size', 12)

        self.canvas.setFont(self.font_name, font_size)

        # 値の処理
        if config.get('value'):
            # 固定値
            text = config['value']
        elif config.get('format') == 'reiwa':
            # 令和変換
            text = self.convert_to_reiwa(value) if value else ''
        elif config.get('format') == 'reiwa_period' and form_data:
            # 期間の令和変換
            start = form_data.get('certification_period_start', '')
            end = form_data.get('certification_period_end', '')
            if start and end:
                start_reiwa = self.convert_to_reiwa(start)
                end_reiwa = self.convert_to_reiwa(end)
                text = f'{start_reiwa} ～ {end_reiwa}'
            else:
                text = ''
        else:
            text = str(value) if value else ''

        # テキスト描画
        if config.get('type') == 'multiline':
            self.draw_multiline_text(x, y, text, config)
        else:
            # Noneチェックを追加
            if text is None:
                text = ""
            self.canvas.drawString(x, y, str(text))

    def draw_multiline_text(self, x, y, text, config):
        """複数行テキストを描画"""
        max_lines = config.get('max_lines', 5)
        line_height = config.get('line_height', 14)
        max_chars = config.get('max_chars', 50)

        # Noneチェックを追加
        if text is None:
            text = ""

        lines = text.split('\n')
        for i, line in enumerate(lines[:max_lines]):
            self.canvas.drawString(x, y - (i * line_height), line[:max_chars])

    def draw_checkbox(self, field_name, value, options):
        """チェックボックスを描画"""
        if field_name not in self.coordinates:
            return

        config = self.coordinates[field_name]
        x = config.get('x', 0)
        y = self.height - config.get('y', 0)
        font_size = config.get('font_size', 12)

        self.canvas.setFont(self.font_name, font_size)

        for i, (option_value, option_text) in enumerate(options):
            checkbox = '☑' if value == option_value else '☐'
            text = f'{checkbox} {option_text}'
            self.canvas.drawString(x, y - (i * 15), text)

    def generate_client_fields(self, client, user):
        """利用者の基本情報を描画"""
        # 基本情報の描画
        self.draw_text('name', client.name)
        self.draw_text('furigana', client.furigana)
        self.draw_text('insurance_number', client.insurance_number)
        self.draw_text('birth_date', client.birth_date)

        # 固定情報
        self.draw_text('office_name', None)
        self.draw_text('office_address', None)

        # ケアマネジャー名
        if user.is_authenticated:
            care_manager = user.get_full_name() or user.username
            self.draw_text('care_manager', care_manager)

    def generate_form_fields(self, form_data):
        """フォームデータを描画"""
        if not form_data:
            return

        # 依頼種別（チェックボックス）
        request_type = form_data.get('request_type', '')
        if 'request_type_new' in self.coordinates:
            new_check = '☑' if request_type == 'new' else '☐'
            change_check = '☑' if request_type == 'change' else '☐'
            self.draw_text('request_type_new', f'{new_check} 新規')
            self.draw_text('request_type_change', f'{change_check} 変更')

        # 日付フィールド
        date_fields = ['certification_date', 'request_date', 'effective_start_date']
        for field in date_fields:
            if field in form_data:
                self.draw_text(field, form_data[field], form_data=form_data)

        # 期間フィールド
        self.draw_text('certification_period', '', form_data=form_data)

        # テキストフィールド
        text_fields = ['emergency_contact']
        for field in text_fields:
            if field in form_data:
                self.draw_text(field, form_data[field])

        # 複数行テキストフィールド
        multiline_fields = ['user_situation', 'family_requests']
        for field in multiline_fields:
            if field in form_data and field in self.coordinates:
                config = self.coordinates[field]
                x = config.get('x', 0)
                y = self.height - config.get('y', 0)
                self.canvas.setFont(self.font_name, config.get('font_size', 9))
                self.draw_multiline_text(x, y, form_data[field], config)

        # 依頼事由（チェックボックスグループ）
        request_reason = form_data.get('request_reason', '')
        if 'request_reason' in self.coordinates:
            config = self.coordinates['request_reason']
            x = config.get('x', 0)
            y = self.height - config.get('y', 0)
            self.canvas.setFont(self.font_name, config.get('font_size', 10))

            reason_options = {
                'new_or_change': '新規または事業所変更のため',
                'level_change': '要支援から要介護へ変更のため',
                'provisional_different': '暫定での届出と認定結果が異なるため',
                'other': f"その他: {form_data.get('other_reason_detail', '')}"
            }

            if request_reason in reason_options:
                text = f'☑ {reason_options[request_reason]}'
                self.canvas.drawString(x, y, text)

        # 負担割合証交付方法
        delivery_method = form_data.get('burden_delivery_method', '')
        if 'burden_delivery_method' in self.coordinates:
            config = self.coordinates['burden_delivery_method']
            x = config.get('x', 0)
            y = self.height - config.get('y', 0)
            self.canvas.setFont(self.font_name, config.get('font_size', 10))

            delivery_options = {
                'care_manager': 'ケアマネジャーが受け取る',
                'mail': '自宅への郵送を希望する',
                'with_result': '認定結果と一緒に受け取る'
            }

            if delivery_method in delivery_options:
                text = f'☑ {delivery_options[delivery_method]}'
                self.canvas.drawString(x, y, text)

    def finalize(self):
        """PDF生成を完了"""
        self.canvas.showPage()
        self.canvas.save()


def generate_pdf_with_config(response, document_type, client, user, form_data=None):
    """設定ファイルを使用してPDFを生成"""
    generator = PDFGenerator(document_type)
    generator.setup_canvas(response)
    generator.generate_client_fields(client, user)
    generator.generate_form_fields(form_data)
    generator.finalize()
    return response