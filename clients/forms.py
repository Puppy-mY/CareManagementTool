from django import forms
from .models import Client, Feedback, FeedbackReply, HomeCareSupportOffice


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = [
            # 基本情報
            'name', 'furigana', 'birth_date', 'gender', 'phone', 'address',
            # 保険情報
            'insurance_number', 'care_level', 'certification_date', 'certification_period_start', 'certification_period_end',
            'care_burden',
            'disability_level', 'dementia_level',
            'disability_handbook', 'disability_handbook_type', 'difficult_disease', 'life_protection',
            'medical_insurance_type', 'medical_insurer_name_issuer', 'medical_insurer_number', 'medical_insurance_symbol', 'medical_insurance_number', 'medical_insurance_branch',
            # 公的制度・受給者証（有無のみ）
            'limit_cert', 'high_cost_care',
            'disability_welfare',
            'specific_medical', 'welfare_medical', 'nhi_limit_cert', 'high_cost_combined',
            # 家族情報（1人目）
            'family_name1', 'family_relationship1', 'family_address1', 'family_contact1',
            'family_living_status1', 'family_care_status1', 'family_employment1', 'family_notes1',
            # 家族情報（2人目）
            'family_name2', 'family_relationship2', 'family_address2', 'family_contact2',
            'family_living_status2', 'family_care_status2', 'family_employment2', 'family_notes2',
        ]
        
        widgets = {
            # 基本情報
            'insurance_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '例: 1234567890',
                'maxlength': '10',
                'pattern': '[0-9]{10}',
                'inputmode': 'numeric'
            }),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '例: 介護　太郎'}),
            'furigana': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '例: かいご　たろう'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '例: 059-253-6599'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '例: 三重県津市神戸154-9'}),
            
            # 保険情報
            'care_level': forms.Select(attrs={'class': 'form-select'}),
            'certification_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'certification_period_start': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'certification_period_end': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'care_burden': forms.Select(attrs={'class': 'form-select'}),
            'disability_level': forms.Select(attrs={'class': 'form-select'}),
            'dementia_level': forms.Select(attrs={'class': 'form-select'}),
            'disability_handbook': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'disability_handbook_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '例: 肢体不自由'}),
            'difficult_disease': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'life_protection': forms.CheckboxInput(attrs={'class': 'form-check-input'}),

            # 医療保険情報
            'medical_insurance_type': forms.Select(attrs={'class': 'form-select'}),
            'medical_insurer_name_issuer': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '例: ○○市'}),
            'medical_insurer_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '例: 123456'}),
            'medical_insurance_symbol': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '例: 01'}),
            'medical_insurance_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '例: 1234567890'}),
            'medical_insurance_branch': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '例: 01', 'maxlength': '2'}),
            
            # 家族情報（1人目）
            'family_name1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '例: 介護　花子'}),
            'family_relationship1': forms.Select(attrs={'class': 'form-select'}),
            'family_address1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '例: 三重県津市神戸154-9'}),
            'family_living_status1': forms.Select(attrs={'class': 'form-select'}),
            'family_care_status1': forms.Select(attrs={'class': 'form-select'}),
            'family_employment1': forms.Select(attrs={'class': 'form-select'}),
            'family_contact1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '例: 090-1234-5678'}),
            'family_notes1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '特記事項があれば記載'}),
            
            # 家族情報（2人目）
            'family_name2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '例: 介護　次郎'}),
            'family_relationship2': forms.Select(attrs={'class': 'form-select'}),
            'family_address2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '例: 三重県津市神戸154-9'}),
            'family_living_status2': forms.Select(attrs={'class': 'form-select'}),
            'family_care_status2': forms.Select(attrs={'class': 'form-select'}),
            'family_employment2': forms.Select(attrs={'class': 'form-select'}),
            'family_contact2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '例: 090-1234-5678'}),
            'family_notes2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '特記事項があれば記載'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # 必須フィールドにマークを追加
        required_fields = ['insurance_number', 'name', 'furigana', 'birth_date', 'gender']
        for field_name in required_fields:
            if field_name in self.fields:
                self.fields[field_name].required = True
                self.fields[field_name].widget.attrs['required'] = True
                
        # プレースホルダーやヘルプテキストを設定
        self.fields['insurance_number'].help_text = '介護保険証に記載されている被保険者番号です'
        self.fields['furigana'].help_text = 'ひらがなで入力してください'
        self.fields['certification_date'].help_text = '要介護認定を受けた日付'
        self.fields['certification_period_start'].help_text = '認定の有効期間開始日'
        self.fields['certification_period_end'].help_text = '認定の有効期間終了日'
        # burden_period関連のhelp_textを削除

    def clean_insurance_number(self):
        """被保険者番号のバリデーション（10桁の数字のみ）"""
        insurance_number = self.cleaned_data.get('insurance_number')
        if insurance_number:
            if len(insurance_number) != 10:
                raise forms.ValidationError('被保険者番号は10桁で入力してください。')
            if not insurance_number.isdigit():
                raise forms.ValidationError('被保険者番号は数字のみで入力してください。')
        return insurance_number

    def clean_name(self):
        """氏名のバリデーション（全角・半角スペース必須、保存時は全角スペースに統一）"""
        name = self.cleaned_data.get('name', '')
        if name:
            # 前後の空白を削除
            name = name.strip()
            # 半角スペースを全角スペースに変換
            name = name.replace(' ', '　')
            # 全角スペースが含まれているか確認
            if '　' not in name:
                raise forms.ValidationError('姓と名の間にはスペース（空白）を入れてください。')
        return name

    def clean_furigana(self):
        """ふりがなのバリデーション（全角・半角スペース必須、保存時は全角スペースに統一）"""
        furigana = self.cleaned_data.get('furigana', '')
        if furigana:
            # 前後の空白を削除
            furigana = furigana.strip()
            # 半角スペースを全角スペースに変換
            furigana = furigana.replace(' ', '　')
            # 全角スペースが含まれているか確認
            if '　' not in furigana:
                raise forms.ValidationError('姓と名の間にはスペース（空白）を入れてください。')
        return furigana


class FeedbackForm(forms.ModelForm):
    """フィードバック投稿フォーム"""

    class Meta:
        model = Feedback
        fields = ['category', 'title', 'content', 'password']

        widgets = {
            'category': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '簡潔にタイトルを入力してください',
                'maxlength': '200',
                'required': True
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': '詳細な内容を記入してください。\n不具合の場合は、どのような操作を行った際に発生したかも記載してください。',
                'rows': 8,
                'required': True
            }),
            'password': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '4桁の数字を入力',
                'maxlength': '4',
                'pattern': '[0-9]{4}',
                'required': True,
                'inputmode': 'numeric'
            }),
        }

        labels = {
            'category': 'カテゴリ',
            'title': 'タイトル',
            'content': '詳細内容',
            'password': '閲覧パスワード（4桁の数字）',
        }

        help_texts = {
            'category': '適切なカテゴリを選択してください',
            'password': '後でフィードバックを確認する際に必要です。忘れないようにメモしてください。',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # すべてのフィールドを必須に設定
        for field_name in self.fields:
            self.fields[field_name].required = True

    def clean_password(self):
        """パスワードのバリデーション（4桁の数字のみ）"""
        password = self.cleaned_data.get('password')
        if password:
            if len(password) != 4:
                raise forms.ValidationError('パスワードは4桁で入力してください。')
            if not password.isdigit():
                raise forms.ValidationError('パスワードは数字のみで入力してください。')
        return password


class FeedbackEditForm(forms.ModelForm):
    """フィードバック編集フォーム（管理者用）"""

    class Meta:
        model = Feedback
        fields = ['category', 'title', 'content']

        widgets = {
            'category': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '簡潔にタイトルを入力してください',
                'maxlength': '200',
                'required': True
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': '詳細な内容を記入してください',
                'rows': 8,
                'required': True
            }),
        }

        labels = {
            'category': 'カテゴリ',
            'title': 'タイトル',
            'content': '詳細内容',
        }

        help_texts = {
            'category': '適切なカテゴリを選択してください',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # すべてのフィールドを必須に設定
        for field_name in self.fields:
            self.fields[field_name].required = True


class FeedbackReplyForm(forms.ModelForm):
    """フィードバック返信フォーム"""

    class Meta:
        model = FeedbackReply
        fields = ['content']

        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': '返信内容を入力してください...',
                'rows': 4,
                'required': True
            }),
        }

        labels = {
            'content': '返信内容',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].required = True


class HomeCareSupportOfficeForm(forms.ModelForm):
    """居宅介護支援事業所フォーム"""

    class Meta:
        model = HomeCareSupportOffice
        fields = ['name', 'office_number', 'postal_code', 'address', 'phone', 'fax', 'manager_name', 'is_active']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '例: 居宅介護支援事業所 安濃津ろまん',
                'required': True
            }),
            'office_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '例: 2470100419',
                'maxlength': '20',
                'required': True
            }),
            'postal_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '例: 514-0009'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '例: 三重県津市羽所町○○'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '例: 059-123-4567'
            }),
            'fax': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '例: 059-123-4568'
            }),
            'manager_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '例: 山田 太郎'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

        labels = {
            'name': '事業所名',
            'office_number': '事業所番号',
            'postal_code': '郵便番号',
            'address': '住所',
            'phone': '電話番号',
            'fax': 'FAX',
            'manager_name': '管理者名',
            'is_active': '有効',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 必須フィールド
        self.fields['name'].required = True
        self.fields['office_number'].required = True


_DATE_WIDGET = forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})


class CareInsuranceForm(forms.ModelForm):
    """介護保険関係フォーム"""

    class Meta:
        model = Client
        fields = [
            'care_level', 'certification_date', 'certification_period_start', 'certification_period_end',
            'care_burden', 'burden_period_start', 'burden_period_end',
            'limit_cert', 'limit_cert_start', 'limit_cert_end',
            'high_cost_care',
        ]
        widgets = {
            'care_level': forms.Select(attrs={'class': 'form-select'}),
            'certification_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'certification_period_start': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'certification_period_end': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'care_burden': forms.Select(attrs={'class': 'form-select'}),
            'burden_period_start': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'burden_period_end': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'limit_cert_start': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'limit_cert_end': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class DisabilityWelfareForm(forms.ModelForm):
    """障害福祉関係フォーム"""

    class Meta:
        model = Client
        fields = [
            'disability_welfare',
            'disability_welfare_cert_start', 'disability_welfare_cert_end',
            'disability_welfare_decision_start', 'disability_welfare_decision_end',
        ]
        widgets = {
            'disability_welfare_cert_start': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'disability_welfare_cert_end': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'disability_welfare_decision_start': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'disability_welfare_decision_end': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class MedicalCertForm(forms.ModelForm):
    """医療関係フォーム"""

    class Meta:
        model = Client
        fields = [
            'specific_medical', 'specific_medical_start', 'specific_medical_end',
            'welfare_medical', 'welfare_medical_start', 'welfare_medical_end',
            'nhi_limit_cert', 'nhi_limit_cert_start', 'nhi_limit_cert_end',
            'high_cost_combined',
        ]
        widgets = {
            'specific_medical_start': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'specific_medical_end': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'welfare_medical_start': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'welfare_medical_end': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'nhi_limit_cert_start': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'nhi_limit_cert_end': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
