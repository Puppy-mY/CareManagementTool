# Excel座標設定リファレンス

このファイルは、`excel_coordinates.json`で使用している座標設定の詳細説明です。
記載例）
|　| フィールド名 | セル座標 | フォーム項目名 |

## 居宅サービス計画作成依頼（変更）届出書

|　| フォーム項目名 | フィールド名 | セル座標 |
|　|--------------|----------|----------------|
|　| 氏名 | client_name | A6 |
|　| ふりがな | client_furigana | D5 |
|　| 被保険者番号 | insurance_number | N5 |
|　| 生年月日 | birth_date | O10 | 
|　| 要介護度 | care_level | AF3 |
|　| 担当ケアマネジャー | care_manager_name | U15 |
|　| 新規・変更 | reason_new_or_change | A18 |
|　| 区分変更 | reason_level_change | A19 |
|　| 暫定ケアプラン（認定結果と異なる場合） | reason_provisional_different | A20 |
|　| その他 | reason_other | A21 |
|　| その他の詳細 | reason_other_detail | E21 |
|　| 実施開始日 | effective_start_date | T21 |
|　| 住所 | client_address | J33 |
|　| 負担同意書（事業者から） | burden_agree_provider | A25 |
|　| 負担同意書（郵送） | burden_agree_mail | A26 |
|　| 負担同意書（同時提出） | burden_agree_simultaneous | A27 |

## アセスメントシート

### 基本事項等
   | フォーム項目名 | フィールド名 | セル座標 |
   |---------------|------------|--------|
 〇| 作成年月日 | assessment_date | AF1 |
 〇| アセスメントの理由 | assessment_type | G3 | その他の詳細（assessment_type_other）
 〇| 面談場所 | interview_location | V3 | その他の詳細（interview_location_other）
 〇| 作成者 | assessor | AG3 |
 〇| 氏名 | client_name | D5 |
 〇| ふりがな | client_furigana | D4 |
 〇| 性別 | client_gender | R5 |
 〇| 生年月日 | birth_date | X5 |
 〇| 年齢 | client_age | AD5 |
 〇| 住所 | client_address | D7 |
 〇| 連絡先 | client_contact | AD7 |

### 保険情報
   | フォーム項目名 | フィールド名 | セル座標 |
   |---------------|------------|--------|
 〇| 被保険者番号 | insurance_number | E10 |
 〇| 要介護度 | care_level_official | J10 |
 〇| 認定日 | certification_date | Q10 |
 〇| 認定期間（開始） | certification_period_start | V10 |
 〇| 認定期間（終了） | certification_period_end | AC10 |
 〇| 負担割合 | burden_ratio | AI10 |
 | 医療保険 | medical_insurance | B13 |
 〇| 身体障がい者手帳の有無 | disability_handbook | M13 |
 | 身体障がい者手帳の種類 | disability_type | O13 |
 | 難病申請 | difficult_disease | R13 |
 〇| 生活保護 | life_protection | V13 |
 | 障がい者日常生活自立度 | disability_level | Z13 |
 | 認知症日常生活自立度 | dementia_level | AF13 |

### 家族状況
   | フォーム項目名 | フィールド名 | セル座標 |
   |---------------|------------|--------|
 | 家族氏名-1 | family_member1_name | C16 |
 | 続柄-1 | family_member1_relation | I16 |
 | 住所-1 | family_member1_address | L16 |
 | 連絡先-1 | family_member1_contact | S16 |
 | 介護-1 | family_member1_care | X16 |
 | 同居有無-1 | family_member1_living_together | AA16 |
 | 就労の有無-1 | family_member1_job | AD16 |
 | 備考（KP等）-1 | family_member1_notes | AF16 |
 | 家族氏名-2 | family_member2_name | C18 |
 | 続柄-2 | family_member2_relation | I18 |
 | 住所-2 | family_member2_address | L18 |
 | 連絡先-2 | family_member2_contact | S18 |
 | 介護-2 | family_member2_care | X18 |
 | 同居有無-2 | family_member2_living_together | AA18 |
 | 就労の有無-2 | family_member2_job | AD18 |
 | 備考（KP等）-2 | family_member2_notes | AF18 |

### 住居状況
   | フォーム項目名 | フィールド名 | セル座標 |
   |---------------|------------|--------|
 〇| 家庭環境 | home_environment | F20 |
 〇| 住居形態 | housing_type | F21 |
 |
 〇| 住居権利 | housing_ownership | F22 |
 〇| 専有居室 | private_room | F23 |
 〇| 冷暖房 | air_conditioning | R20 |
 〇| トイレ | toilet_type | R21 |
 | 
 〇| 浴室 | bathroom | R22 |
 〇| 就寝 | sleeping_arrangement | R223 | その他の詳細
 〇| 居室段差 | room_level_difference | AD20 |
 〇| 住宅改修 | housing_modification | AD21 |
 〇| 住宅改修の必要性 | housing_modification_need | AF22 |
 〇| 特別な状況 | special_circumstances | AD23 | 

### 健康状態
   | フォーム項目名 | フィールド名 | セル座標 |
   |---------------|------------|--------|
 〇| 疾患名-1 | disease_name_1 | B25 |
 〇| 発症日-1 | onset_date_1 | N25 |
 〇| 疾患名-2 | disease_name_2 | B26 |
 〇| 発症日-2 | onset_date_2 | N26 |
 〇| 疾患名-3 | disease_name_3 | B27 |
 〇| 発症日-3 | onset_date_3 | N27 |
 〇| 疾患名-4 | disease_name_4 | B29 |
 〇| 発症日-4 | onset_date_4 | N29 |
 〇| 疾患名-5 | disease_name_5 | B31 |
 〇| 発症日-5 | onset_date_5 | N31 |
 〇| 疾患名-6 | disease_name_6 | B33 |
 〇| 発症日-6 | onset_date_6 | N33 |
 〇| 既往 | medical_history | R25 |
 | 特別な医療処置 | special_medical_treatment | V28 |
 | 主治医＊安濃津ろまん入居後（中）病院・クリニック名 | main_doctor_hospital | V30 |
 | 主治医氏名 | main_doctor_name | AD30 |
 | 往診医　病院・クリニック名 | visiting_doctor_hospital | V32 |
 | 往診医氏名 | visiting_doctor_name | AD32 |
 | かかりつけ医-1 | family_doctor_1 | V34 |
 | かかりつけ医-2 | family_doctor_2 | AD34 |
 | かかりつけ医-3 | family_doctor_3 | V35 |
 | かかりつけ医-4 | family_doctor_4 | AD35 |
 | 通院状況 | hospital_visit_info | V36 |
 | アレルギーの有無 | has_allergy | F37 |
 | アレルギーの種類 | allergy_details | I37 |
 | 服薬状況 | medication_content | V38 |

### サービス利用状況
   | フォーム項目名 | フィールド名 | セル座標 |
   |---------------|------------|--------|
 | 介護サービス | care_services | F40 |
 | 福祉用具 | welfare_equipment | V40 |
 | その他のサービス | other_services | V42 |
 | インフォーマルサービス | informal_services | F43 |
 | 社会との関り | social_relationships | V43 |

### 本人・家族の希望等
   | フォーム項目名 | フィールド名 | セル座標 |
   |---------------|------------|--------|
 | 本人の希望 | personal_hopes | A47 |
 | 家族の希望 | family_hopes | S47 |
 | 生活歴 | life_history | B50 |
 | 特記・備考 | notes | A54 |

### 身体状況
   | フォーム項目名 | フィールド名 | セル座標 |
   |---------------|------------|--------|
 | 皮膚疾患 | skin_disease | I58 |
 | 感染症 | infection_status | I59 |
 | 特別な医療処置 | special_medical_treatment | I60 |
 | 麻痺の有無 | paralysis_location | I61 |
 | 痛みの有無 | pain_location | I62 |
 〇| 身長 | height | I63 |
 〇| 体重 | weight | I64 |
 | 視力 | vision | I65 |
 | 眼鏡等 | uses_glasses | I66 |
 | 聴力 | hearing | I67 |
 | 補聴器等 | uses_hearing_aid | I68 |
 | 身体状況の詳細 | physical_notes | P58 |

### 基本動作
   | フォーム項目名 | フィールド名 | セル座標 |
   |---------------|------------|--------|
 | 寝返り | turning_over | I69 |
 | 起き上がり |  | I70 |
 | 座位 | sitting | I71 |
 | 立ち上がり | standing_up | I72 |
 | 立位 | standing | I73 |
 | 移乗 | transfer | I74 |
 | 屋内移動 | indoor_mobility | I75 |
 | 使用用具（屋内） | indoor_mobility_equipment | I76 |
 | 屋外移動 | outdoor_mobility | I77 |
 | 使用用具（屋外） | outdoor_mobility_equipment | I78 |
 | 基本動作の詳細 | basic_activity_notes | P69 |

### ADL
   | フォーム項目名 | フィールド名 | セル座標 |
   |---------------|------------|--------|
 | 食事方法 | eating_method | I79 |
 | 食事動作 | eating_assistance | I80 |
 | 嚥下 | swallowing | I81 |
 | 主食 | meal_form_main | I82 |
 | 副食 | meal_form_side | I83 |
 | 水分とろみ | water_thickening | I84 |
 | 食事制限 | eating_restriction | I85 |
 | 道具・用具 | eating_utensils | I86 |
 | 食事の詳細 | eating_notes | P79 |
 | 口腔衛生 | oral_hygiene_assistance | I87 |
 | 自歯の有無 | natural_teeth_presence | I88 |
 | 有無・種類 | denture_type | I89 |
 | 場所 | denture_location | I90 |
 | 口腔の詳細 | oral_notes | P79 |
 | 入浴動作 | bathing_assistance | I91 |
 | 形態 | bathing_form | I92 |
 | 入浴の制限 | bathing_restriction | I93 |
 | 上衣 | dressing_upper | I94 |
 | 下衣 | dressing_lower | I95 |
 | 入浴・更衣の詳細 | bathing_notes | P91 |
 | 排泄動作 | excretion_assistance | I96 |
 | 尿意 | urination | I97 |
 | 失禁 | urinary_incontinence | I98 |
 | 便意 | defecation | I99 |
 | 失禁 | fecal_incontinence | I99 |
 | 日中 | daytime_location | I101 |
 | 夜間 | nighttime_location | I102 |
 | 排泄用品 | excretion_supplies | I103 |
 | 排泄の詳細 | excretion_notes | P96 |   	

### IADL（104-106行目）
   | フォーム項目名 | フィールド名 | セル座標 |
   |---------------|------------|--------|
 | 調理 | cooking | F104 |
 | 洗濯 | washing | F105 |
 | 金銭管理 | money_management | F106 |
 | 掃除 | cleaning | M104 |
 | 買い物 | shopping | M105 |
 | IADLの詳細 | iadl_notes | P104 |

### 認知機能（107-111行目）
   | フォーム項目名 | フィールド名 | セル座標 |
   |---------------|------------|--------|
 | 認知症の有無 | dementia_presence | I107 |
 | 認知症の程度 | dementia_severity | L107 |
 | BPSD | bpsd_symptoms | D108 |
 | 会話 | conversation | I110 |
 | 意思疎通 | communication | I111 |
 | 認知の詳細 | cognitive_notes | P107 |

## 備考

このリファレンスは、アセスメントシートExcelファイル（111行×37列）の主要な入力セルの座標を記録しています。

**フォームフィールドとExcelセルのマッピング方針:**
- ラベルセルは基本的にスキップ（データ入力に使用しない）
- 実際の値を入力するセル座標のみを`excel_coordinates_assessment.json`に記載
- マージセル対応: MergedCellの場合は自動的に左上のセルに書き込み

**今後の拡張:**
- 必要に応じて座標を追加
- フォームフィールドとExcelセルの対応関係を明確化