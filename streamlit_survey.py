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
    st.session_state.responses = {}
if 'current_page' not in st.session_state:
    st.session_state.current_page = 1

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
        updated_data = pd.concat([existing_data, pd.DataFrame([data])], ignore_index=True)
        updated_data.to_csv(DATA_FILE, index=False)
    else:
        pd.DataFrame([data]).to_csv(DATA_FILE, index=False)

# 11段階評価のオプション（0-10）
rating_options_11 = {
    0: "0（全く当てはまらない）",
    1: "1",
    2: "2",
    3: "3",
    4: "4",
    5: "5（どちらとも言えない）",
    6: "6",
    7: "7",
    8: "8",
    9: "9",
    10: "10（非常に当てはまる）"
}

# 5段階評価のオプション
rating_options_5 = [
    "満足していない",
    "どちらかと言えば満足していない",
    "どちらとも言えない",
    "どちらかと言えば満足している",
    "満足している"
]

# 期待度の5段階評価のオプション
expectation_options_5 = [
    "期待していない",
    "どちらかと言えば期待していない",
    "どちらとも言えない",
    "どちらかと言えば期待している",
    "期待している"
]

# 活躍貢献度の5段階評価のオプション
contribution_options_5 = [
    "活躍貢献できていない",
    "どちらかと言えば活躍貢献できていない",
    "どちらとも言えない",
    "どちらかと言えば活躍貢献できていると感じる",
    "活躍貢献できていると感じる"
]

# デモグラフィック項目
demographic_questions = {
    "雇用形態": ["正社員", "契約社員", "パートアルバイト", "業務委託", "派遣", "その他"],
    "入社形態": ["新卒入社", "中途入社"],
    "年齢": None,  # 数値入力
    "事業部": ["営業部", "マーケティング部", "開発部", "人事部", "経理部", "総務部", "その他"],
    "職種": ["営業", "マーケティング", "エンジニア", "デザイナー", "人事", "経理", "総務", "その他"],
    "役職": ["一般社員", "主任", "係長", "課長", "部長", "役員", "その他"],
    "残業時間": None,  # 数値入力
    "有給休暇消化率": None,  # 数値入力
    "入社年": None,  # 数値入力
    "年収": None,  # 数値入力
}

# 評価項目
evaluation_questions = [
    {
        "question": "総合評価：自分の親しい友人や家族に対して、この会社への転職・就職をどの程度勧めたいと思いますか？",
        "type": "rating_11",
        "key": "nps"
    },
    {
        "question": "総合満足度：自社の現在の働く環境や条件、周りの人間関係なども含めあなたはどの程度満足されていますか？",
        "type": "rating_11",
        "key": "overall_satisfaction"
    },
    {
        "question": "あなたはこの会社でこれからも長く働きたいとどの程度思われますか",
        "type": "rating_11",
        "key": "intention_to_stay"
    },
    {
        "question": "現在の所属組織であなたはどの程度、活躍貢献できていると感じますか？あなたのお気持ちに最も近しいものをお選びください。",
        "type": "contribution_5",
        "key": "contribution"
    }
]

# 期待項目と満足項目のカテゴリと質問
expectation_satisfaction_categories = {
    "働き方・時間の柔軟性": {
        "勤務時間の適正": "自分に合った勤務時間で働ける",
        "休暇制度1": "休日休暇がちゃんと取れる",
        "休暇制度2": "有給休暇がちゃんと取れる",
        "勤務形態の柔軟性": "柔軟な勤務体系（リモートワーク、時短勤務、フレックス制など）のもとで働ける",
        "通勤負荷": "自宅から適切な距離で働ける",
        "異動・転勤の柔軟性1": "自身の希望が十分に考慮されるような転勤体制がある",
        "異動・転勤の柔軟性2": "自身の希望が十分に考慮されるような社内異動体制が整備されている"
    },
    "労働条件・待遇": {
        "残業・労働対価": "残業したらその分しっかり給与が支払われる",
        "業務量適正": "自分のキャパシティーに合った量の仕事で働ける",
        "身体的負荷": "仕事内容や量に対する身体的な負荷が少ない",
        "精神的負荷": "仕事内容や量に対する精神的な負荷が少ない",
        "福利厚生": "充実した福利厚生がある"
    },
    "評価制度・成長": {
        "評価制度": "自身の行った仕事が正当に評価される",
        "昇進・昇給": "成果に応じて早期の昇給・昇格が望める",
        "目標設定": "達成可能性が見込まれる目標やノルマのもとで働く"
    },
    "キャリア・スキル形成": {
        "スキル獲得（専門）": "専門的なスキルや技術・知識や経験を獲得できる",
        "スキル獲得（汎用）": "汎用的なスキル（コミュニケーション能力や論理的思考力など）や技術・知識・経験を獲得できる",
        "教育制度・研修制度": "整った教育体制がある",
        "キャリアパス": "自分に合った将来のキャリアパスをしっかり設計してくれる",
        "キャリアの方向性": "将来自分のなりたいもしくはやりたい方向性とマッチした仕事を任せてもらえる",
        "ロールモデル": "身近にロールモデルとなるような人がいる"
    },
    "仕事内容・やりがい": {
        "誇り・社会貢献1": "誇りやプライドを持てるような仕事内容を提供してくれる",
        "誇り・社会貢献2": "社会に対して貢献実感を持てるような仕事を任せてもらえる",
        "やりがい・裁量1": "やりがいを感じられるような仕事を任せてもらえる",
        "やりがい・裁量2": "自分の判断で進められる裁量のある仕事ができる",
        "成長実感": "成長実感を感じられるような仕事を任せてもらえる",
        "達成感": "達成感を感じられるような仕事を任せてもらえる",
        "プロジェクト規模": "規模の大きなプロジェクトや仕事を任せてもらえる",
        "強みの活用": "自分の強みを活かせるような仕事を任せてもらえる"
    },
    "人間関係・組織風土": {
        "人間関係": "人間関係が良好な職場である",
        "ハラスメント対策": "セクハラやパワハラがないような職場である",
        "組織文化・カルチャーフィット": "自身の価値観や考え方と共感出来るような会社の社風や文化がある",
        "組織文化・風通し": "意見や考え方などについて自由に言い合える風通しの良い職場である",
        "組織文化・学習協働文化": "社内で相互に教えたったり・学び合ったりするような職場である"
    },
    "組織・経営基盤": {
        "経営の安定性・戦略性1": "事業基盤について安心感のある職場である",
        "経営の安定性・戦略性2": "信頼できる経営戦略や戦術を実行する職場である",
        "経営の安定性・戦略性3": "同業他社と比較して事業内容そのものに競合優位性や独自性を感じられる",
        "ブランド・認知度": "ブランド力や知名度のある職場である",
        "ミッション・バリューの共感": "会社のミッション・バリューに共感できる",
        "コンプライアンス・ガバナンス": "法令遵守が整った職場である"
    },
    "働く環境": {
        "物理的環境": "働きやすい仕事環境やオフィス環境である",
        "ダイバーシティ": "女性が働きやすい職場である"
    }
}

# ページ遷移時に一番上にスクロールする関数
def scroll_to_top():
    js = '''
    <script>
        window.scrollTo(0, 0);
    </script>
    '''
    st.markdown(js, unsafe_allow_html=True)

# イントロページ
def show_intro():
    scroll_to_top()
    st.title("従業員満足度・期待度調査")
    st.markdown("""
    このアンケートは、従業員の皆様の満足度と期待度を調査し、より良い職場環境づくりに役立てることを目的としています。
    
    各質問について、**現在の満足度**と**今後の期待度**の両方をお答えいただきます。
    回答は匿名で処理され、個人が特定されることはありません。
    
    アンケートの所要時間は約15分です。ご協力をお願いいたします。
    """)
    
    if st.button("アンケートを開始する", type="primary"):
        st.session_state.current_page = 2
        st.experimental_rerun()

# デモグラフィックページ
def show_demographics():
    scroll_to_top()
    st.title("基本情報")
    st.markdown("以下の基本情報をご入力ください。")
    
    with st.form("demographics_form"):
        for question, options in demographic_questions.items():
            if options is None:
                # 数値入力の場合
                if question == "年齢":
                    st.session_state.responses[question] = st.number_input(
                        f"{question}",
                        min_value=18,
                        max_value=80,
                        value=30,
                        step=1
                    )
                elif question == "残業時間":
                    st.session_state.responses[question] = st.number_input(
                        f"{question}（月平均時間）",
                        min_value=0,
                        max_value=100,
                        value=20,
                        step=1
                    )
                elif question == "有給休暇消化率":
                    st.session_state.responses[question] = st.slider(
                        f"{question}（%）",
                        min_value=0,
                        max_value=100,
                        value=50,
                        step=5
                    )
                elif question == "入社年":
                    current_year = datetime.now().year
                    st.session_state.responses[question] = st.selectbox(
                        f"{question}",
                        options=list(range(current_year, current_year - 50, -1))
                    )
                elif question == "年収":
                    # 年収を半角数字で直接入力
                    st.session_state.responses[question] = st.text_input(
                        f"{question}（万円）",
                        value="500",
                        help="半角数字で入力してください"
                    )
            else:
                # 選択肢がある場合
                st.session_state.responses[question] = st.selectbox(
                    f"{question}",
                    options=options
                )
        
        submit_button = st.form_submit_button("次へ進む", type="primary")
        
        if submit_button:
            st.session_state.current_page = 3
            st.experimental_rerun()

# 評価項目ページ（リッカート尺度形式）
def show_evaluation():
    scroll_to_top()
    st.title("総合評価")
    st.markdown("以下の質問について、あなたの評価をお聞かせください。")
    
    with st.form("evaluation_form"):
        # 11段階評価の質問（リッカート尺度形式）
        st.subheader("総合評価項目")
        
        # 11段階評価の説明
        st.markdown("### 選択肢の説明")
        st.write("0: 全く当てはまらない")
        st.write("5: どちらとも言えない")
        st.write("10: 非常に当てはまる")
        
        # 11段階評価の質問
        for item in evaluation_questions:
            if item['type'] == 'rating_11':
                st.markdown(f"**{item['question']}**")
                
                # ラジオボタンを作成
                value = st.radio(
                    "選択してください",
                    options=list(range(11)),
                    format_func=lambda x: f"{x}",
                    horizontal=True,
                    key=f"eval_{item['key']}",
                    label_visibility="collapsed"
                )
                
                # 選択された値を保存
                st.session_state.responses[item['key']] = value
                
                st.divider()
        
        # 活躍貢献度の質問（5段階評価）
        st.subheader("活躍貢献度")
        
        # 選択肢の説明を先に表示
        st.markdown("### 選択肢の説明")
        for i, option in enumerate(contribution_options_5):
            st.write(f"{i+1}. {option}")
        
        # 質問と選択肢
        for item in evaluation_questions:
            if item['type'] == 'contribution_5':
                st.markdown(f"**{item['question']}**")
                
                # ラジオボタンを作成
                value = st.radio(
                    "選択してください",
                    options=list(range(1, 6)),
                    format_func=lambda x: f"{x}",
                    horizontal=True,
                    key=f"eval_{item['key']}",
                    label_visibility="collapsed"
                )
                
                # 選択された値を保存
                st.session_state.responses[item['key']] = value
        
        submit_button = st.form_submit_button("次へ進む", type="primary")
        
        if submit_button:
            st.session_state.current_page = 4
            st.experimental_rerun()

# 期待項目ページ（リッカート尺度形式）
def show_expectation():
    scroll_to_top()
    st.title("期待項目の確認")
    st.markdown("以下の項目について、今の会社にどの程度**期待**しているかを率直にお答えください。")
    
    # 選択肢の説明を先に表示
    st.markdown("### 選択肢の説明")
    for i, option in enumerate(expectation_options_5):
        st.write(f"{i+1}. {option}")
    
    with st.form("expectation_form"):
        for category, questions in expectation_satisfaction_categories.items():
            st.header(category)
            
            # 各質問項目
            for q_key, question in questions.items():
                st.markdown(f"**{question}**")
                
                # ラジオボタンを作成
                value = st.radio(
                    f"期待度: {question}",
                    options=list(range(1, 6)),
                    format_func=lambda x: f"{x}",
                    horizontal=True,
                    key=f"exp_{q_key}",
                    label_visibility="collapsed"
                )
                
                # 選択された値を保存
                st.session_state.responses[f"expectation_{q_key}"] = value
                
                st.divider()
        
        submit_button = st.form_submit_button("次へ進む", type="primary")
        
        if submit_button:
            st.session_state.current_page = 5
            st.experimental_rerun()

# 満足項目ページ（リッカート尺度形式）
def show_satisfaction():
    scroll_to_top()
    st.title("満足項目の確認")
    st.markdown("以下の項目について、今の会社にどの程度**満足**しているかを率直にお答えください。")
    
    # 選択肢の説明を先に表示
    st.markdown("### 選択肢の説明")
    for i, option in enumerate(rating_options_5):
        st.write(f"{i+1}. {option}")
    
    with st.form("satisfaction_form"):
        for category, questions in expectation_satisfaction_categories.items():
            st.header(category)
            
            # 各質問項目
            for q_key, question in questions.items():
                st.markdown(f"**{question}**")
                
                # ラジオボタンを作成
                value = st.radio(
                    f"満足度: {question}",
                    options=list(range(1, 6)),
                    format_func=lambda x: f"{x}",
                    horizontal=True,
                    key=f"sat_{q_key}",
                    label_visibility="collapsed"
                )
                
                # 選択された値を保存
                st.session_state.responses[f"satisfaction_{q_key}"] = value
                
                st.divider()
        
        submit_button = st.form_submit_button("回答を送信する", type="primary")
        
        if submit_button:
            # タイムスタンプを追加
            st.session_state.responses['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # データを保存
            save_data(st.session_state.responses)
            
            # サンキューページへ
            st.session_state.current_page = 6
            st.experimental_rerun()

# サンキューページ
def show_thank_you():
    scroll_to_top()
    st.title("ご回答ありがとうございました")
    st.markdown("""
    アンケートへのご協力ありがとうございました。
    いただいた回答は、より良い職場環境づくりのために活用させていただきます。
    """)
    
    if st.button("新しいアンケートを開始", type="primary"):
        # セッション状態をリセット
        st.session_state.responses = {}
        st.session_state.current_page = 1
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
        justify-content: space-between;
    }
    .stRadio label {
        margin-right: 0;
    }
    /* 選択肢の数字を強調表示 */
    .stRadio label span:first-child {
        font-weight: bold;
        font-size: 1.1em;
    }
    /* 選択肢の間隔を調整 */
    .stRadio > div > div {
        flex: 1;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # プログレスバーの表示（ページ1は除く）
    if st.session_state.current_page > 1 and st.session_state.current_page < 6:
        progress_value = (st.session_state.current_page - 1) / 5
        st.progress(progress_value)
        st.write(f"ページ {st.session_state.current_page - 1}/5")
    
    # ページ表示
    if st.session_state.current_page == 1:
        show_intro()
    elif st.session_state.current_page == 2:
        show_demographics()
    elif st.session_state.current_page == 3:
        show_evaluation()
    elif st.session_state.current_page == 4:
        show_expectation()
    elif st.session_state.current_page == 5:
        show_satisfaction()
    elif st.session_state.current_page == 6:
        show_thank_you()

if __name__ == "__main__":
    main()
