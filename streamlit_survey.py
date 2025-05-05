import streamlit as st
import pandas as pd
import numpy as np
import io
from datetime import datetime

# ページ設定
st.set_page_config(
    page_title="採用力可視化アンケート",
    page_icon="📝",
    layout="wide",
)

# シンプルなカスタムCSS
st.markdown("""
<style>
    /* 全体のフォント設定 */
    html, body, [class*="css"] {
        font-family: 'Helvetica', 'Arial', sans-serif;
    }
    
    /* ヘッダーのスタイル */
    h1, h2, h3 {
        color: #1E293B;
        margin-bottom: 1rem;
    }
    
    /* セクションの区切り */
    .section {
        margin-bottom: 2rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid #eee;
    }
    
    /* 必須項目のマーク */
    .required {
        color: red;
        margin-left: 5px;
    }
    
    /* 送信ボタン */
    .submit-button {
        background-color: #1E293B;
        color: white;
        padding: 10px 20px;
        border-radius: 5px;
        border: none;
        cursor: pointer;
        font-size: 16px;
    }
    
    /* 評価スケールの説明 */
    .scale-description {
        font-size: 0.8rem;
        color: #6c757d;
        margin-bottom: 1rem;
    }
    
    /* 期待度と満足度のラベル */
    .expectation-label {
        color: #4285F4;
        font-weight: bold;
    }
    
    .satisfaction-label {
        color: #34A853;
        font-weight: bold;
    }
    
    /* 項目のカード */
    .item-card {
        background-color: #f8f9fa;
        border-radius: 5px;
        padding: 15px;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# セッション状態の初期化
if 'responses' not in st.session_state:
    st.session_state.responses = []

if 'current_page' not in st.session_state:
    st.session_state.current_page = 1

if 'form_submitted' not in st.session_state:
    st.session_state.form_submitted = False

# 回答をセッションに保存する関数
def save_response(response_data):
    # タイムスタンプを追加
    response_data['回答日時'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # セッションに保存
    st.session_state.responses.append(response_data)
    st.session_state.form_submitted = True

# 回答をExcelに変換する関数
def convert_to_excel():
    if not st.session_state.responses:
        return None
    
    # 回答をDataFrameに変換
    df = pd.DataFrame(st.session_state.responses)
    
    # Excelファイルとして保存
    excel_buffer = io.BytesIO()
    df.to_excel(excel_buffer, index=False, engine='openpyxl')
    excel_buffer.seek(0)
    
    return excel_buffer

# アンケートの説明ページ
def show_introduction():
    st.title("採用力可視化アンケート")
    
    st.markdown("""
    このアンケートは、当社の採用力と従業員満足度を向上させるために実施しています。
    皆様の率直なご意見をお聞かせください。回答は匿名で処理され、集計結果のみが分析に使用されます。
    
    ### アンケートの構成
    1. 基本情報
    2. 総合評価
    3. 勤務・仕事に関する評価
    4. キャリア・成長に関する評価
    5. 環境・人間関係に関する評価
    6. 会社・組織に関する評価
    7. 自由記述
    
    各項目について、「期待度」（あなたがどの程度重要と考えているか）と「満足度」（現状にどの程度満足しているか）の両方をお聞きします。
    
    所要時間は約10分です。最後までご回答いただけますようお願いいたします。
    """)
    
    if st.button("アンケートを開始する", key="start_survey"):
        st.session_state.current_page = 2
        st.rerun()

# 基本情報入力ページ
def show_basic_info():
    st.title("基本情報")
    
    with st.form("basic_info_form"):
        st.markdown('<span class="required">*</span> は必須項目です', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            department = st.selectbox(
                "部署 <span class='required'>*</span>",
                ["営業部", "マーケティング部", "エンジニアリング部", "人事部", "経理部", "その他"],
                index=None,
                placeholder="選択してください",
                key="department",
                help="所属している部署を選択してください",
                format_func=lambda x: x,
                label_visibility="visible",
                disabled=False,
                unsafe_allow_html=True
            )
            
            position = st.selectbox(
                "役職 <span class='required'>*</span>",
                ["マネージャー", "シニア", "ミッド", "ジュニア", "その他"],
                index=None,
                placeholder="選択してください",
                key="position",
                help="現在の役職を選択してください",
                format_func=lambda x: x,
                label_visibility="visible",
                disabled=False,
                unsafe_allow_html=True
            )
        
        with col2:
            age_group = st.selectbox(
                "年齢層 <span class='required'>*</span>",
                ["20代", "30代", "40代", "50代", "60代以上"],
                index=None,
                placeholder="選択してください",
                key="age_group",
                help="年齢層を選択してください",
                format_func=lambda x: x,
                label_visibility="visible",
                disabled=False,
                unsafe_allow_html=True
            )
            
            years_of_service = st.slider(
                "勤続年数 <span class='required'>*</span>",
                min_value=0.5,
                max_value=30.0,
                value=3.0,
                step=0.5,
                format="%.1f年",
                key="years_of_service",
                help="現在の会社での勤続年数を選択してください",
                label_visibility="visible",
                disabled=False,
                unsafe_allow_html=True
            )
        
        submitted = st.form_submit_button("次へ")
        
        if submitted:
            if not department or not position or not age_group:
                st.error("必須項目をすべて入力してください")
            else:
                # 回答を一時保存
                st.session_state.temp_response = {
                    "部署": department,
                    "役職": position,
                    "年齢層": age_group,
                    "勤続年数": years_of_service
                }
                
                # 次のページへ
                st.session_state.current_page = 3
                st.rerun()

# 総合評価ページ
def show_overall_evaluation():
    st.title("総合評価")
    
    with st.form("overall_evaluation_form"):
        st.markdown("""
        <div class="scale-description">
            <span class="expectation-label">期待度</span>: 1(全く重要でない) 〜 5(非常に重要)<br>
            <span class="satisfaction-label">満足度</span>: 1(非常に不満) 〜 5(非常に満足)
        </div>
        """, unsafe_allow_html=True)
        
        # NPS
        st.markdown('<div class="item-card">', unsafe_allow_html=True)
        st.subheader("会社の推奨度（NPS）")
        st.write("この会社を友人や知人に勧める可能性はどのくらいですか？")
        nps = st.slider(
            "推奨度",
            min_value=0,
            max_value=10,
            value=7,
            step=1,
            format="%d",
            key="nps",
            help="0（全く勧めない）から10（強く勧める）の間で評価してください"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 総合満足度
        st.markdown('<div class="item-card">', unsafe_allow_html=True)
        st.subheader("総合満足度")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<span class="expectation-label">期待度</span>: 会社全体に対してどの程度の期待を持っていますか？', unsafe_allow_html=True)
            overall_expectation = st.slider(
                "総合満足度の期待度",
                min_value=1,
                max_value=5,
                value=4,
                step=1,
                format="%d",
                key="overall_expectation"
            )
        
        with col2:
            st.markdown('<span class="satisfaction-label">満足度</span>: 現在の会社全体に対する満足度はどの程度ですか？', unsafe_allow_html=True)
            overall_satisfaction = st.slider(
                "総合満足度の満足度",
                min_value=1,
                max_value=5,
                value=3,
                step=1,
                format="%d",
                key="overall_satisfaction"
            )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 活躍度合い
        st.markdown('<div class="item-card">', unsafe_allow_html=True)
        st.subheader("活躍度合い")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<span class="expectation-label">期待度</span>: 自分の能力を発揮することをどの程度重要と考えていますか？', unsafe_allow_html=True)
            achievement_expectation = st.slider(
                "活躍度合いの期待度",
                min_value=1,
                max_value=5,
                value=4,
                step=1,
                format="%d",
                key="achievement_expectation"
            )
        
        with col2:
            st.markdown('<span class="satisfaction-label">満足度</span>: 現在、自分の能力をどの程度発揮できていると感じますか？', unsafe_allow_html=True)
            achievement_satisfaction = st.slider(
                "活躍度合いの満足度",
                min_value=1,
                max_value=5,
                value=3,
                step=1,
                format="%d",
                key="achievement_satisfaction"
            )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 勤続意向
        st.markdown('<div class="item-card">', unsafe_allow_html=True)
        st.subheader("勤続意向")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<span class="expectation-label">期待度</span>: 長く働き続けることをどの程度重要と考えていますか？', unsafe_allow_html=True)
            stay_expectation = st.slider(
                "勤続意向の期待度",
                min_value=1,
                max_value=5,
                value=4,
                step=1,
                format="%d",
                key="stay_expectation"
            )
        
        with col2:
            st.markdown('<span class="satisfaction-label">満足度</span>: 今後もこの会社で働き続けたいと思いますか？', unsafe_allow_html=True)
            stay_satisfaction = st.slider(
                "勤続意向の満足度",
                min_value=1,
                max_value=5,
                value=3,
                step=1,
                format="%d",
                key="stay_satisfaction"
            )
        st.markdown('</div>', unsafe_allow_html=True)
        
        submitted = st.form_submit_button("次へ")
        
        if submitted:
            # 前のページの回答と結合
            st.session_state.temp_response.update({
                "NPS": nps,
                "総合満足度_期待度": overall_expectation,
                "総合満足度_満足度": overall_satisfaction,
                "活躍度合い_期待度": achievement_expectation,
                "活躍度合い_満足度": achievement_satisfaction,
                "勤続意向_期待度": stay_expectation,
                "勤続意向_満足度": stay_satisfaction
            })
            
            # 次のページへ
            st.session_state.current_page = 4
            st.rerun()

# 勤務・仕事に関する評価ページ
def show_work_evaluation():
    st.title("勤務・仕事に関する評価")
    
    with st.form("work_evaluation_form"):
        st.markdown("""
        <div class="scale-description">
            <span class="expectation-label">期待度</span>: 1(全く重要でない) 〜 5(非常に重要)<br>
            <span class="satisfaction-label">満足度</span>: 1(非常に不満) 〜 5(非常に満足)
        </div>
        """, unsafe_allow_html=True)
        
        # 勤務時間
        st.markdown('<div class="item-card">', unsafe_allow_html=True)
        st.subheader("勤務時間")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<span class="expectation-label">期待度</span>: 勤務時間の柔軟性や適切さをどの程度重要と考えていますか？', unsafe_allow_html=True)
            work_time_expectation = st.slider(
                "勤務時間の期待度",
                min_value=1,
                max_value=5,
                value=4,
                step=1,
                format="%d",
                key="work_time_expectation"
            )
        
        with col2:
            st.markdown('<span class="satisfaction-label">満足度</span>: 現在の勤務時間に対する満足度はどの程度ですか？', unsafe_allow_html=True)
            work_time_satisfaction = st.slider(
                "勤務時間の満足度",
                min_value=1,
                max_value=5,
                value=3,
                step=1,
                format="%d",
                key="work_time_satisfaction"
            )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 仕事量
        st.markdown('<div class="item-card">', unsafe_allow_html=True)
        st.subheader("仕事量")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<span class="expectation-label">期待度</span>: 適切な仕事量をどの程度重要と考えていますか？', unsafe_allow_html=True)
            workload_expectation = st.slider(
                "仕事量の期待度",
                min_value=1,
                max_value=5,
                value=4,
                step=1,
                format="%d",
                key="workload_expectation"
            )
        
        with col2:
            st.markdown('<span class="satisfaction-label">満足度</span>: 現在の仕事量に対する満足度はどの程度ですか？', unsafe_allow_html=True)
            workload_satisfaction = st.slider(
                "仕事量の満足度",
                min_value=1,
                max_value=5,
                value=3,
                step=1,
                format="%d",
                key="workload_satisfaction"
            )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 仕事内容
        st.markdown('<div class="item-card">', unsafe_allow_html=True)
        st.subheader("仕事内容")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<span class="expectation-label">期待度</span>: やりがいのある仕事内容をどの程度重要と考えていますか？', unsafe_allow_html=True)
            work_content_expectation = st.slider(
                "仕事内容の期待度",
                min_value=1,
                max_value=5,
                value=4,
                step=1,
                format="%d",
                key="work_content_expectation"
            )
        
        with col2:
            st.markdown('<span class="satisfaction-label">満足度</span>: 現在の仕事内容に対する満足度はどの程度ですか？', unsafe_allow_html=True)
            work_content_satisfaction = st.slider(
                "仕事内容の満足度",
                min_value=1,
                max_value=5,
                value=3,
                step=1,
                format="%d",
                key="work_content_satisfaction"
            )
        st.markdown('</div>', unsafe_allow_html=True)
        
        submitted = st.form_submit_button("次へ")
        
        if submitted:
            # 前のページの回答と結合
            st.session_state.temp_response.update({
                "勤務時間_期待度": work_time_expectation,
                "勤務時間_満足度": work_time_satisfaction,
                "仕事量_期待度": workload_expectation,
                "仕事量_満足度": workload_satisfaction,
                "仕事内容_期待度": work_content_expectation,
                "仕事内容_満足度": work_content_satisfaction
            })
            
            # 次のページへ
            st.session_state.current_page = 5
            st.rerun()

# キャリア・成長に関する評価ページ
def show_career_evaluation():
    st.title("キャリア・成長に関する評価")
    
    with st.form("career_evaluation_form"):
        st.markdown("""
        <div class="scale-description">
            <span class="expectation-label">期待度</span>: 1(全く重要でない) 〜 5(非常に重要)<br>
            <span class="satisfaction-label">満足度</span>: 1(非常に不満) 〜 5(非常に満足)
        </div>
        """, unsafe_allow_html=True)
        
        # 昇給昇格
        st.markdown('<div class="item-card">', unsafe_allow_html=True)
        st.subheader("昇給昇格")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<span class="expectation-label">期待度</span>: 昇給や昇格の機会をどの程度重要と考えていますか？', unsafe_allow_html=True)
            promotion_expectation = st.slider(
                "昇給昇格の期待度",
                min_value=1,
                max_value=5,
                value=4,
                step=1,
                format="%d",
                key="promotion_expectation"
            )
        
        with col2:
            st.markdown('<span class="satisfaction-label">満足度</span>: 現在の昇給や昇格の機会に対する満足度はどの程度ですか？', unsafe_allow_html=True)
            promotion_satisfaction = st.slider(
                "昇給昇格の満足度",
                min_value=1,
                max_value=5,
                value=3,
                step=1,
                format="%d",
                key="promotion_satisfaction"
            )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 成長実感
        st.markdown('<div class="item-card">', unsafe_allow_html=True)
        st.subheader("成長実感")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<span class="expectation-label">期待度</span>: 自身の成長を実感できることをどの程度重要と考えていますか？', unsafe_allow_html=True)
            growth_expectation = st.slider(
                "成長実感の期待度",
                min_value=1,
                max_value=5,
                value=4,
                step=1,
                format="%d",
                key="growth_expectation"
            )
        
        with col2:
            st.markdown('<span class="satisfaction-label">満足度</span>: 現在、自身の成長をどの程度実感できていますか？', unsafe_allow_html=True)
            growth_satisfaction = st.slider(
                "成長実感の満足度",
                min_value=1,
                max_value=5,
                value=3,
                step=1,
                format="%d",
                key="growth_satisfaction"
            )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 将来キャリア
        st.markdown('<div class="item-card">', unsafe_allow_html=True)
        st.subheader("将来キャリア")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<span class="expectation-label">期待度</span>: 将来のキャリアパスが明確であることをどの程度重要と考えていますか？', unsafe_allow_html=True)
            career_expectation = st.slider(
                "将来キャリアの期待度",
                min_value=1,
                max_value=5,
                value=4,
                step=1,
                format="%d",
                key="career_expectation"
            )
        
        with col2:
            st.markdown('<span class="satisfaction-label">満足度</span>: 現在の将来キャリアの見通しに対する満足度はどの程度ですか？', unsafe_allow_html=True)
            career_satisfaction = st.slider(
                "将来キャリアの満足度",
                min_value=1,
                max_value=5,
                value=3,
                step=1,
                format="%d",
                key="career_satisfaction"
            )
        st.markdown('</div>', unsafe_allow_html=True)
        
        submitted = st.form_submit_button("次へ")
        
        if submitted:
            # 前のページの回答と結合
            st.session_state.temp_response.update({
                "昇給昇格_期待度": promotion_expectation,
                "昇給昇格_満足度": promotion_satisfaction,
                "成長実感_期待度": growth_expectation,
                "成長実感_満足度": growth_satisfaction,
                "将来キャリア_期待度": career_expectation,
                "将来キャリア_満足度": career_satisfaction
            })
            
            # 次のページへ
            st.session_state.current_page = 6
            st.rerun()

# 環境・人間関係に関する評価ページ
def show_environment_evaluation():
    st.title("環境・人間関係に関する評価")
    
    with st.form("environment_evaluation_form"):
        st.markdown("""
        <div class="scale-description">
            <span class="expectation-label">期待度</span>: 1(全く重要でない) 〜 5(非常に重要)<br>
            <span class="satisfaction-label">満足度</span>: 1(非常に不満) 〜 5(非常に満足)
        </div>
        """, unsafe_allow_html=True)
        
        # 人間関係
        st.markdown('<div class="item-card">', unsafe_allow_html=True)
        st.subheader("人間関係")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<span class="expectation-label">期待度</span>: 良好な職場の人間関係をどの程度重要と考えていますか？', unsafe_allow_html=True)
            relationship_expectation = st.slider(
                "人間関係の期待度",
                min_value=1,
                max_value=5,
                value=4,
                step=1,
                format="%d",
                key="relationship_expectation"
            )
        
        with col2:
            st.markdown('<span class="satisfaction-label">満足度</span>: 現在の職場の人間関係に対する満足度はどの程度ですか？', unsafe_allow_html=True)
            relationship_satisfaction = st.slider(
                "人間関係の満足度",
                min_value=1,
                max_value=5,
                value=3,
                step=1,
                format="%d",
                key="relationship_satisfaction"
            )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 働く環境
        st.markdown('<div class="item-card">', unsafe_allow_html=True)
        st.subheader("働く環境")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<span class="expectation-label">期待度</span>: 快適な職場環境をどの程度重要と考えていますか？', unsafe_allow_html=True)
            environment_expectation = st.slider(
                "働く環境の期待度",
                min_value=1,
                max_value=5,
                value=4,
                step=1,
                format="%d",
                key="environment_expectation"
            )
        
        with col2:
            st.markdown('<span class="satisfaction-label">満足度</span>: 現在の職場環境に対する満足度はどの程度ですか？', unsafe_allow_html=True)
            environment_satisfaction = st.slider(
                "働く環境の満足度",
                min_value=1,
                max_value=5,
                value=3,
                step=1,
                format="%d",
                key="environment_satisfaction"
            )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 文化・社風
        st.markdown('<div class="item-card">', unsafe_allow_html=True)
        st.subheader("文化・社風")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<span class="expectation-label">期待度</span>: 良い会社文化や社風をどの程度重要と考えていますか？', unsafe_allow_html=True)
            culture_expectation = st.slider(
                "文化・社風の期待度",
                min_value=1,
                max_value=5,
                value=4,
                step=1,
                format="%d",
                key="culture_expectation"
            )
        
        with col2:
            st.markdown('<span class="satisfaction-label">満足度</span>: 現在の会社文化や社風に対する満足度はどの程度ですか？', unsafe_allow_html=True)
            culture_satisfaction = st.slider(
                "文化・社風の満足度",
                min_value=1,
                max_value=5,
                value=3,
                step=1,
                format="%d",
                key="culture_satisfaction"
            )
        st.markdown('</div>', unsafe_allow_html=True)
        
        submitted = st.form_submit_button("次へ")
        
        if submitted:
            # 前のページの回答と結合
            st.session_state.temp_response.update({
                "人間関係_期待度": relationship_expectation,
                "人間関係_満足度": relationship_satisfaction,
                "働く環境_期待度": environment_expectation,
                "働く環境_満足度": environment_satisfaction,
                "文化・社風_期待度": culture_expectation,
                "文化・社風_満足度": culture_satisfaction
            })
            
            # 次のページへ
            st.session_state.current_page = 7
            st.rerun()

# 会社・組織に関する評価ページ
def show_company_evaluation():
    st.title("会社・組織に関する評価")
    
    with st.form("company_evaluation_form"):
        st.markdown("""
        <div class="scale-description">
            <span class="expectation-label">期待度</span>: 1(全く重要でない) 〜 5(非常に重要)<br>
            <span class="satisfaction-label">満足度</span>: 1(非常に不満) 〜 5(非常に満足)
        </div>
        """, unsafe_allow_html=True)
        
        # 事業基盤
        st.markdown('<div class="item-card">', unsafe_allow_html=True)
        st.subheader("事業基盤")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<span class="expectation-label">期待度</span>: 安定した事業基盤をどの程度重要と考えていますか？', unsafe_allow_html=True)
            business_foundation_expectation = st.slider(
                "事業基盤の期待度",
                min_value=1,
                max_value=5,
                value=4,
                step=1,
                format="%d",
                key="business_foundation_expectation"
            )
        
        with col2:
            st.markdown('<span class="satisfaction-label">満足度</span>: 現在の会社の事業基盤に対する満足度はどの程度ですか？', unsafe_allow_html=True)
            business_foundation_satisfaction = st.slider(
                "事業基盤の満足度",
                min_value=1,
                max_value=5,
                value=3,
                step=1,
                format="%d",
                key="business_foundation_satisfaction"
            )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # ビジョン・戦略
        st.markdown('<div class="item-card">', unsafe_allow_html=True)
        st.subheader("ビジョン・戦略")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<span class="expectation-label">期待度</span>: 明確なビジョンや戦略をどの程度重要と考えていますか？', unsafe_allow_html=True)
            vision_strategy_expectation = st.slider(
                "ビジョン・戦略の期待度",
                min_value=1,
                max_value=5,
                value=4,
                step=1,
                format="%d",
                key="vision_strategy_expectation"
            )
        
        with col2:
            st.markdown('<span class="satisfaction-label">満足度</span>: 現在の会社のビジョンや戦略に対する満足度はどの程度ですか？', unsafe_allow_html=True)
            vision_strategy_satisfaction = st.slider(
                "ビジョン・戦略の満足度",
                min_value=1,
                max_value=5,
                value=3,
                step=1,
                format="%d",
                key="vision_strategy_satisfaction"
            )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 福利厚生
        st.markdown('<div class="item-card">', unsafe_allow_html=True)
        st.subheader("福利厚生")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<span class="expectation-label">期待度</span>: 充実した福利厚生をどの程度重要と考えていますか？', unsafe_allow_html=True)
            benefits_expectation = st.slider(
                "福利厚生の期待度",
                min_value=1,
                max_value=5,
                value=4,
                step=1,
                format="%d",
                key="benefits_expectation"
            )
        
        with col2:
            st.markdown('<span class="satisfaction-label">満足度</span>: 現在の福利厚生に対する満足度はどの程度ですか？', unsafe_allow_html=True)
            benefits_satisfaction = st.slider(
                "福利厚生の満足度",
                min_value=1,
                max_value=5,
                value=3,
                step=1,
                format="%d",
                key="benefits_satisfaction"
            )
        st.markdown('</div>', unsafe_allow_html=True)
        
        submitted = st.form_submit_button("次へ")
        
        if submitted:
            # 前のページの回答と結合
            st.session_state.temp_response.update({
                "事業基盤_期待度": business_foundation_expectation,
                "事業基盤_満足度": business_foundation_satisfaction,
                "ビジョン・戦略_期待度": vision_strategy_expectation,
                "ビジョン・戦略_満足度": vision_strategy_satisfaction,
                "福利厚生_期待度": benefits_expectation,
                "福利厚生_満足度": benefits_satisfaction
            })
            
            # 次のページへ
            st.session_state.current_page = 8
            st.rerun()

# 自由記述ページ
def show_free_comment():
    st.title("自由記述")
    
    with st.form("free_comment_form"):
        st.write("以下の質問に自由にお答えください。回答は任意です。")
        
        strengths = st.text_area(
            "当社の強みや良い点は何だと思いますか？",
            height=100,
            key="strengths",
            help="会社の強みや良い点について自由にお書きください",
            label_visibility="visible"
        )
        
        weaknesses = st.text_area(
            "当社の弱みや改善すべき点は何だと思いますか？",
            height=100,
            key="weaknesses",
            help="会社の弱みや改善すべき点について自由にお書きください",
            label_visibility="visible"
        )
        
        suggestions = st.text_area(
            "会社をより良くするための提案があれば教えてください。",
            height=100,
            key="suggestions",
            help="会社をより良くするための提案を自由にお書きください",
            label_visibility="visible"
        )
        
        submitted = st.form_submit_button("送信")
        
        if submitted:
            # 前のページの回答と結合
            st.session_state.temp_response.update({
                "強み・良い点": strengths,
                "弱み・改善点": weaknesses,
                "提案": suggestions
            })
            
            # 回答を保存
            save_response(st.session_state.temp_response)
            
            # 完了ページへ
            st.session_state.current_page = 9
            st.rerun()

# 完了ページ
def show_completion():
    st.title("アンケート回答完了")
    
    st.success("アンケートへのご回答ありがとうございました。皆様のご意見は今後の改善に活かしてまいります。")
    
    # 管理者用のダウンロードボタン
    st.subheader("管理者用")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("新しいアンケートに回答する"):
            st.session_state.form_submitted = False
            st.session_state.current_page = 1
            st.rerun()
    
    with col2:
        excel_data = convert_to_excel()
        if excel_data:
            st.download_button(
                label="回答データをダウンロード",
                data=excel_data,
                file_name=f"recruitment_survey_responses_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    
    # 回答数の表示
    st.info(f"現在の回答数: {len(st.session_state.responses)}件")
    
    # 回答データのプレビュー（管理者向け）
    if st.checkbox("回答データを表示"):
        if st.session_state.responses:
            st.dataframe(pd.DataFrame(st.session_state.responses))
        else:
            st.write("回答データがありません。")

# メイン関数
def main():
    # 現在のページに応じて表示を切り替え
    if st.session_state.current_page == 1:
        show_introduction()
    elif st.session_state.current_page == 2:
        show_basic_info()
    elif st.session_state.current_page == 3:
        show_overall_evaluation()
    elif st.session_state.current_page == 4:
        show_work_evaluation()
    elif st.session_state.current_page == 5:
        show_career_evaluation()
    elif st.session_state.current_page == 6:
        show_environment_evaluation()
    elif st.session_state.current_page == 7:
        show_company_evaluation()
    elif st.session_state.current_page == 8:
        show_free_comment()
    elif st.session_state.current_page == 9:
        show_completion()

if __name__ == "__main__":
    main()
