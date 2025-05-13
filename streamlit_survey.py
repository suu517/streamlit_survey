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

# セッション状態初期化
def initialize():
    if 'page' not in st.session_state:
        st.session_state.page = 1
    if 'responses' not in st.session_state:
        st.session_state.responses = {}
initialize()

DATA_FILE = "employee_survey_data.csv"

@st.cache_data
def load_data():
    return pd.read_csv(DATA_FILE) if os.path.exists(DATA_FILE) else pd.DataFrame()

def save_data(record):
    df = load_data()
    df = pd.concat([df, pd.DataFrame([record])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

# 共通選択肢定義
rating_11 = {i: f"{i}" for i in range(11)}
options_5 = [
    "満足していない", "どちらかと言えば満足していない", "どちらとも言えない",
    "どちらかと言えば満足している", "満足している"
]
exp_5 = [
    "期待していない", "どちらかと言えば期待していない", "どちらとも言えない",
    "どちらかと言えば期待している", "期待している"
]
contrib_5 = [
    "活躍貢献できていない", "どちらかと言えば活躍貢献できていない", "どちらとも言えない",
    "どちらかと言えば活躍貢献できていると感じる", "活躍貢献できていると感じる"
]

# デモグラフィック質問定義
DEMOGRAPHIC_QUESTIONS = {
    "雇用形態": ["正社員", "契約社員", "パートアルバイト", "業務委託", "派遣", "その他"],
    "入社形態": ["新卒入社", "中途入社"],
    "年齢": (18, 80),
    "事業部": ["営業部", "マーケティング部", "開発部", "人事部", "経理部", "総務部", "その他"],
    "職種": ["営業", "マーケティング", "エンジニア", "デザイナー", "人事", "経理", "総務", "その他"],
    "役職": ["一般社員", "主任", "係長", "課長", "部長", "役員", "その他"],
    "残業時間（月平均）": (0, 100),
    "有給休暇消化率（%）": (0, 100),
    "入社年": list(range(datetime.now().year, datetime.now().year - 50, -1)),
    "年収（万円）": None
}

# 総合評価質問定義
EVALUATION_QUESTIONS = [
    {"label": "総合評価: この会社を友人や家族にどの程度勧めたいか", "options": list(rating_11.keys()), "key": "nps"},
    {"label": "総合満足度: 現在の環境や人間関係等を含めた満足度", "options": list(rating_11.keys()), "key": "overall_satisfaction"},
    {"label": "定着意向: この会社でこれからも長く働きたいか", "options": list(rating_11.keys()), "key": "intention_to_stay"},
    {"label": "活躍貢献度: 現在の所属組織で活躍・貢献できていると感じますか", "options": list(range(1,6)), "key": "contribution", "map": contrib_5}
]

# 期待度・満足度カテゴリと質問定義
EXPECTATION_SATISFACTION_CATEGORIES = {
    "働き方・時間の柔軟性": {
        "勤務時間の適正": "自分に合った勤務時間で働ける",
        "休暇制度1": "休日休暇がちゃんと取れる",
        "休暇制度2": "有給休暇がちゃんと取れる",
        "勤務形態の柔軟性": "リモートワーク・時短・フレックス制が使える",
        "通勤負荷": "自宅から適切な距離で働ける",
        "異動転勤希望考慮": "希望を考慮した異動・転勤体制がある",
        "社内異動制度": "社内異動体制が整備されている"
    },
    "労働条件・待遇": {
        "残業対価": "残業した分しっかり給与が支払われる",
        "業務量適正": "キャパに合った量の仕事量",
        "身体的負荷": "身体的負荷が少ない仕事内容",
        "精神的負荷": "精神的負荷が少ない仕事内容",
        "福利厚生": "充実した福利厚生がある"
    },
    "評価制度・成長": {
        "評価制度": "仕事が正当に評価される",
        "昇進昇給": "成果に応じた昇給・昇進が望める",
        "目標設定": "達成可能な目標・ノルマ設定"
    },
    "キャリア・スキル形成": {
        "専門スキル獲得": "専門的スキルや知識を獲得できる",
        "汎用スキル獲得": "コミュ力・論理的思考力など汎用スキルを獲得できる",
        "研修制度": "整った教育・研修制度がある",
        "キャリアパス設計": "将来のキャリアパスを設計してくれる",
        "業務マッチング": "やりたい方向性に合った仕事を任せてもらえる",
        "ロールモデル": "身近にロールモデルとなる人がいる"
    },
    "仕事内容・やりがい": {
        "社会貢献": "社会に貢献実感を持てる仕事",
        "やりがい裁量": "裁量ある仕事を任せてもらえる",
        "成長実感": "成長実感を得られる仕事",
        "達成感": "達成感を感じられる仕事",
        "プロジェクト規模": "大規模プロジェクトに関われる",
        "強み活用": "自分の強みを活かせる仕事"
    },
    "人間関係・組織風土": {
        "人間関係": "人間関係が良好な職場",
        "ハラスメント対策": "セクハラ・パワハラ防止が徹底されている",
        "カルチャーフィット": "価値観が合う社風",
        "風通し": "意見交換が自由な職場",
        "学習協働": "相互学習・協働文化がある"
    },
    "組織・経営基盤": {
        "安定性": "安定感のある事業基盤",
        "戦略性": "信頼できる経営戦略がある",
        "競合優位性": "競合優位性・独自性を感じる",
        "ブランド力": "ブランド力・知名度がある",
        "ミッション共感": "ミッション・バリューに共感できる",
        "ガバナンス": "法令遵守が徹底されている"
    },
    "働く環境": {
        "物理環境": "働きやすいオフィス環境",
        "ダイバーシティ": "女性が働きやすい環境"
    }
}

# 共通CSS
st.markdown("""
<style>
.stApp { max-width:1200px; margin:auto; }
.stRadio > div { flex-wrap: nowrap; overflow-x: auto; }
</style>
""", unsafe_allow_html=True)

# 各ページ表示

def page_intro():
    st.title("従業員満足度・期待度調査")
    st.write("所要時間約15分。匿名で回答されます。")
    if st.button("アンケート開始"): st.session_state.page = 2


def page_demographics():
    st.header("基本情報入力")
    cols = st.columns(3)
    for i, (q, opts) in enumerate(DEMOGRAPHIC_QUESTIONS.items()):
        with cols[i % 3]:
            if opts is None:
                if '年収' in q:
                    st.session_state.responses[q] = st.text_input(q, help="万円単位、半角数字で")
                else:
                    st.session_state.responses[q] = st.number_input(q, min_value=opts[0], max_value=opts[1], value=opts[0] if isinstance(opts, tuple) else 0)
            else:
                st.session_state.responses[q] = st.selectbox(q, options=opts)
    if st.button("次へ"): st.session_state.page = 3


def page_evaluation():
    st.header("総合評価")
    st.write("各質問について、以下のスライダーまたは選択肢で回答してください。")
    for item in EVALUATION_QUESTIONS:
        st.subheader(item['label'])
        if item.get('map'):
            sel = st.radio("", options=item['map'], horizontal=True)
            st.session_state.responses[item['key']] = item['map'].index(sel) + 1
        else:
            st.slider("", min_value=min(item['options']), max_value=max(item['options']), value=min(item['options']), key=item['key'])
    if st.button("次へ"): st.session_state.page = 4


def page_expectation():
    st.header("期待度調査")
    for cat, qs in EXPECTATION_SATISFACTION_CATEGORIES.items():
        with st.expander(cat):
            for k, label in qs.items():
                st.session_state.responses[f"exp_{k}"] = st.radio(label, options=exp_5, horizontal=True)
    if st.button("次へ"): st.session_state.page = 5


def page_satisfaction():
    st.header("満足度調査")
    for cat, qs in EXPECTATION_SATISFACTION_CATEGORIES.items():
        with st.expander(cat):
            for k, label in qs.items():
                st.session_state.responses[f"sat_{k}"] = st.radio(label, options=options_5, horizontal=True)
    if st.button("回答を送信"): 
        st.session_state.responses['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        save_data(st.session_state.responses)
        st.session_state.page = 6


def page_thanks():
    st.success("ご回答ありがとうございました！")
    if st.button("新しいアンケート"): 
        st.session_state.responses.clear()
        st.session_state.page = 1

# メイン制御
if st.session_state.page == 1:
    page_intro()
elif st.session_state.page == 2:
    page_demographics()
elif st.session_state.page == 3:
    page_evaluation()
elif st.session_state.page == 4:
    page_expectation()
elif st.session_state.page == 5:
    page_satisfaction()
else:
    page_thanks()
