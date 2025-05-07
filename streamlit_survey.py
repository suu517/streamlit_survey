import streamlit as st
import pandas as pd
from datetime import datetime
import os

# ページ設定
st.set_page_config(
    page_title="従業員満足度・期待度調査",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# セッション状態の初期化
if 'page' not in st.session_state:
    st.session_state.page = 'intro'
if 'responses' not in st.session_state:
    st.session_state.responses = []
if 'current_data' not in st.session_state:
    st.session_state.current_data = {}

# データファイルのパス
DATA_FILE = "employee_survey_data.csv"

# データファイルの読み込み
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame()

# データの保存
def save_data(data):
    if os.path.exists(DATA_FILE):
        existing_data = pd.read_csv(DATA_FILE)
        updated_data = pd.concat([existing_data, data], ignore_index=True)
        updated_data.to_csv(DATA_FILE, index=False)
    else:
        data.to_csv(DATA_FILE, index=False)

# 5段階評価のオプション
satisfaction_options = {
    1: "非常に不満",
    2: "不満",
    3: "どちらでもない",
    4: "満足",
    5: "非常に満足"
}

expectation_options = {
    1: "全く期待していない",
    2: "あまり期待していない",
    3: "どちらでもない",
    4: "やや期待している",
    5: "非常に期待している"
}

# NPS用の10段階評価のオプション
nps_options = {
    1: "全く勧めない",
    2: "2",
    3: "3",
    4: "4",
    5: "5",
    6: "6",
    7: "7",
    8: "8",
    9: "9",
    10: "積極的に勧める"
}

# 質問リスト
questions = {
    "C. 総合評価": {
        "総合評価": [
            "親しい家族や友人にどの程度自社を勧めたいのか（NPS）",
            "総合満足度",
            "この会社にどれぐらい長く勤めいたいと感じているのか",
            "自分は現在の会社もしくは部署でどれぐらい活躍できていると感じるのか"
        ]
    },
    "A. あなたの仕事について": {
        "勤務時間": [
            "現在の残業時間について、どのように感じていますか？",
            "残業代金について、どのように感じていますか？"
        ],
        "仕事量": [
            "現在の仕事量について、どのように感じていますか？",
            "現在の仕事による身体的な疲労度はどの程度ですか？",
            "現在の仕事による精神的な疲労度はどの程度ですか？"
        ],
        "仕事内容": [
            "今の仕事に誇りやプライドを感じますか？",
            "仕事における裁量の大きさについて、どのように感じていますか？",
            "今の仕事にやりがいを感じますか？",
            "今の仕事は社会に貢献していると感じますか？",
            "今の仕事を通じて成長を実感していますか？",
            "今の仕事で達成感を感じることはありますか？",
            "担当している仕事の規模の大きさをどのように感じていますか？",
            "今の仕事で自分の強みを発揮できていると感じますか？",
            "今の仕事を通じて専門的なスキルや知識を獲得できていると感じますか？",
            "今の仕事は汎用的なスキルが身につくと思いますか？",
            "今の仕事はあなたの将来のキャリアの方向性と合っていますか？"
        ],
        "休日休暇": [
            "現在の休日休暇の取得状況について、十分に取れていると感じますか？",
            "有給休暇は十分に利用できていますか？"
        ],
        "勤務体系": [
            "現在の働き方（リモートワーク、時短勤務、シフト制など）について、どのように感じていますか？"
        ],
        "昇給昇格": [
            "昇給や昇格のスピード感について、どのように感じていますか？",
            "仕事の内容に対して、しっかりと評価されていると感じますか？",
            "評価制度や体制は透明性・明確性があると思いますか？"
        ],
        "人間関係": [
            "現在の職場の人間関係は良好だと思いますか？",
            "これまでにセクハラやパワハラと感じたことはありますか？"
        ],
        "働く外的環境（場所）": [
            "現在の勤務地はあなたにとって適切な距離だと感じますか？",
            "働いているオフィスや自宅の環境は十分に整っていると感じますか？"
        ],
        "成長実感": [
            "仕事を通じて成長を実感していますか？",
            "知識やスキルを獲得できていると感じますか？",
            "得た知識や経験を職場で発揮できていると感じますか？"
        ],
        "目標やノルマ": [
            "現在の目標やノルマは達成可能だと思いますか？"
        ],
        "将来のキャリア": [
            "将来のキャリアパスについて、ロールモデルとなるような人はいますか？",
            "会社はあなたの将来のキャリアパスをしっかりと設計してくれていると感じますか？"
        ]
    },
    "B. あなたの会社について": {
        "会社の事業基盤": [
            "会社の事業基盤について、安心感を持つことができますか？",
            "会社のブランド力について、どの程度感じますか？"
        ],
        "会社のビジョン・戦略・戦術などの将来性": [
            "会社のビジョンや将来性に対して、期待や信頼を持つことができますか？",
            "会社の現状の経営戦略や戦術について、信頼・期待を持つことができますか？"
        ],
        "会社の事業内容": [
            "会社の事業内容は社会の役に立っている、または貢献していると感じますか？",
            "会社の事業以外の取り組みで、社会の役に立っている、または貢献していると感じますか？",
            "会社の事業内容は同業他社と比較してどの程度優位性があると感じますか？",
            "会社の事業内容は同業他社と比較してどの程度独自性があると感じますか？",
            "会社の事業内容は同業他社と比較してどの程度革新性（イノベーション性）があると感じますか？"
        ],
        "会社の社内配置": [
            "会社の転勤体制はあなたの希望に沿ったものだと感じますか？",
            "会社の異動体制（自己公募制度など）はあなたの希望に沿ったものだと感じますか？"
        ],
        "会社の文化・社風": [
            "会社の社風や文化はあなたの価値観や考え方と共感できますか？",
            "会社の風通しの良さについて、どの程度感じますか？",
            "社内で教え合ったり、学び合ったりする文化や風土があると感じますか？"
        ],
        "会社の福利厚生": [
            "会社の福利厚生について、あなたの満足度を教えてください。"
        ],
        "会社の教育体制": [
            "会社の教育研修制度は充実していると感じますか？"
        ],
        "会社の女性の働きやすさ": [
            "社内の女性の働きやすさについて、どの程度感じますか？（男性の方もご意見をお聞かせください）"
        ],
        "会社の法令遵守な体制": [
            "社内の法令遵守の体制について、どの程度感じますか？"
        ]
    }
}

# イントロページ
def show_intro():
    st.title("従業員満足度・期待度調査")
    st.markdown("""
    このアンケートは、従業員の皆様の満足度と期待度を調査し、より良い職場環境づくりに役立てることを目的としています。
    
    各質問について、**現在の満足度**と**今後の期待度**の両方をお答えいただきます。
    回答は匿名で処理され、個人が特定されることはありません。
    
    アンケートの所要時間は約15分です。ご協力をお願いいたします。
    """)
    
    # 基本情報入力
    st.header("基本情報")
    
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.current_data['department'] = st.selectbox(
            "部署",
            ["営業部", "マーケティング部", "開発部", "人事部", "経理部", "総務部", "その他"]
        )
        st.session_state.current_data['position'] = st.selectbox(
            "役職",
            ["一般社員", "主任", "係長", "課長", "部長", "役員", "その他"]
        )
    
    with col2:
        st.session_state.current_data['years_of_service'] = st.slider(
            "勤続年数",
            min_value=0,
            max_value=40,
            value=3,
            step=1
        )
        st.session_state.current_data['age_group'] = st.selectbox(
            "年齢層",
            ["20代以下", "30代", "40代", "50代", "60代以上"]
        )
    
    st.session_state.current_data['gender'] = st.radio(
        "性別",
        ["男性", "女性", "その他", "回答しない"],
        horizontal=True
    )
    
    if st.button("アンケートを開始する", type="primary"):
        st.session_state.page = 'survey'
        st.experimental_rerun()

# アンケートページ
def show_survey():
    st.title("従業員満足度・期待度調査")
    
    # プログレスバーの表示
    progress_placeholder = st.empty()
    
    # フォーム作成
    with st.form("survey_form"):
        all_responses = {}
        all_comments = {}
        
        # 各セクションと質問を処理
        for section_idx, (section, categories) in enumerate(questions.items()):
            st.header(section)
            
            for category, qs in categories.items():
                st.subheader(category)
                
                for q_idx, question in enumerate(qs):
                    q_key = f"{section}_{category}_{q_idx}"
                    
                    st.markdown(f"**{question}**")
                    
                    # NPSの質問（10段階評価）
                    if "NPS" in question:
                        nps_value = st.radio(
                            f"NPS: {question}",
                            options=list(range(1, 11)),
                            format_func=lambda x: nps_options[x],
                            horizontal=True,
                            key=f"nps_{q_key}"
                        )
                        all_responses[f"nps_{q_key}"] = nps_value
                    else:
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown("**現在の満足度**")
                            satisfaction = st.radio(
                                f"満足度: {question}",
                                options=list(range(1, 6)),
                                format_func=lambda x: satisfaction_options[x],
                                horizontal=True,
                                key=f"sat_{q_key}",
                                label_visibility="collapsed"
                            )
                            all_responses[f"satisfaction_{q_key}"] = satisfaction
                        
                        with col2:
                            st.markdown("**今後の期待度**")
                            expectation = st.radio(
                                f"期待度: {question}",
                                options=list(range(1, 6)),
                                format_func=lambda x: expectation_options[x],
                                horizontal=True,
                                key=f"exp_{q_key}",
                                label_visibility="collapsed"
                            )
                            all_responses[f"expectation_{q_key}"] = expectation
                    
                    # コメント欄（オプション）- 文化・社風の具体的な記載項目は削除
                    if not ("文化・社風" in category and "共感できる" in question):
                        comment = st.text_area(
                            "コメント（任意）",
                            key=f"comment_{q_key}",
                            height=100
                        )
                        all_comments[f"comment_{q_key}"] = comment
                    
                    st.divider()
        
        # 特別な質問（有給休暇消化率）
        st.subheader("追加情報")
        paid_leave_usage = st.slider(
            "昨年度の有給休暇消化率を教えてください（%）",
            min_value=0,
            max_value=100,
            value=50,
            step=5
        )
        all_responses["paid_leave_usage"] = paid_leave_usage
        
        # 福利厚生に関する自由記述
        st.subheader("福利厚生について")
        valued_benefits = st.text_area(
            "特に評価している福利厚生があれば教えてください。",
            height=100
        )
        all_comments["valued_benefits"] = valued_benefits
        
        desired_benefits = st.text_area(
            "今後、どのような福利厚生があれば良いと感じますか？",
            height=100
        )
        all_comments["desired_benefits"] = desired_benefits
        
        # 送信ボタン
        submit_button = st.form_submit_button("回答を送信する", type="primary")
        
        if submit_button:
            # 基本情報と回答を結合
            response_data = {**st.session_state.current_data, **all_responses, **all_comments}
            response_data['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # データフレームに変換
            df = pd.DataFrame([response_data])
            
            # データを保存
            save_data(df)
            
            # セッション状態を更新
            st.session_state.responses.append(response_data)
            st.session_state.page = 'thank_you'
            st.experimental_rerun()

# サンキューページ
def show_thank_you():
    st.title("ご回答ありがとうございました")
    st.markdown("""
    アンケートへのご協力ありがとうございました。
    いただいた回答は、より良い職場環境づくりのために活用させていただきます。
    """)
    
    if st.button("新しいアンケートを開始", type="primary"):
        st.session_state.page = 'intro'
        st.experimental_rerun()

# メインアプリケーション
def main():
    # カスタムCSS
    st.markdown("""
    <style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .stRadio > div {
        flex-direction: row;
    }
    .stRadio label {
        margin-right: 15px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # ページ表示
    if st.session_state.page == 'intro':
        show_intro()
    elif st.session_state.page == 'survey':
        show_survey()
    elif st.session_state.page == 'thank_you':
        show_thank_you()

if __name__ == "__main__":
    main()
