# UIデザインガイドライン

## 基本色使用原則

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

#### 使用場面
- **カード背景**: 白 (#ffffff)
- **ページ背景**: ライトグレー (#f8f9fa)
- **境界線**: ライトグレー (#dee2e6)
- **メインテキスト**: 黒/ダークグレー
- **補助テキスト**: ミディアムグレー
- **アイコン**: グレー系

#### 禁止事項
- テキストや背景への色付き要素の使用
- 装飾的な色の追加
- カラフルな背景やグラデーション

## ボタンスタイル統一規格

### 基本ボタンスタイル

**利用者一覧の操作ボタンを基準とする**

**HTML構造:**
```html
<button class="btn btn-outline-secondary btn-sm" style="transition: all 0.2s ease;">
    テキスト
</button>
```

**基本スペック:**
- クラス: `btn btn-outline-secondary btn-sm`
- トランジション: `transition: all 0.2s ease`
- フォントサイズ・パディング: レイアウトに応じて調整

### ホバーアニメーション効果

**共通アニメーション:**
```css
button:hover {
    transform: translateY(-1px);
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
```

### 色分け体系

#### 基本原則: 通常時は全てグレー枠、ホバー時に機能別色変化

**通常時**: 全ボタン `btn-outline-secondary` (グレー枠)

#### ホバー時の色分け

#### 1. 保存系ボタン
- **用途**: 保存、保存して戻る、確定
- **ホバー時**: 赤っぽい色
  - 背景色: `#f8d7da`
  - 枠色: `#dc3545`
  - 文字色: `#dc3545`

#### 2. プレビュー系ボタン
- **用途**: プレビュー、表示、確認
- **ホバー時**: 緑っぽい色
  - 背景色: `#d1f2d1`
  - 枠色: `#198754`
  - 文字色: `#198754`

#### 3. 一般操作ボタン
- **用途**: 戻る、印刷、詳細を見る、編集する、試算する、管理する
- **ホバー時**: グレー色
  - 背景色: `#f5f5f5`
  - 枠色: `#999`
  - 文字色: `#333`

#### 4. 作成・新規ボタン (特別な場合のみ)
- **用途**: 新規作成、書類作成
- **ホバー時**: 青っぽい色
  - 背景色: `#e3f2fd`
  - 枠色: `#0d6efd`
  - 文字色: `#0d6efd`

#### 5. 警告・編集ボタン (特別な場合のみ)
- **用途**: 再編集、変更、更新
- **ホバー時**: 黄色
  - 背景色: `#fff3cd`
  - 枠色: `#ffc107`
  - 文字色: `#ffc107`

## 介護度表示色体系

### 要支援・要介護度のバッジ色

**利用者一覧で使用している色体系:**

#### 要支援系
- **要支援1**: `badge bg-info` (#0dcaf0 - 明るい青)
- **要支援2**: `badge bg-info` (#0dcaf0 - 明るい青)

#### 要介護系
- **要介護1**: `badge bg-warning` (#ffc107 - 黄色)
- **要介護2**: `badge bg-warning` (#ffc107 - 黄色)
- **要介護3**: `badge bg-danger` (#dc3545 - 赤色)
- **要介護4**: `badge bg-danger` (#dc3545 - 赤色)
- **要介護5**: `badge bg-dark` (#212529 - 濃いグレー)

### 介護度による色の意味
- **青系**: 要支援（軽度）
- **黄系**: 要介護軽度（1-2）
- **赤系**: 要介護中度（3-4）
- **黒系**: 要介護重度（5）

## 実装時のCSS例

```css
/* 基本ボタンスタイル */
.btn-outline-secondary.btn-sm:hover {
    background-color: #f5f5f5 !important;
    border-color: #999 !important;
    color: #333 !important;
    transform: translateY(-1px);
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.btn-outline-success:hover {
    background-color: #d1f2d1 !important;
    border-color: #198754 !important;
    color: #198754 !important;
    transform: translateY(-1px);
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.btn-outline-info:hover {
    background-color: #e3f2fd !important;
    border-color: #0d6efd !important;
    color: #0d6efd !important;
    transform: translateY(-1px);
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.btn-outline-warning:hover {
    background-color: #fff3cd !important;
    border-color: #ffc107 !important;
    color: #ffc107 !important;
    transform: translateY(-1px);
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.btn-outline-danger:hover {
    background-color: #f8d7da !important;
    border-color: #dc3545 !important;
    color: #dc3545 !important;
    transform: translateY(-1px);
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
```

## 適用原則

### ボタン選択基準
1. **機能の性質でホバー色を選択**
   - 保存・確定 → 赤っぽい色
   - プレビュー・表示・確認 → 緑っぽい色
   - 一般操作（戻る・印刷・詳細・編集・試算・管理） → グレー色
   - 作成・新規（特別な場合） → 青っぽい色
   - 再編集・変更（特別な場合） → 黄色

2. **通常時の統一**
   - 全ボタンは `btn-outline-secondary` (グレー枠) で統一

3. **サイズ調整**
   - レイアウトに応じてフォントサイズとパディングを適切に調整
   - 重要度に応じてサイズを変更可能

4. **アニメーション統一**
   - 必ず `transition: all 0.2s ease` を適用
   - ホバー時の浮き上がり効果 (`translateY(-1px)`)
   - 統一されたシャドウ効果

### 禁止事項
- 独自の色の追加
- アニメーション効果の変更
- 基本スタイルの大幅な改変
- ボタン以外への色付き装飾の使用

---
*このガイドラインに従うことで、シンプルで統一された美しいUIを維持できます*