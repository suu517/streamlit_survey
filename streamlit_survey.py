import streamlit as st
import pandas as pd
from datetime import datetime
import os
import base64

# ページ設定
st.set_page_config(
    page_title="従業員満足度・期待度調査",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# セッション状態の初期化
def initialize_session():
    defaults = {
        'page': 'intro',
        'responses': {},
        'current_page': 1,
        'error_message': None
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

initialize_session()

# データファイルパス
DATA_FILE = "employee_survey_data.csv"

# データ読み込み
@st.cache_data
def load_data():
    return pd.read_csv(DATA_FILE) if os.path.exists(DATA_FILE) else pd.DataFrame()

# データ保存
def save_data(data):
    if os.path.exists(DATA_FILE):
        df = load_data()
        df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
    else:
        df = pd.DataFrame([data])
    df.to_csv(DATA_FILE, index=False)

# 共通評価オプション
rating_options_11 = {
    i: f"{i}" for i in range(11)
}

rating_options_5 = [
    "満足していない", "どちらかと言えば満足していない", "どちらとも言えない",
    "どちらかと言えば満足している", "満足している"
]

expectation_options_5 = [
    "期待していない", "どちらかと言えば期待していない", "どちらとも言えない",
    "どちらかと言えば期待している", "期待している"
]

contribution_options_5 = [
    "活躍貢献できていない", "どちらかと言えば活躍貢献できていない", "どちらとも言えない",
    "どちらかと言えば活躍貢献できていると感じる", "活躍貢献できていると感じる"
]

# デモグラフィック質問
DEMOGRAPHIC_QUESTIONS = {
    "雇用形態": ["正社員", "契約社員", "パートアルバイト", "業務委託", "派遣", "その他"],
    "入社形態": ["新卒入社", "中途入社"],
    "年齢": None,
    "事業部": ["営業部", "マーケティング部", "開発部", "人事部", "経理部", "総務部", "その他"],
    "職種": ["営業", "マーケティング", "エンジニア", "デザイナー", "人事", "経理", "総務", "その他"],
    "役職": ["一般社員", "主任", "係長", "課長", "部長", "役員", "その他"],
    "残業時間": None,
    "有給休暇消化率": None,
    "入社年": None,
    "年収": None
}

# 評価項目
EVALUATION_QUESTIONS = [
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
EXPECTATION_SATISFACTION_CATEGORIES = {
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

# エラーメッセージ表示
def show_error_message():
    if st.session_state.error_message:
        st.error(st.session_state.error_message)
        st.session_state.error_message = None

# ページ遷移関数 - Streamlitの状態を完全にリセットして新しいページを表示
def change_page(new_page):
    # 現在のページを更新
    st.session_state.current_page = new_page
    # 強制的にページをリロード
    st.experimental_singleton.clear()
    st.experimental_memo.clear()
    st.rerun()

# イントロページ
def show_intro():
    # 最初に空のコンテナを表示（これにより画面の一番上に表示される）
    top_container = st.empty()
    
    with top_container.container():
        st.title("従業員満足度・期待度調査")
        st.markdown("""
        このアンケートは、従業員の皆様の満足度と期待度を調査し、より良い職場環境づくりに役立てることを目的としています。
        
        各質問について、**現在の満足度**と**今後の期待度**の両方をお答えいただきます。
        回答は匿名で処理され、個人が特定されることはありません。
        
        アンケートの所要時間は約15分です。ご協力をお願いいたします。
        """)
        
        if st.button("アンケートを開始する", type="primary"):
            st.session_state.current_page = 2
            st.rerun()

# デモグラフィックページ
def show_demographics():
    # 最初に空のコンテナを表示（これにより画面の一番上に表示される）
    top_container = st.empty()
    
    with top_container.container():
        st.title("基本情報")
        st.markdown("以下の基本情報をご入力ください。")
        
        # エラーメッセージ表示
        show_error_message()
        
        with st.form("demographics_form"):
            for question, options in DEMOGRAPHIC_QUESTIONS.items():
                if options is None:
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
                        st.session_state.responses[question] = st.text_input(
                            f"{question}（万円）",
                            value="500",
                            help="半角数字で入力してください"
                        )
                else:
                    st.session_state.responses[question] = st.selectbox(
                        f"{question}",
                        options=options
                    )
            
            submit_button = st.form_submit_button("次へ進む", type="primary")
            
            if submit_button:
                # 全ての質問に回答されているか確認
                all_answered = True
                for question in DEMOGRAPHIC_QUESTIONS.keys():
                    if question not in st.session_state.responses or not st.session_state.responses[question]:
                        all_answered = False
                        break
                
                if all_answered:
                    st.session_state.current_page = 3
                    # 強制的にページをリロード
                    st.experimental_singleton.clear()
                    st.experimental_memo.clear()
                    st.rerun()
                else:
                    st.session_state.error_message = "すべての質問に回答してください。"
                    st.rerun()

# 評価項目ページ
def show_evaluation():
    # 最初に空のコンテナを表示（これにより画面の一番上に表示される）
    top_container = st.empty()
    
    with top_container.container():
        st.title("総合評価")
        st.markdown("以下の質問について、あなたの評価をお聞かせください。")
        
        # エラーメッセージ表示
        show_error_message()
        
        # 11段階評価の説明をカード形式で表示
        with st.container():
            st.markdown("""
            <div style="background-color: #f0f2f6; padding: 15px; border-radius: 10px; margin-bottom: 20px;">
                <h3 style="margin-top: 0;">選択肢の説明</h3>
                <div style="display: flex; justify-content: space-between;">
                    <div>0: 全く当てはまらない</div>
                    <div>5: どちらとも言えない</div>
                    <div>10: 非常に当てはまる</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # 11段階評価の質問（フォームの外で処理）
        st.markdown("## 総合評価項目")
        
        for item in EVALUATION_QUESTIONS:
            if item['type'] == 'rating_11':
                st.markdown(f"### {item['question']}")
                
                # 選択肢を水平に配置
                cols = st.columns(11)
                for i in range(11):
                    with cols[i]:
                        # セッション状態から現在の選択を取得
                        is_selected = st.session_state.responses.get(item['key']) == i
                        
                        # ボタンのスタイルを選択状態に応じて変更
                        button_label = f"{i}"
                        button_type = "primary" if is_selected else "secondary"
                        
                        # ボタンをクリックしたときの処理
                        if st.button(button_label, key=f"btn_{item['key']}_{i}", type=button_type):
                            st.session_state.responses[item['key']] = i
                            st.rerun()
                
                # 特定の値の下に説明を表示
                cols = st.columns(11)
                with cols[0]:
                    st.markdown("<div style='text-align: center; font-size: 0.8em;'>全く当てはまらない</div>", unsafe_allow_html=True)
                with cols[5]:
                    st.markdown("<div style='text-align: center; font-size: 0.8em;'>どちらとも言えない</div>", unsafe_allow_html=True)
                with cols[10]:
                    st.markdown("<div style='text-align: center; font-size: 0.8em;'>非常に当てはまる</div>", unsafe_allow_html=True)
                
                st.markdown("<hr>", unsafe_allow_html=True)
        
        # 活躍貢献度の説明
        st.markdown("## 活躍貢献度")
        
        # 選択肢の説明をカード形式で表示
        with st.container():
            st.markdown("""
            <div style="background-color: #f0f2f6; padding: 15px; border-radius: 10px; margin-bottom: 20px;">
                <h3 style="margin-top: 0;">選択肢の説明</h3>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px;">
            """, unsafe_allow_html=True)
            
            for i, option in enumerate(contribution_options_5):
                st.markdown(f"<div>{i+1}: {option}</div>", unsafe_allow_html=True)
            
            st.markdown("</div></div>", unsafe_allow_html=True)
        
        # 活躍貢献度の質問（フォームの外で処理）
        for item in EVALUATION_QUESTIONS:
            if item['type'] == 'contribution_5':
                st.markdown(f"### {item['question']}")
                
                # 選択肢を水平に配置
                cols = st.columns(5)
                for i in range(1, 6):
                    with cols[i-1]:
                        # セッション状態から現在の選択を取得
                        is_selected = st.session_state.responses.get(item['key']) == i
                        
                        # ボタンのスタイルを選択状態に応じて変更
                        button_label = f"{i}"
                        button_type = "primary" if is_selected else "secondary"
                        
                        # ボタンをクリックしたときの処理
                        if st.button(button_label, key=f"btn_{item['key']}_{i}", type=button_type):
                            st.session_state.responses[item['key']] = i
                            st.rerun()
                
                # 各ボタンの下に説明を表示
                cols = st.columns(5)
                for i, option in enumerate(contribution_options_5):
                    with cols[i]:
                        st.markdown(f"<div style='text-align: center; font-size: 0.8em;'>{option}</div>", unsafe_allow_html=True)
        
        # 次へ進むボタン（フォームの外）
        if st.button("次へ進む", type="primary", key="next_button_eval"):
            # 全ての質問に回答されているか確認
            all_answered = True
            for item in EVALUATION_QUESTIONS:
                if item['key'] not in st.session_state.responses:
                    all_answered = False
                    break
            
            if all_answered:
                st.session_state.current_page = 4
                # 強制的にページをリロード
                st.experimental_singleton.clear()
                st.experimental_memo.clear()
                st.rerun()
            else:
                st.session_state.error_message = "すべての質問に回答してください。"
                st.rerun()

# 期待項目ページ
def show_expectation():
    # 最初に空のコンテナを表示（これにより画面の一番上に表示される）
    top_container = st.empty()
    
    with top_container.container():
        st.title("期待項目の確認")
        st.markdown("以下の項目について、今の会社にどの程度**期待**しているかを率直にお答えください。")
        
        # エラーメッセージ表示
        show_error_message()
        
        # 選択肢の説明をカード形式で表示
        with st.container():
            st.markdown("""
            <div style="background-color: #f0f2f6; padding: 15px; border-radius: 10px; margin-bottom: 20px;">
                <h3 style="margin-top: 0;">選択肢の説明</h3>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px;">
            """, unsafe_allow_html=True)
            
            for i, option in enumerate(expectation_options_5):
                st.markdown(f"<div>{i+1}: {option}</div>", unsafe_allow_html=True)
            
            st.markdown("</div></div>", unsafe_allow_html=True)
        
        # カテゴリごとに質問を表示
        for category, questions in EXPECTATION_SATISFACTION_CATEGORIES.items():
            st.markdown(f"## {category}")
            
            # 各質問項目
            for q_key, question in questions.items():
                st.markdown(f"### {question}")
                
                # 選択肢を水平に配置
                cols = st.columns(5)
                for i in range(1, 6):
                    with cols[i-1]:
                        # セッション状態から現在の選択を取得
                        is_selected = st.session_state.responses.get(f"expectation_{q_key}") == i
                        
                        # ボタンのスタイルを選択状態に応じて変更
                        button_label = f"{i}"
                        button_type = "primary" if is_selected else "secondary"
                        
                        # ボタンをクリックしたときの処理
                        if st.button(button_label, key=f"btn_exp_{q_key}_{i}", type=button_type):
                            st.session_state.responses[f"expectation_{q_key}"] = i
                            st.rerun()
                
                # 各ボタンの下に説明を表示
                cols = st.columns(5)
                for i, option in enumerate(expectation_options_5):
                    with cols[i]:
                        st.markdown(f"<div style='text-align: center; font-size: 0.8em;'>{option}</div>", unsafe_allow_html=True)
                
                st.markdown("<hr>", unsafe_allow_html=True)
        
        # 次へ進むボタン
        if st.button("次へ進む", type="primary", key="next_button_exp"):
            # 全ての質問に回答されているか確認
            all_answered = True
            for category, questions in EXPECTATION_SATISFACTION_CATEGORIES.items():
                for q_key in questions.keys():
                    if f"expectation_{q_key}" not in st.session_state.responses:
                        all_answered = False
                        break
                if not all_answered:
                    break
            
            if all_answered:
                st.session_state.current_page = 5
                # 強制的にページをリロード
                st.experimental_singleton.clear()
                st.experimental_memo.clear()
                st.rerun()
            else:
                st.session_state.error_message = "すべての質問に回答してください。"
                st.rerun()

# 満足項目ページ
def show_satisfaction():
    # 最初に空のコンテナを表示（これにより画面の一番上に表示される）
    top_container = st.empty()
    
    with top_container.container():
        st.title("満足項目の確認")
        st.markdown("以下の項目について、今の会社にどの程度**満足**しているかを率直にお答えください。")
        
        # エラーメッセージ表示
        show_error_message()
        
        # 選択肢の説明をカード形式で表示
        with st.container():
            st.markdown("""
            <div style="background-color: #f0f2f6; padding: 15px; border-radius: 10px; margin-bottom: 20px;">
                <h3 style="margin-top: 0;">選択肢の説明</h3>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px;">
            """, unsafe_allow_html=True)
            
            for i, option in enumerate(rating_options_5):
                st.markdown(f"<div>{i+1}: {option}</div>", unsafe_allow_html=True)
            
            st.markdown("</div></div>", unsafe_allow_html=True)
        
        # カテゴリごとに質問を表示
        for category, questions in EXPECTATION_SATISFACTION_CATEGORIES.items():
            st.markdown(f"## {category}")
            
            # 各質問項目
            for q_key, question in questions.items():
                st.markdown(f"### {question}")
                
                # 選択肢を水平に配置
                cols = st.columns(5)
                for i in range(1, 6):
                    with cols[i-1]:
                        # セッション状態から現在の選択を取得
                        is_selected = st.session_state.responses.get(f"satisfaction_{q_key}") == i
                        
                        # ボタンのスタイルを選択状態に応じて変更
                        button_label = f"{i}"
                        button_type = "primary" if is_selected else "secondary"
                        
                        # ボタンをクリックしたときの処理
                        if st.button(button_label, key=f"btn_sat_{q_key}_{i}", type=button_type):
                            st.session_state.responses[f"satisfaction_{q_key}"] = i
                            st.rerun()
                
                # 各ボタンの下に説明を表示
                cols = st.columns(5)
                for i, option in enumerate(rating_options_5):
                    with cols[i]:
                        st.markdown(f"<div style='text-align: center; font-size: 0.8em;'>{option}</div>", unsafe_allow_html=True)
                
                st.markdown("<hr>", unsafe_allow_html=True)
        
        # 送信ボタン
        if st.button("回答を送信する", type="primary", key="submit_button_sat"):
            # 全ての質問に回答されているか確認
            all_answered = True
            for category, questions in EXPECTATION_SATISFACTION_CATEGORIES.items():
                for q_key in questions.keys():
                    if f"satisfaction_{q_key}" not in st.session_state.responses:
                        all_answered = False
                        break
                if not all_answered:
                    break
            
            if all_answered:
                # タイムスタンプを追加
                st.session_state.responses['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # データを保存
                save_data(st.session_state.responses)
                
                # サンキューページへ
                st.session_state.current_page = 6
                # 強制的にページをリロード
                st.experimental_singleton.clear()
                st.experimental_memo.clear()
                st.rerun()
            else:
                st.session_state.error_message = "すべての質問に回答してください。"
                st.rerun()

# サンキューページ
def show_thank_you():
    # 最初に空のコンテナを表示（これにより画面の一番上に表示される）
    top_container = st.empty()
    
    with top_container.container():
        st.title("ご回答ありがとうございました")
        st.markdown("""
        アンケートへのご協力ありがとうございました。
        いただいた回答は、より良い職場環境づくりのために活用させていただきます。
        """)
        
        if st.button("新しいアンケートを開始", type="primary"):
            # セッション状態をリセット
            st.session_state.responses = {}
            st.session_state.current_page = 1
            # 強制的にページをリロード
            st.experimental_singleton.clear()
            st.experimental_memo.clear()
            st.rerun()

# メインアプリケーション
def main():
    # カスタムCSS
    st.markdown("""
    <style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    
    /* カード風のスタイル */
    .card {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    
    /* 質問のスタイル */
    h3 {
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    
    /* ボタンのスタイル調整 */
    .stButton button {
        width: 100%;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    /* 選択されたボタンのスタイル */
    .stButton button[data-baseweb="button"][kind="primary"] {
        background-color: #1E88E5;
    }
    
    /* 区切り線のスタイル */
    hr {
        margin: 2rem 0;
        border: 0;
        border-top: 1px solid #e0e0e0;
    }
    
    /* プログレスバーのスタイル */
    .stProgress > div > div {
        background-color: #1E88E5;
    }
    
    /* エラーメッセージのスタイル */
    .stAlert {
        margin-bottom: 20px;
    }
    
    /* モバイル対応 */
    @media (max-width: 768px) {
        .stButton button {
            font-size: 0.8rem;
            padding: 0.3rem;
        }
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
