import streamlit as st
from dataclasses import dataclass
from typing import List

# ---------------------------------------------------------
# 1. コンフィグレーション
# ---------------------------------------------------------
GRADUATION_REQ = 128      # 卒業要件総単位数
COMMON_REQ = 44           # 共通教育 必要単位数
SPECIALIZED_REQ = 78      # 専門教育 必要単位数

# ---------------------------------------------------------
# 2. データ構造
# ---------------------------------------------------------
@dataclass
class Subject:
    name: str
    credits: int
    category: str  
    # category定義:
    # common_lang, common_human, common_social, common_natural, common_health, common_univ
    # pbl, basic_comp, basic_math_star, basic_other
    # ds_prac, ds_found, ds_theory
    # ict_prac, ict_found, ict_theory
    # human_prac, human_found, human_theory
    # other_exchange, other_dept
    required: bool = False # ●印 (必修)
    is_star: bool = False  # ★印 (数学選択)

# ---------------------------------------------------------
# 3. 全科目データ (画像1〜4の完全統合)
# ---------------------------------------------------------
SUBJECT_DATA = [
    # === 【共通教育科目】 (画像1, 2) ===
    # 外国語 (要6単位)
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

    # 人文系 (要4単位)
    Subject("歴史学", 2, "common_human"),
    Subject("教育学", 2, "common_human"),
    Subject("哲学", 2, "common_human"),
    Subject("地理学", 2, "common_human"),
    Subject("論理学", 2, "common_human"),
    Subject("心理学", 2, "common_human"),

    # 社会系 (要4単位)
    Subject("日本国憲法", 2, "common_social"),
    Subject("法学概論", 2, "common_social"),
    Subject("人権論", 2, "common_social"),
    Subject("経営学概論", 2, "common_social"),
    Subject("社会学概論", 2, "common_social"),
    Subject("民法", 2, "common_social"),
    Subject("知的財産概論", 2, "common_social"),

    # 自然系 (要4単位)
    Subject("数学基礎", 2, "common_natural"),
    Subject("幾何学入門", 2, "common_natural"),
    Subject("生物学概論", 2, "common_natural"),
    Subject("計算機科学概論", 2, "common_natural"),
    Subject("人工知能概論", 2, "common_natural"),
    Subject("物理学概論", 2, "common_natural"),
    Subject("地球科学概論", 2, "common_natural"),

    # 保健体育
    Subject("体育実技 I", 1, "common_health"),
    Subject("体育実技 II", 1, "common_health"),
    Subject("栄養学", 2, "common_health"),
    Subject("健康学", 2, "common_health"),

    # 全学共通
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

    # === 【専門教育科目】 (画像3) ===
    # PBL
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

    # 情報専門基礎
    Subject("コンピュータプログラミング I", 2, "basic_comp", required=True),
    Subject("コンピュータプログラミング II", 2, "basic_comp", required=True),
    Subject("情報学アカデミックスキル", 2, "basic_comp", required=True),
    Subject("計算機アーキテクチャ", 2, "basic_other"),
    Subject("コンピュータプログラミング演習 I", 1, "basic_comp", required=True),
    Subject("コンピュータプログラミング演習 II", 1, "basic_comp", required=True),
    Subject("IT実習A", 2, "basic_other"),
    Subject("IT実習B", 2, "basic_other"),
    Subject("アルゴリズム論", 2, "basic_other"),
    
    # ★数学科目
    Subject("微分積分 I", 2, "basic_math_star", is_star=True),
    Subject("微分積分 II", 2, "basic_math_star", is_star=True),
    Subject("線形代数 I", 2, "basic_math_star", is_star=True),
    Subject("線形代数 II", 2, "basic_math_star", is_star=True),
    Subject("数学演習 I", 1, "basic_math_star", is_star=True),
    Subject("数学演習 II", 1, "basic_math_star", is_star=True),

    # トラック1: データサイエンス系 (DS)
    Subject("データ可視化", 2, "ds_prac"),
    Subject("計測工学", 2, "ds_prac"),
    Subject("基礎データ解析", 2, "ds_prac"),
    Subject("シミュレーション工学", 2, "ds_prac"),
    Subject("確率統計", 2, "ds_found"),
    Subject("線形計画法", 2, "ds_found"),
    Subject("画像情報処理", 2, "ds_found"),
    Subject("応用画像処理", 2, "ds_found"),
    Subject("微分方程式・フーリエ解析", 2, "ds_theory"),
    Subject("離散数学", 2, "ds_theory"), # ここでは理論系に配置(画像準拠)
    Subject("機械学習", 2, "ds_theory"),
    Subject("制御工学", 2, "ds_theory"),

    # トラック2: ICTトラック (ICT)
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

    # トラック3: 人間・社会情報学トラック (Human)
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

    # === 【その他科目】 (画像4) ===
    # 単位互換科目
    Subject("単位互換科目 I", 1, "other_exchange"),
    Subject("単位互換科目 II", 2, "other_exchange"),
    Subject("単位互換科目 III", 2, "other_exchange"),
    Subject("単位互換科目 IV", 1, "other_exchange"),
    Subject("単位互換科目 V", 2, "other_exchange"),
    Subject("単位互換科目 VI", 4, "other_exchange"),
    
    # 他学部・他学科
    Subject("地域協働論", 2, "other_dept"),
    Subject("教育行政論", 2, "other_dept"),
    Subject("国際フィールドワーク", 2, "other_dept"),
    Subject("ソーシャルデザイン", 2, "other_dept"),
    Subject("災害ツーリズム論", 2, "other_dept"),
]

# ---------------------------------------------------------
# 4. アプリケーションロジック
# ---------------------------------------------------------
def main():
    st.set_page_config(page_title="卒業要件チェックシート", layout="wide")
    st.title("🎓 福知山公立大学情報学部情報学科 卒業要件判定システム（2024～2025年度入学カリキュラム）")
    st.markdown("履修科目にチェックを入れてください．自動的に要件充足状況を計算します．")

    selected_subjects = []

    # タブ設定 (その他を追加)
    tab1, tab2, tab3, tab4 = st.tabs([
        "① 共通教育科目", 
        "② 専門基礎・PBL", 
        "③ 専門トラック",
        "④ その他・他学部"
    ])

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
                if st.checkbox(f"{label} ({s.credits})", key=s.name): selected_subjects.append(s)

        st.divider()
        
        # 3分野
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("##### 📚 人文系 (要4単位)")
            for s in [x for x in SUBJECT_DATA if x.category == "common_human"]:
                if st.checkbox(f"{s.name}", key=s.name): selected_subjects.append(s)
        with c2:
            st.markdown("##### ⚖️ 社会系 (要4単位)")
            for s in [x for x in SUBJECT_DATA if x.category == "common_social"]:
                if st.checkbox(f"{s.name}", key=s.name): selected_subjects.append(s)
        with c3:
            st.markdown("##### 🧪 自然系 (要4単位)")
            for s in [x for x in SUBJECT_DATA if x.category == "common_natural"]:
                if st.checkbox(f"{s.name}", key=s.name): selected_subjects.append(s)

        st.divider()
        st.markdown("##### 🏃 保健体育・全学共通")
        cols = st.columns(4)
        for i, s in enumerate([x for x in SUBJECT_DATA if x.category in ["common_health", "common_univ"]]):
            with cols[i % 4]:
                if st.checkbox(f"{s.name} ({s.credits})", key=s.name): selected_subjects.append(s)

    # -----------------------
    # ② 専門基礎・PBL
    # -----------------------
    with tab2:
        c_pbl, c_basic = st.columns(2)
        
        with c_pbl:
            st.subheader("PBL科目")
            for s in [x for x in SUBJECT_DATA if x.category == "pbl"]:
                label = f"●{s.name}" if s.required else s.name
                if st.checkbox(f"{label} ({s.credits})", key=s.name): selected_subjects.append(s)
        
        with c_basic:
            st.subheader("情報専門基礎")
            st.markdown("**【必】=必修, 【★】=数学選択(4単位以上)**")
            
            st.markdown("###### プログラミング・その他")
            for s in [x for x in SUBJECT_DATA if x.category in ["basic_comp", "basic_other"]]:
                label = f"●{s.name}" if s.required else s.name
                if st.checkbox(f"{label} ({s.credits})", key=s.name): selected_subjects.append(s)
            
            st.markdown("###### ★数学科目 (要4単位)")
            for s in [x for x in SUBJECT_DATA if x.category == "basic_math_star"]:
                if st.checkbox(f"★{s.name} ({s.credits})", key=s.name): selected_subjects.append(s)

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
                    if st.checkbox(f"{s.name}", key=s.name): selected_subjects.append(s)
                st.markdown("#### 基盤系")
                for s in [x for x in SUBJECT_DATA if x.category == f"{prefix}_found"]:
                    if st.checkbox(f"{s.name}", key=s.name): selected_subjects.append(s)
                st.markdown("#### 理論系")
                for s in [x for x in SUBJECT_DATA if x.category == f"{prefix}_theory"]:
                    if st.checkbox(f"{s.name}", key=s.name): selected_subjects.append(s)

        render_track(col_ds, "📈 データサイエンス", "ds")
        render_track(col_ict, "💻 ICT", "ict")
        render_track(col_human, "🎨 人間・社会情報", "human")

    # -----------------------
    # ④ その他・他学部
    # -----------------------
    with tab4:
        st.subheader("その他科目")
        st.write("これらは主に総単位数(128)に含まれます．")
        col_ex, col_dep = st.columns(2)
        with col_ex:
            st.markdown("##### 単位互換科目")
            for s in [x for x in SUBJECT_DATA if x.category == "other_exchange"]:
                if st.checkbox(f"{s.name} ({s.credits})", key=s.name): selected_subjects.append(s)
        with col_dep:
            st.markdown("##### 他学部・他学科科目")
            for s in [x for x in SUBJECT_DATA if x.category == "other_dept"]:
                if st.checkbox(f"{s.name} ({s.credits})", key=s.name): selected_subjects.append(s)

    # ---------------------------------------------------------
    # 集計ロジック
    # ---------------------------------------------------------
    # 1. カテゴリ別合計
    total_credits = sum(s.credits for s in selected_subjects)
    
    def calc_sum(cat_prefix):
        return sum(s.credits for s in selected_subjects if s.category.startswith(cat_prefix))
    
    common_credits = calc_sum("common")
    specialized_total = sum(s.credits for s in selected_subjects if not s.category.startswith("common") and not s.category.startswith("other"))
    
    # 共通教育 詳細要件
    c_lang = sum(s.credits for s in selected_subjects if s.category == "common_lang")
    c_human = sum(s.credits for s in selected_subjects if s.category == "common_human")
    c_social = sum(s.credits for s in selected_subjects if s.category == "common_social")
    c_natural = sum(s.credits for s in selected_subjects if s.category == "common_natural")

    # 専門基礎 数学★要件
    math_star_credits = sum(s.credits for s in selected_subjects if s.category == "basic_math_star")
    is_math_cleared = math_star_credits >= 4

    # トラック要件 (実践>=4 and 基盤>=4 and 理論>=4)
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
    
    # 表示用トラック選択
    if ds_ok: display_track, d_p, d_f, d_t = "データサイエンス", ds_p, ds_f, ds_t
    elif ict_ok: display_track, d_p, d_f, d_t = "ICT", ict_p, ict_f, ict_t
    elif human_ok: display_track, d_p, d_f, d_t = "人間・社会情報", human_p, human_f, human_t
    else:
        # 未達成時は合計が多いものを仮表示
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
    # サイドバー レポート
    # ---------------------------------------------------------
    st.sidebar.title("📊 判定結果")
    
    # 総単位
    st.sidebar.metric("総取得単位", f"{total_credits} / {GRADUATION_REQ}", delta=total_credits - GRADUATION_REQ)
    if total_credits >= GRADUATION_REQ:
        st.sidebar.success("総単位数クリア！")
    
    # 共通教育
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**① 共通教育 ({common_credits}/{COMMON_REQ})**")
    def status_icon(cond): return "✅" if cond else "⚠️"
    st.sidebar.write(f"{status_icon(c_lang >= 6)} 外国語: {c_lang}/6")
    st.sidebar.write(f"{status_icon(c_human >= 4)} 人文系: {c_human}/4")
    st.sidebar.write(f"{status_icon(c_social >= 4)} 社会系: {c_social}/4")
    st.sidebar.write(f"{status_icon(c_natural >= 4)} 自然系: {c_natural}/4")

    # 専門教育
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**② 専門教育 ({specialized_total}/{SPECIALIZED_REQ})**")
    st.sidebar.write(f"{status_icon(is_math_cleared)} 数学★選択: {math_star_credits}/4")

    # トラック詳細
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**③ トラック判定**\n(基準: {display_track})")
    st.sidebar.write(f"{status_icon(d_p >= 4)} 実践系: {d_p}/4")
    st.sidebar.write(f"{status_icon(d_f >= 4)} 基盤系: {d_f}/4")
    st.sidebar.write(f"{status_icon(d_t >= 4)} 理論系: {d_t}/4")
    if any_track_cleared: st.sidebar.success("トラック要件クリア")

    # 総合判定
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