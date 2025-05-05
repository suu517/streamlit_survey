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
    
    所要時間は約10分です。最後までご回答いただけますようお願いいたします。
    """)
    
    if st.button("アンケートを開始する", key="start_survey"):
        st.session_state.current_page = 2
        st.experimental_rerun()

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
                st.experimental_rerun()

# 総合評価ページ
def show_overall_evaluation():
    st.title("総合評価")
    
    with st.form("overall_evaluation_form"):
        st.markdown('<div class="scale-description">1: 非常に不満 / 2: 不満 / 3: どちらでもない / 4: 満足 / 5: 非常に満足</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            nps = st.slider(
                "この会社を友人や知人に勧める可能性はどのくらいですか？（NPS）",
                min_value=0,
                max_value=10,
                value=7,
                step=1,
                format="%d",
                key="nps",
                help="0（全く勧めない）から10（強く勧める）の間で評価してください",
                label_visibility="visible"
            )
            
            overall_satisfaction = st.slider(
                "総合的な満足度",
                min_value=1,
                max_value=5,
                value=3,
                step=1,
                format="%d",
                key="overall_satisfaction",
                help="会社全体に対する満足度を評価してください",
                label_visibility="visible"
            )
        
        with col2:
            sense_of_achievement = st.slider(
                "活躍度合い（自分の能力を発揮できているか）",
                min_value=1,
                max_value=5,
                value=3,
                step=1,
                format="%d",
                key="sense_of_achievement",
                help="自分の能力や才能を発揮できているかを評価してください",
                label_visibility="visible"
            )
            
            intention_to_stay = st.slider(
                "勤続意向（今後もこの会社で働き続けたいか）",
                min_value=1,
                max_value=5,
                value=3,
                step=1,
                format="%d",
                key="intention_to_stay",
                help="今後もこの会社で働き続けたいと思うかを評価してください",
                label_visibility="visible"
            )
        
        submitted = st.form_submit_button("次へ")
        
        if submitted:
            # 前のページの回答と結合
            st.session_state.temp_response.update({
                "NPS": nps,
                "総合満足度": overall_satisfaction,
                "活躍度合い": sense_of_achievement,
                "勤続意向": intention_to_stay
            })
            
            # 次のページへ
            st.session_state.current_page = 4
            st.experimental_rerun()

# 勤務・仕事に関する評価ページ
def show_work_evaluation():
    st.title("勤務・仕事に関する評価")
    
    with st.form("work_evaluation_form"):
        st.markdown('<div class="scale-description">1: 非常に不満 / 2: 不満 / 3: どちらでもない / 4: 満足 / 5: 非常に満足</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            work_time = st.slider(
                "勤務時間",
                min_value=1,
                max_value=5,
                value=3,
                step=1,
                format="%d",
                key="work_time",
                help="勤務時間の長さや柔軟性に対する満足度を評価してください",
                label_visibility="visible"
            )
            
            workload = st.slider(
                "仕事量",
                min_value=1,
                max_value=5,
                value=3,
                step=1,
                format="%d",
                key="workload",
                help="担当している仕事の量に対する満足度を評価してください",
                label_visibility="visible"
            )
            
            work_content = st.slider(
                "仕事内容",
                min_value=1,
                max_value=5,
                value=3,
                step=1,
                format="%d",
                key="work_content",
                help="担当している仕事の内容に対する満足度を評価してください",
                label_visibility="visible"
            )
        
        with col2:
            holidays = st.slider(
                "休日休暇",
                min_value=1,
                max_value=5,
                value=3,
                step=1,
                format="%d",
                key="holidays",
                help="休日や休暇の取得しやすさに対する満足度を評価してください",
                label_visibility="visible"
            )
            
            work_style = st.slider(
                "勤務体系",
                min_value=1,
                max_value=5,
                value=3,
                step=1,
                format="%d",
                key="work_style",
                help="勤務体系（フレックス、リモートワークなど）に対する満足度を評価してください",
                label_visibility="visible"
            )
            
            goals = st.slider(
                "目標・ノルマ",
                min_value=1,
                max_value=5,
                value=3,
                step=1,
                format="%d",
                key="goals",
                help="設定されている目標やノルマの適切さに対する満足度を評価してください",
                label_visibility="visible"
            )
        
        submitted = st.form_submit_button("次へ")
        
        if submitted:
            # 前のページの回答と結合
            st.session_state.temp_response.update({
                "勤務時間": work_time,
                "仕事量": workload,
                "仕事内容": work_content,
                "休日休暇": holidays,
                "勤務体系": work_style,
                "目標・ノルマ": goals
            })
            
            # 次のページへ
            st.session_state.current_page = 5
            st.experimental_rerun()

# キャリア・成長に関する評価ページ
def show_career_evaluation():
    st.title("キャリア・成長に関する評価")
    
    with st.form("career_evaluation_form"):
        st.markdown('<div class="scale-description">1: 非常に不満 / 2: 不満 / 3: どちらでもない / 4: 満足 / 5: 非常に満足</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            promotion = st.slider(
                "昇給昇格",
                min_value=1,
                max_value=5,
                value=3,
                step=1,
                format="%d",
                key="promotion",
                help="昇給や昇格の機会や基準に対する満足度を評価してください",
                label_visibility="visible"
            )
            
            growth = st.slider(
                "成長実感",
                min_value=1,
                max_value=5,
                value=3,
                step=1,
                format="%d",
                key="growth",
                help="自身の成長を実感できているかを評価してください",
                label_visibility="visible"
            )
        
        with col2:
            future_career = st.slider(
                "将来キャリア",
                min_value=1,
                max_value=5,
                value=3,
                step=1,
                format="%d",
                key="future_career",
                help="将来のキャリアパスの明確さや魅力に対する満足度を評価してください",
                label_visibility="visible"
            )
            
            education = st.slider(
                "教育体制",
                min_value=1,
                max_value=5,
                value=3,
                step=1,
                format="%d",
                key="education",
                help="社内の教育・研修制度に対する満足度を評価してください",
                label_visibility="visible"
            )
        
        submitted = st.form_submit_button("次へ")
        
        if submitted:
            # 前のページの回答と結合
            st.session_state.temp_response.update({
                "昇給昇格": promotion,
                "成長実感": growth,
                "将来キャリア": future_career,
                "教育体制": education
            })
            
            # 次のページへ
            st.session_state.current_page = 6
            st.experimental_rerun()

# 環境・人間関係に関する評価ページ
def show_environment_evaluation():
    st.title("環境・人間関係に関する評価")
    
    with st.form("environment_evaluation_form"):
        st.markdown('<div class="scale-description">1: 非常に不満 / 2: 不満 / 3: どちらでもない / 4: 満足 / 5: 非常に満足</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            relationship = st.slider(
                "人間関係",
                min_value=1,
                max_value=5,
                value=3,
                step=1,
                format="%d",
                key="relationship",
                help="職場の人間関係に対する満足度を評価してください",
                label_visibility="visible"
            )
            
            work_environment = st.slider(
                "働く環境",
                min_value=1,
                max_value=5,
                value=3,
                step=1,
                format="%d",
                key="work_environment",
                help="オフィス環境や設備に対する満足度を評価してください",
                label_visibility="visible"
            )
        
        with col2:
            culture = st.slider(
                "文化・社風",
                min_value=1,
                max_value=5,
                value=3,
                step=1,
                format="%d",
                key="culture",
                help="会社の文化や社風に対する満足度を評価してください",
                label_visibility="visible"
            )
            
            women_friendly = st.slider(
                "女性の働きやすさ",
                min_value=1,
                max_value=5,
                value=3,
                step=1,
                format="%d",
                key="women_friendly",
                help="女性が働きやすい環境かどうかを評価してください",
                label_visibility="visible"
            )
        
        submitted = st.form_submit_button("次へ")
        
        if submitted:
            # 前のページの回答と結合
            st.session_state.temp_response.update({
                "人間関係": relationship,
                "働く環境": work_environment,
                "文化・社風": culture,
                "女性の働きやすさ": women_friendly
            })
            
            # 次のページへ
            st.session_state.current_page = 7
            st.experimental_rerun()

# 会社・組織に関する評価ページ
def show_company_evaluation():
    st.title("会社・組織に関する評価")
    
    with st.form("company_evaluation_form"):
        st.markdown('<div class="scale-description">1: 非常に不満 / 2: 不満 / 3: どちらでもない / 4: 満足 / 5: 非常に満足</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            business_foundation = st.slider(
                "事業基盤",
                min_value=1,
                max_value=5,
                value=3,
                step=1,
                format="%d",
                key="business_foundation",
                help="会社の事業基盤の安定性に対する満足度を評価してください",
                label_visibility="visible"
            )
            
            vision_strategy = st.slider(
                "ビジョン・戦略",
                min_value=1,
                max_value=5,
                value=3,
                step=1,
                format="%d",
                key="vision_strategy",
                help="会社のビジョンや戦略に対する満足度を評価してください",
                label_visibility="visible"
            )
            
            business_content = st.slider(
                "事業内容",
                min_value=1,
                max_value=5,
                value=3,
                step=1,
                format="%d",
                key="business_content",
                help="会社の事業内容に対する満足度を評価してください",
                label_visibility="visible"
            )
        
        with col2:
            placement = st.slider(
                "社内配置",
                min_value=1,
                max_value=5,
                value=3,
                step=1,
                format="%d",
                key="placement",
                help="社内の配置や異動に対する満足度を評価してください",
                label_visibility="visible"
            )
            
            benefits = st.slider(
                "福利厚生",
                min_value=1,
                max_value=5,
                value=3,
                step=1,
                format="%d",
                key="benefits",
                help="福利厚生制度に対する満足度を評価してください",
                label_visibility="visible"
            )
            
            compliance = st.slider(
                "法令遵守",
                min_value=1,
                max_value=5,
                value=3,
                step=1,
                format="%d",
                key="compliance",
                help="会社のコンプライアンス体制に対する満足度を評価してください",
                label_visibility="visible"
            )
        
        submitted = st.form_submit_button("次へ")
        
        if submitted:
            # 前のページの回答と結合
            st.session_state.temp_response.update({
                "事業基盤": business_foundation,
                "ビジョン・戦略": vision_strategy,
                "事業内容": business_content,
                "社内配置": placement,
                "福利厚生": benefits,
                "法令遵守": compliance
            })
            
            # 次のページへ
            st.session_state.current_page = 8
            st.experimental_rerun()

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
            st.experimental_rerun()

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
            st.experimental_rerun()
    
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