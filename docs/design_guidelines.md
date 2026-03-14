# システム共通デザインガイドライン

**最終更新**: 2026-02-24

---

## 1. 基本色使用原則

### シンプルカラー基準

**ボタン以外の要素は基本色のみ使用**

#### 許可されている色
- **白** (#ffffff) - 背景、カード背景
- **黒** (#000000, #212529) - テキスト、アイコン
- **グレー系**
  - ライトグレー (#f8f9fa) - セクション背景
  - ミディアムグレー (#6c757d) - 補助テキスト
  - ダークグレー (#495057) - 見出し
  - 境界線グレー (#dee2e6) - ボーダー

#### 禁止事項
- テキストや背景への色付き要素の使用
- 装飾的な色の追加
- カラフルな背景やグラデーション

---

## 2. カラーパレット（8色体系）

色の統一性を保つため、以下の8色セットを基準として使用する。

| # | カラー | 背景色 | 枠線色 | 用途 |
|---|--------|--------|--------|------|
| 1 | グレー | `#f5f5f5` | `#999999` | 中立的な操作、一般ボタン |
| 2 | ブルー | `#e3f2fd` | `#0d6efd` | 編集操作、情報系 |
| 3 | グリーン | `#e8f5e8` | `#198754` | 計算系、成功系 |
| 4 | オレンジ | `#fff3e0` | `#fd7e14` | 評価系、アセスメント系 |
| 5 | パープル | `#f3e5f5` | `#6f42c1` | 書類系、ドキュメント系 |
| 6 | ピンク | `#ffebee` | `#d63384` | スケジュール系、重要操作 |
| 7 | イエロー | `#fff9c4` | `#ffc107` | 履歴系、記録系、注意喚起 |
| 8 | ベージュ | `#f5f0e8` | `#d2b48c` | 出力系、印刷系 |

### 色の組み合わせパターン

- **パターン1**: 対応する枠線色＋背景色のセット（ボタンホバー等）
- **パターン2**: 背景色のみ（バッジ、ラベル等）
- **パターン3**: 枠線グレー固定（`#999999`）＋ 背景色（介護度バッジ等）

### 補足色
- 白背景: `#ffffff`
- 薄いグレー（ホバー）: `#e9ecef`
- カウントダウン（期限切れ）: `#ffcdd2`
- カウントダウン（30日以内）: `#fff9c4`
- カウントダウン（31日以上）: `#c8e6c9`

---

## 3. ボタンスタイル統一規格

### 基本ルール

- **通常時**: 全ボタン `btn btn-outline-secondary` （グレー枠）
- **トランジション**: `transition: all 0.2s ease`
- **ホバー共通**: `transform: translateY(-1px)` + `box-shadow: 0 2px 4px rgba(0,0,0,0.1)`

### ホバー時の色分け

| 用途 | 背景色 | 枠色 | 文字色 |
|------|--------|------|--------|
| **保存・確定** | `#f8d7da` | `#dc3545` | `#dc3545` |
| **プレビュー・表示** | `#d1f2d1` | `#198754` | `#198754` |
| **一般操作**（戻る・印刷・詳細・編集） | `#f5f5f5` | `#999` | `#333` |
| **作成・新規** | `#e3f2fd` | `#0d6efd` | `#0d6efd` |
| **再編集・変更** | `#fff3cd` | `#ffc107` | `#ffc107` |

### CSS実装例

```css
/* 共通ホバーアニメーション */
.btn:hover {
    transform: translateY(-1px);
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

/* 一般操作ボタン */
.btn-outline-secondary:hover {
    background-color: #f5f5f5 !important;
    border-color: #999 !important;
    color: #333 !important;
}
```

---

## 4. 選択ボタン（アセスメント等）

カラーテーマ `body.theme-current` 使用時：

| カテゴリ | 背景色 | 枠色 | 文字色 |
|----------|--------|------|--------|
| **ポジティブ**（可能・自立・あり） | `#e3f2fd` | `#0d6efd` | `#0d6efd` |
| **ネガティブ**（不可能・全介助・なし） | `#ffc8dd` | `#d63384` | `#d63384` |
| **ニュートラル**（不明・見守り） | `#d1f2d1` | `#198754` | `#198754` |

---

## 5. 介護度表示色

### パターン3（枠線グレー固定＋背景色）使用

| 介護度 | 枠線色 | 背景色 |
|--------|--------|--------|
| 要支援1・2 | `#999999` | `#f5f5f5` |
| 要介護1 | `#999999` | `#e3f2fd` |
| 要介護2 | `#999999` | `#fff3e0` |
| 要介護3 | `#999999` | `#f3e5f5` |
| 要介護4 | `#999999` | `#ffebee` |
| 要介護5 | `#999999` | `#e8f5e8` |

---

## 6. フォームバリデーション仕様

### 未入力チェック時の挙動

保存ボタン押下時に必須項目が未入力の場合：

1. **アラート表示**: 未入力項目を示すメッセージを `alert` で表示
2. **フォーカス移動**: 該当フィールドにカーソルを移動
3. **スクロール**: 該当フィールドが画面中央に表示されるようスクロール
4. **折りたたみ要素の展開**: アコーディオン・タブ等の中にある場合は先に展開

### 基本実装

```javascript
const focusAndScroll = function(element) {
    if (element) {
        element.focus();
        element.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
};

if (!fieldElement.value.trim()) {
    alert('○○を入力してください。');
    focusAndScroll(fieldElement);
    return false;
}
```

### アコーディオン内の項目

```javascript
const openCollapseAndFocus = function(element, collapseId) {
    const collapseElement = document.getElementById(collapseId);
    if (collapseElement && !collapseElement.classList.contains('show')) {
        new bootstrap.Collapse(collapseElement, { show: true });
        setTimeout(function() {
            element.focus();
            element.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }, 400);
    } else {
        focusAndScroll(element);
    }
};
```

### Bootstrapバリデーションスタイル無効化

`django_bootstrap5` 使用ページで枠色変更・アイコン表示を無効化する CSS：

```css
.form-control.is-valid, .form-control.is-invalid,
.form-select.is-valid, .form-select.is-invalid {
    border-color: #ced4da !important;
    background-image: none !important;
    padding-right: 0.75rem !important;
}
.valid-feedback, .invalid-feedback {
    display: none !important;
}
```

### 適用済みページ

| ページ | ファイル |
|--------|----------|
| 届出書作成（共通） | `templates/clients/document_create_base.html` |
| 届出書作成（介護予防版） | `templates/clients/document_create_preventive.html` |
| 届出書作成（居宅版） | `templates/clients/document_create_kyotaku.html` |
| アセスメントフォーム | `templates/assessments/detailed_assessment_form.html` |
| 利用者登録 | `templates/clients/client_form.html` (枠色変更・アイコン無効化のみ) |
