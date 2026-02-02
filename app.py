import streamlit as st
from dataclasses import dataclass
from typing import List
import json
import os

# ---------------------------------------------------------
# 1. コンフィグレーション
# ---------------------------------------------------------
GRADUATION_REQ = 128      # 卒業要件総単位数
COMMON_REQ = 44           # 共通教育 必要単位数
SPECIALIZED_REQ = 78      # 専門教育 必要単位数
DATA_FILE = "graduation_data.json" # 保存用ファイル名

# ---------------------------------------------------------
# 2. データ構造
# ---------------------------------------------------------
@dataclass
class Subject:
    name: str
    credits: int
    category: str
    required: bool = False # ●印 (必修)
    is_star: bool = False  # ★印 (数学選択)

# ---------------------------------------------------------
# 3. 全科目データ
# ---------------------------------------------------------
SUBJECT_DATA = [
    # === 【共通教育科目】 ===
    Subject("English I", 1, "common_lang", required=True),
    Subject("English II", 1, "common_lang", required=True),
    Subject("English III", 1, "common_lang"),
    Subject("English IV", 1, "common_lang"),
    Subject("English V", 1, "common_lang"),
    Subject("English VI", 1, "common_lang"),
    Subject("中国語 I", 1, "common_lang"),
    Subject("中国語 II", 1, "common_lang"),
    Subject("中国語 III", 1, "common_lang"),
    Subject("中国語 IV", 1, "common_lang"),
    Subject("海外語学研修 I", 2, "common_lang"),
    Subject("海外語学研修 II", 2, "common_lang"),

    Subject("歴史学", 2, "common_human"),
    Subject("教育学", 2, "common_human"),
    Subject("哲学", 2, "common_human"),
    Subject("地理学", 2, "common_human"),
    Subject("論理学", 2, "common_human"),
    Subject("心理学", 2, "common_human"),

    Subject("日本国憲法", 2, "common_social"),
    Subject("法学概論", 2, "common_social"),
    Subject("人権論", 2, "common_social"),
    Subject("経営学概論", 2, "common_social"),
    Subject("社会学概論", 2, "common_social"),
    Subject("民法", 2, "common_social"),
    Subject("知的財産概論", 2, "common_social"),

    Subject("数学基礎", 2, "common_natural"),
    Subject("幾何学入門", 2, "common_natural"),
    Subject("生物学概論", 2, "common_natural"),
    Subject("計算機科学概論", 2, "common_natural"),
    Subject("人工知能概論", 2, "common_natural"),
    Subject("物理学概論", 2, "common_natural"),
    Subject("地球科学概論", 2, "common_natural"),

    Subject("体育実技 I", 1, "common_health"),
    Subject("体育実技 II", 1, "common_health"),
    Subject("栄養学", 2, "common_health"),
    Subject("健康学", 2, "common_health"),

    Subject("データサイエンス入門", 2, "common_univ"),
    Subject("統計学", 2, "common_univ"),
    Subject("多文化共生論", 2, "common_univ"),
    Subject("地域文化論", 2, "common_univ"),
    Subject("地域資源論", 2, "common_univ"),
    Subject("行政学入門", 2, "common_univ"),
    Subject("社会保障論", 2, "common_univ"),
    Subject("情報リテラシー", 2, "common_univ"),
    Subject("国際関係論", 2, "common_univ"),
    Subject("持続可能な社会論", 2, "common_univ"),
    Subject("社会福祉論", 2, "common_univ"),
    Subject("社会調査論", 2, "common_univ"),
    Subject("地域防災論", 2, "common_univ"),
    Subject("経営情報システム論", 2, "common_univ"),
    Subject("観光情報学", 2, "common_univ"),

    # === 【専門教育科目】 ===
    Subject("地域情報PBL I", 1, "pbl"),
    Subject("地域情報PBL II", 1, "pbl"),
    Subject("地域情報PBL III", 1, "pbl"),
    Subject("地域情報PBL IV", 1, "pbl"),
    Subject("地域情報プロジェクト I", 2, "pbl", required=True),
    Subject("地域情報プロジェクト II", 2, "pbl", required=True),
    Subject("地域情報プロジェクト III", 4, "pbl", required=True),
    Subject("地域情報プロジェクト IV", 4, "pbl", required=True),
    Subject("インターンシップ実習 I", 1, "pbl"),
    Subject("インターンシップ実習 II", 1, "pbl"),

    Subject("コンピュータプログラミング I", 2, "basic_comp", required=True),
    Subject("コンピュータプログラミング II", 2, "basic_comp", required=True),
    Subject("情報学アカデミックスキル", 2, "basic_comp", required=True),
    Subject("計算機アーキテクチャ", 2, "basic_other"),
    Subject("コンピュータプログラミング演習 I", 1, "basic_comp", required=True),
    Subject("コンピュータプログラミング演習 II", 1, "basic_comp", required=True),
    Subject("IT実習A", 2, "basic_other", required=True),
    Subject("IT実習B", 2, "basic_other", required=True),
    Subject("アルゴリズム論", 2, "basic_other"),
    
    Subject("微分積分 I", 2, "basic_math_star", is_star=True),
    Subject("微分積分 II", 2, "basic_math_star", is_star=True),
    Subject("線形代数 I", 2, "basic_math_star", is_star=True),
    Subject("線形代数 II", 2, "basic_math_star", is_star=True),
    Subject("数学演習 I", 1, "basic_math_star", is_star=True),
    Subject("数学演習 II", 1, "basic_math_star", is_star=True),

    # トラック1: データサイエンス
    Subject("データ可視化", 2, "ds_prac"),
    Subject("計測工学", 2, "ds_prac"),
    Subject("基礎データ解析", 2, "ds_prac"),
    Subject("シミュレーション工学", 2, "ds_prac"),
    Subject("確率統計", 2, "ds_found"),
    Subject("線形計画法", 2, "ds_found"),
    Subject("画像情報処理", 2, "ds_found"),
    Subject("応用画像処理", 2, "ds_found"),
    Subject("微分方程式・フーリエ解析", 2, "ds_theory"),
    Subject("離散数学", 2, "ds_theory"),
    Subject("機械学習", 2, "ds_theory"),
    Subject("制御工学", 2, "ds_theory"),

    # トラック2: ICT
    Subject("情報ネットワーク", 2, "ict_prac"),
    Subject("地理情報システム", 2, "ict_prac"),
    Subject("情報セキュリティ", 2, "ict_prac"),
    Subject("組込みシステム", 2, "ict_prac"),
    Subject("データベースシステム", 2, "ict_found"),
    Subject("ソフトウェア工学", 2, "ict_found"),
    Subject("オペレーティングシステム", 2, "ict_found"),
    Subject("プログラミング言語処理系", 2, "ict_found"),
    Subject("論理設計", 2, "ict_theory"),
    Subject("情報符号理論", 2, "ict_theory"),
    Subject("計算理論", 2, "ict_theory"),
    Subject("数値解析", 2, "ict_theory"),

    # トラック3: 人間・社会情報
    Subject("エンタテインメント情報学", 2, "human_prac"),
    Subject("メディア情報学", 2, "human_prac"),
    Subject("サービスエンジニアリング", 2, "human_prac"),
    Subject("ゲーム情報学", 2, "human_prac"),
    Subject("ディープラーニング", 2, "human_found"),
    Subject("ヒューマンインタフェース", 2, "human_found"),
    Subject("コンピュータグラフィックス", 2, "human_found"),
    Subject("音情報処理", 2, "human_found"),
    Subject("多変量解析", 2, "human_theory"),
    Subject("信号情報処理", 2, "human_theory"),
    Subject("パターン認識", 2, "human_theory"),
    Subject("自然言語処理", 2, "human_theory"),

    # その他
    Subject("単位互換科目 I", 1, "other_exchange"),
    Subject("単位互換科目 II", 2, "other_exchange"),
    Subject("単位互換科目 III", 2, "other_exchange"),
    Subject("単位互換科目 IV", 1, "other_exchange"),
    Subject("単位互換科目 V", 2, "other_exchange"),
    Subject("単位互換科目 VI", 4, "other_exchange"),
    
    Subject("地域協働論", 2, "other_dept"),
    Subject("教育行政論", 2, "other_dept"),
    Subject("国際フィールドワーク", 2, "other_dept"),
    Subject("ソーシャルデザイン", 2, "other_dept"),
    Subject("災害ツーリズム論", 2, "other_dept"),
]

# ---------------------------------------------------------
# 4. 保存・読み込みロジック
# ---------------------------------------------------------
def load_data():
    """JSONファイルから履修済み科目名のリストを読み込む"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def save_data(checked_names):
    """履修済み科目名のリストをJSONファイルに保存する"""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(checked_names, f, ensure_ascii=False, indent=4)
        st.toast(f"✅ 保存しました！ ({len(checked_names)}科目)", icon="💾")
    except Exception as e:
        st.error(f"保存に失敗しました: {e}")

# ---------------------------------------------------------
# 5. アプリケーションロジック
# ---------------------------------------------------------
def main():
    st.set_page_config(page_title="卒業要件チェックシート", layout="wide")
    
    # --- 初期化処理 ---
    # セッションステートにデータが未ロードならファイルから読み込む
    if "loaded_checked_items" not in st.session_state:
        st.session_state["loaded_checked_items"] = load_data()
        # 読み込んだデータに基づいて，各チェックボックスの初期状態(True/False)を設定
        for subj in SUBJECT_DATA:
            if subj.name in st.session_state["loaded_checked_items"]:
                st.session_state[subj.name] = True
    
    st.title("🎓 情報学科 卒業要件判定システム")
    st.markdown("履修科目にチェックを入れてください．サイドバーの「保存」ボタンで記録を残せます．")

    # タブ設定
    tab1, tab2, tab3, tab4 = st.tabs([
        "① 共通教育科目", 
        "② 専門基礎・PBL", 
        "③ 専門トラック",
        "④ その他・他学部"
    ])

    # ヘルパー関数: チェックボックスを描画し，リストに追加
    # keyを科目名にすることで session_state と自動連動させる
    selected_subjects = []
    
    def create_checkbox(subject_obj, label=None):
        if label is None:
            label = subject_obj.name
        
        # チェックボックスの状態は st.session_state[subject_obj.name] で管理される
        is_checked = st.checkbox(f"{label} ({subject_obj.credits})", key=subject_obj.name)
        if is_checked:
            selected_subjects.append(subject_obj)

    # -----------------------
    # ① 共通教育科目
    # -----------------------
    with tab1:
        st.subheader(f"共通教育科目 (目標: {COMMON_REQ}単位)")
        
        # 外国語
        st.markdown("##### 🗣️ 外国語 (要6単位)")
        cols = st.columns(4)
        for i, s in enumerate([x for x in SUBJECT_DATA if x.category == "common_lang"]):
            with cols[i % 4]:
                label = f"●{s.name}" if s.required else s.name
                create_checkbox(s, label)

        st.divider()
        
        # 3分野
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("##### 📚 人文系 (要4単位)")
            for s in [x for x in SUBJECT_DATA if x.category == "common_human"]:
                create_checkbox(s)
        with c2:
            st.markdown("##### ⚖️ 社会系 (要4単位)")
            for s in [x for x in SUBJECT_DATA if x.category == "common_social"]:
                create_checkbox(s)
        with c3:
            st.markdown("##### 🧪 自然系 (要4単位)")
            for s in [x for x in SUBJECT_DATA if x.category == "common_natural"]:
                create_checkbox(s)

        st.divider()
        st.markdown("##### 🏃 保健体育・全学共通")
        cols = st.columns(4)
        for i, s in enumerate([x for x in SUBJECT_DATA if x.category in ["common_health", "common_univ"]]):
            with cols[i % 4]:
                create_checkbox(s)

    # -----------------------
    # ② 専門基礎・PBL
    # -----------------------
    with tab2:
        c_pbl, c_basic = st.columns(2)
        
        with c_pbl:
            st.subheader("PBL科目")
            for s in [x for x in SUBJECT_DATA if x.category == "pbl"]:
                label = f"●{s.name}" if s.required else s.name
                create_checkbox(s, label)
        
        with c_basic:
            st.subheader("情報専門基礎")
            st.markdown("**【●】=必修, 【★】=数学選択(4単位以上)**")
            
            st.markdown("###### プログラミング・その他")
            for s in [x for x in SUBJECT_DATA if x.category in ["basic_comp", "basic_other"]]:
                label = f"●{s.name}" if s.required else s.name
                create_checkbox(s, label)
            
            st.markdown("###### ★数学科目 (要4単位)")
            for s in [x for x in SUBJECT_DATA if x.category == "basic_math_star"]:
                create_checkbox(s, f"★{s.name}")

    # -----------------------
    # ③ 専門トラック
    # -----------------------
    with tab3:
        st.info("専門科目群は、3つのトラックのうち「どれか1つ」で、**実践系・基盤系・理論系からそれぞれ4単位以上**を取得する必要があります．")
        col_ds, col_ict, col_human = st.columns(3)

        def render_track(col, title, prefix):
            with col:
                st.markdown(f"### {title}")
                st.markdown("#### 実践系")
                for s in [x for x in SUBJECT_DATA if x.category == f"{prefix}_prac"]:
                    create_checkbox(s)
                st.markdown("#### 基盤系")
                for s in [x for x in SUBJECT_DATA if x.category == f"{prefix}_found"]:
                    create_checkbox(s)
                st.markdown("#### 理論系")
                for s in [x for x in SUBJECT_DATA if x.category == f"{prefix}_theory"]:
                    create_checkbox(s)

        render_track(col_ds, "📈 データサイエンス", "ds")
        render_track(col_ict, "💻 ICT", "ict")
        render_track(col_human, "🎨 人間・社会情報", "human")

    # -----------------------
    # ④ その他・他学部
    # -----------------------
    with tab4:
        st.subheader("その他科目")
        st.write("この科目を含む全科目の中から6単位必要．")
        col_ex, col_dep = st.columns(2)
        with col_ex:
            st.markdown("##### 単位互換科目")
            for s in [x for x in SUBJECT_DATA if x.category == "other_exchange"]:
                create_checkbox(s)
        with col_dep:
            st.markdown("##### 他学部・他学科科目")
            for s in [x for x in SUBJECT_DATA if x.category == "other_dept"]:
                create_checkbox(s)

    # ---------------------------------------------------------
    # 集計ロジック (変更なし)
    # ---------------------------------------------------------
    total_credits = sum(s.credits for s in selected_subjects)
    
    def calc_sum(cat_prefix):
        return sum(s.credits for s in selected_subjects if s.category.startswith(cat_prefix))
    
    common_credits = calc_sum("common")
    specialized_total = sum(s.credits for s in selected_subjects if not s.category.startswith("common") and not s.category.startswith("other"))
    
    c_lang = sum(s.credits for s in selected_subjects if s.category == "common_lang")
    c_human = sum(s.credits for s in selected_subjects if s.category == "common_human")
    c_social = sum(s.credits for s in selected_subjects if s.category == "common_social")
    c_natural = sum(s.credits for s in selected_subjects if s.category == "common_natural")

    math_star_credits = sum(s.credits for s in selected_subjects if s.category == "basic_math_star")
    is_math_cleared = math_star_credits >= 4

    def check_track_cleared(prefix):
        prac = sum(s.credits for s in selected_subjects if s.category == f"{prefix}_prac")
        found = sum(s.credits for s in selected_subjects if s.category == f"{prefix}_found")
        theory = sum(s.credits for s in selected_subjects if s.category == f"{prefix}_theory")
        is_cleared = (prac >= 4) and (found >= 4) and (theory >= 4)
        return is_cleared, prac, found, theory

    ds_ok, ds_p, ds_f, ds_t = check_track_cleared("ds")
    ict_ok, ict_p, ict_f, ict_t = check_track_cleared("ict")
    human_ok, human_p, human_f, human_t = check_track_cleared("human")
    any_track_cleared = ds_ok or ict_ok or human_ok
    
    if ds_ok: display_track, d_p, d_f, d_t = "データサイエンス", ds_p, ds_f, ds_t
    elif ict_ok: display_track, d_p, d_f, d_t = "ICT", ict_p, ict_f, ict_t
    elif human_ok: display_track, d_p, d_f, d_t = "人間・社会情報", human_p, human_f, human_t
    else:
        sums = {
            "データサイエンス": ds_p+ds_f+ds_t,
            "ICT": ict_p+ict_f+ict_t,
            "人間・社会情報": human_p+human_f+human_t
        }
        display_track = max(sums, key=sums.get)
        if display_track == "データサイエンス": d_p, d_f, d_t = ds_p, ds_f, ds_t
        elif display_track == "ICT": d_p, d_f, d_t = ict_p, ict_f, ict_t
        else: d_p, d_f, d_t = human_p, human_f, human_t

    missing_required = [s.name for s in SUBJECT_DATA if s.required and s not in selected_subjects]

    # ---------------------------------------------------------
    # サイドバー: 保存機能とレポート
    # ---------------------------------------------------------
    st.sidebar.title("卒業要件チェッカー")
    
    # --- 保存ボタン ---
    st.sidebar.markdown("### 💾 データ保存")
    if st.sidebar.button("現状を保存する", type="primary"):
        # 選択されている科目の名前リストを作成して保存
        current_checked = [s.name for s in selected_subjects]
        save_data(current_checked)

    # --- レポート ---
    st.sidebar.markdown("---")
    st.sidebar.header("📊 判定結果")
    st.sidebar.metric("総取得単位", f"{total_credits} / {GRADUATION_REQ}", delta=total_credits - GRADUATION_REQ)
    if total_credits >= GRADUATION_REQ:
        st.sidebar.success("総単位数クリア！")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**① 共通教育 ({common_credits}/{COMMON_REQ})**")
    def status_icon(cond): return "✅" if cond else "⚠️"
    st.sidebar.write(f"{status_icon(c_lang >= 6)} 外国語: {c_lang}/6")
    st.sidebar.write(f"{status_icon(c_human >= 4)} 人文系: {c_human}/4")
    st.sidebar.write(f"{status_icon(c_social >= 4)} 社会系: {c_social}/4")
    st.sidebar.write(f"{status_icon(c_natural >= 4)} 自然系: {c_natural}/4")

    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**② 専門教育 ({specialized_total}/{SPECIALIZED_REQ})**")
    st.sidebar.write(f"{status_icon(is_math_cleared)} 数学★選択: {math_star_credits}/4")

    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**③ トラック判定**\n(基準: {display_track})")
    st.sidebar.write(f"{status_icon(d_p >= 4)} 実践系: {d_p}/4")
    st.sidebar.write(f"{status_icon(d_f >= 4)} 基盤系: {d_f}/4")
    st.sidebar.write(f"{status_icon(d_t >= 4)} 理論系: {d_t}/4")
    if any_track_cleared: st.sidebar.success("トラック要件クリア")

    st.sidebar.markdown("---")
    is_grad_ready = (total_credits >= GRADUATION_REQ) and \
                    (common_credits >= COMMON_REQ) and \
                    any_track_cleared and \
                    is_math_cleared and \
                    (len(missing_required) == 0)

    if is_grad_ready:
        st.sidebar.success("🎊 **卒業要件 達成見込み！**")
        st.balloons()
    else:
        if missing_required:
            with st.expander("🚨 未修得の必修科目"):
                for m in missing_required: st.write(f"・{m}")

if __name__ == "__main__":
    main()