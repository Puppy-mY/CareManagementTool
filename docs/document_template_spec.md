# 書類作成テンプレート設計書

**ベース書類**: 居宅サービス計画作成依頼（変更）届出書
**参考ファイル**: `templates/clients/document_create.html`
**作成日**: 2025-09-17
**目的**: 全ての書類作成ページの統一テンプレートとして使用

## 📋 使用方法
新しい書類を作成する際は：
1. **このdoc.mdを参考にする**
2. **`templates/clients/document_create.html`（居宅サービス計画作成依頼届出書）をベースとしてコピー**
3. **書類固有の項目に合わせてカスタマイズ**

---

## 1. 基本HTML構造

### 1.1 テンプレート継承
```html
{% extends 'base.html' %}
{% load django_bootstrap5 %}

{% block title %}{{ document_name }} - {{ client.name }}様 - {{ block.super }}{% endblock %}
```

### 1.2 基本レイアウト構造
```html
<div class="container-fluid">
    <div class="row">
        <div class="col-12">
            <!-- ヘッダー部分 -->
            <div class="mb-4">
                <!-- タイトル行 -->
                <div style="margin-bottom: 2rem;">
                    <h1 style="font-size: clamp(1.2rem, 3vw, 2rem); margin: 0; word-break: keep-all; overflow-wrap: break-word;">
                        <i class="fas fa-file-alt"></i> 【書類名】
                    </h1>
                </div>
                <!-- 利用者名と戻るボタンの行 -->
                <div class="d-flex justify-content-between align-items-center">
                    <div class="text-muted" style="font-size: 1.2rem; font-weight: 500;">
                        <i class="fas fa-user"></i> {{ client.name }}様
                    </div>
                    <div>
                        <a href="{% url 'client_list' %}" class="btn btn-outline-secondary back-btn">
                            <i class="fas fa-arrow-left"></i> 戻る
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- メインコンテンツ -->
    <div class="row">
        <div class="col-12">
            <!-- フォーム部分 -->
        </div>
    </div>
</div>
```

---

## 2. フォーム構造パターン

### 2.1 基本フォーム枠組み
```html
<form method="post" id="documentForm">
    {% csrf_token %}
    <input type="hidden" name="action" id="actionField" value="">

    <!-- 利用者基本情報（アコーディオン） -->
    <!-- 手動入力項目 -->
    <!-- アクションボタン -->
</form>
```

### 2.2 アコーディオン形式の基本情報
```html
<div class="accordion mb-4" id="basicInfoAccordion">
    <div class="accordion-item">
        <h2 class="accordion-header" id="basicInfoHeading">
            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#basicInfoCollapse" aria-expanded="false" aria-controls="basicInfoCollapse">
                <i class="fas fa-user-circle me-2"></i>
                <strong>利用者基本情報（自動反映）</strong>
                <small class="text-muted ms-2">※利用者データから自動入力・必要に応じて編集可能</small>
            </button>
        </h2>
        <div id="basicInfoCollapse" class="accordion-collapse collapse" aria-labelledby="basicInfoHeading" data-bs-parent="#basicInfoAccordion">
            <div class="accordion-body">
                <!-- 基本情報フィールド -->
            </div>
        </div>
    </div>
</div>
```

### 2.3 手動入力項目のカード
```html
<div class="card mb-4">
    <div class="card-header d-flex align-items-center">
        <h5 class="mb-0"><i class="fas fa-edit me-2"></i>入力項目（手動入力）</h5>
        <small class="text-muted ms-2">※以下の項目をご入力ください</small>
    </div>
    <div class="card-body">
        <!-- 入力フィールド群 -->
    </div>
</div>
```

---

## 3. 入力フィールドパターン

### 3.1 横並びフィールド（基本情報）
```html
<div class="row g-3 mb-3">
    <div class="col-md-4">
        <label class="form-label">氏名 <span class="text-danger">*</span></label>
        <input type="text" name="client_name" class="form-control" value="{{ client.name }}" required>
    </div>
    <div class="col-md-4">
        <label class="form-label">フリガナ（カタカナ） <span class="text-danger">*</span></label>
        <input type="text" name="client_furigana" class="form-control" value="{{ client.furigana }}" required placeholder="カタカナで入力">
    </div>
    <div class="col-md-4">
        <label class="form-label">生年月日 <span class="text-danger">*</span></label>
        <input type="date" name="client_birth_date" class="form-control" value="{{ client.birth_date|date:'Y-m-d' }}" required>
    </div>
</div>
```

### 3.2 チェックボックス（単一選択）
```html
<div class="row g-3 mb-4">
    <div class="col-12">
        <label class="form-label">選択項目 <span class="text-danger">*</span></label>
        <div class="mt-1">
            <small class="text-muted">説明文</small>
        </div>
        <div class="mt-2">
            <div class="form-check mb-2">
                <input class="form-check-input" type="checkbox" name="field_name" id="option1" value="value1" style="border-radius: 3px;">
                <label class="form-check-label" for="option1">
                    選択肢1
                </label>
            </div>
            <!-- 他の選択肢 -->
        </div>
    </div>
</div>
```

### 3.3 区切り線
```html
<div style="border-top: 1px solid #dee2e6; width: 50%; margin: 1.5rem 0;"></div>
```

---

## 4. アクションボタン

### 4.1 ボタン配置
```html
<div class="row mt-4">
    <div class="col-12">
        <div class="d-flex justify-content-end gap-3">
            <button type="button" class="btn btn-outline-secondary save-btn" onclick="saveDocument()">
                <i class="fas fa-save"></i> 保存して戻る
            </button>
            <button type="button" class="btn btn-outline-secondary excel-btn" onclick="excelDocument()">
                <i class="fas fa-file-excel"></i> Excel出力
            </button>
        </div>
    </div>
</div>
```

---

## 5. JavaScript機能

### 5.1 基本関数構造
```javascript
// 保存処理
function saveDocument() {
    console.log('保存ボタンがクリックされました');
    if (validateForm()) {
        document.getElementById('actionField').value = 'save';
        document.getElementById('documentForm').submit();
    }
}

// Excel出力処理
function excelDocument() {
    console.log('Excel出力ボタンがクリックされました');
    if (validateForm()) {
        document.getElementById('actionField').value = 'excel';
        const form = document.getElementById('documentForm');
        form.target = '_self';  // 同じタブでダウンロード
        form.submit();
    }
}

// バリデーション関数
function validateForm() {
    // 必須項目のチェック
    const clientName = document.querySelector('input[name="client_name"]').value;
    // 他の必須項目...

    if (!clientName.trim()) {
        alert('利用者氏名を入力してください。');
        return false;
    }

    // 他のバリデーション...

    return true;
}
```

### 5.2 DOMContentLoaded処理
```javascript
document.addEventListener('DOMContentLoaded', function() {
    console.log('書類が読み込まれました');

    // フリガナの自動変換（書類によって調整）
    const furiganaField = document.querySelector('input[name="client_furigana"]');
    if (furiganaField) {
        furiganaField.addEventListener('input', function() {
            // ひらがなをカタカナに変換（カタカナ指定の場合）
            // ※書類によってはひらがなのままでOKの場合もある
            this.value = this.value.replace(/[\u3041-\u3096]/g, function(match) {
                const chr = match.charCodeAt(0) + 0x60;
                return String.fromCharCode(chr);
            });
        });
    }

    // 単一選択チェックボックス制御（書類によって調整）
    // ※書類によっては複数選択可能な項目もあるため、必要な項目のみ指定
    const singleSelectGroups = ['notification_type', 'request_reason', 'burden_delivery_method'];

    singleSelectGroups.forEach(groupName => {
        const checkboxes = document.querySelectorAll(`input[name="${groupName}"]`);
        if (checkboxes.length > 0) {
            checkboxes.forEach(checkbox => {
                checkbox.addEventListener('change', function() {
                    if (this.checked) {
                        checkboxes.forEach(cb => {
                            if (cb !== this) cb.checked = false;
                        });
                    }
                });
            });
        }
    });
});
```

---

## 6. CSS設計（UI.md準拠）

### 6.1 基本ボタンスタイル
```css
/* UI.md準拠のボタンスタイル */

/* 基本ボタン設定 */
.btn {
    transition: all 0.2s ease;
}

/* 共通ホバーアニメーション */
.btn:hover {
    transform: translateY(-1px);
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

/* 1. 保存系ボタン - 赤っぽい色 */
.save-btn:hover {
    background-color: #f8d7da !important;
    border-color: #dc3545 !important;
    color: #dc3545 !important;
}

/* 2. Excel出力ボタン - UI.md準拠の緑色 */
.excel-btn:hover {
    background-color: #d1f2d1 !important;
    border-color: #198754 !important;
    color: #198754 !important;
}

/* 3. 一般操作ボタン - グレー色 */
.general-btn:hover,
.back-btn:hover {
    background-color: #f5f5f5 !important;
    border-color: #999 !important;
    color: #333 !important;
}
```

### 6.2 フォーム関連スタイル
```css
.card-header {
    border-bottom: 2px solid #dee2e6;
}

.form-check-input:checked {
    background-color: #0d6efd;
    border-color: #0d6efd;
}

.gap-3 {
    gap: 1rem !important;
}

/* チェックボックス */
.form-check-input {
    width: 1em;
    height: 1em;
}

/* アコーディオン */
.border {
    border-radius: 0.375rem;
    background-color: #f8f9fa;
}
```

---

## 7. Djangoビュー側の処理パターン

### 7.1 基本的な処理フロー
1. GET: 初期表示（利用者データの自動入力）
2. POST: 保存またはExcel出力の処理分岐

### 7.2 フォームデータの取得例
```python
def document_create_view(request, client_id):
    client = get_object_or_404(Client, id=client_id)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'save':
            # 保存処理
            pass
        elif action == 'excel':
            # Excel出力処理
            pass

    context = {
        'client': client,
        'document_name': '書類名',
    }
    return render(request, 'clients/document_create.html', context)
```

---

## 8. レスポンシブ対応

### 8.1 ブレークポイント設計
- `col-12`: 全幅（モバイル）
- `col-md-4`: タブレット以上で1/3幅
- `col-md-6`: タブレット以上で1/2幅

### 8.2 フォントサイズ調整
```css
font-size: clamp(1.2rem, 3vw, 2rem);
```

---

## 9. カスタマイズポイント

### 9.1 新しい書類を作成する際の手順
1. **HTML構造をコピー**
2. **書類名を変更** (`<h1>`タグ内)
3. **手動入力項目を書類に応じて変更**
4. **JavaScript関数名を書類固有に変更**（推奨）
5. **バリデーション条件を調整**
6. **Djangoビューの処理を実装**

### 9.2 必須変更項目
- ページタイトル（`{% block title %}`）
- 書類名（`<h1>`内のテキスト）
- フォームフィールド（name属性、ラベル、バリデーション）
- JavaScript関数内のセレクター
- Djangoビューのロジック

### 9.3 書類によって調整が必要な項目
- **フリガナ**: カタカナ自動変換 vs ひらがなのまま
- **チェックボックス**: 単一選択 vs 複数選択可能
- **入力フィールドの配置**: 横並び vs 縦並び
- **必須項目**: 書類によって必須フィールドが異なる

---

## 10. 注意事項

### 10.1 UI.md準拠の重要性
- ボタンは必ず `btn-outline-secondary` で統一
- ホバー時の色分けは機能別に UI.md に従う
- アニメーション効果は統一する

### 10.2 アクセシビリティ
- 必須項目には `<span class="text-danger">*</span>` を追加
- ラベルとフォームの関連付けを適切に行う
- キーボードナビゲーションを考慮

### 10.3 データ整合性
- フォームの name属性は一意にする
- バリデーションは JavaScript とサーバー側の両方で実装
- CSRF トークンを忘れずに含める

---

**このテンプレートを基準として、統一されたデザインと機能を持つ書類作成ページを効率的に開発できます。**