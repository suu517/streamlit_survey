import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os
import numpy as np

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

# 質問リスト
questions = {
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
    },
    "C. 総合評価": {
        "総合評価": [
            "総合満足度",
            "この会社にどれぐらい長く勤めいたいと感じているのか",
            "自分は現在の会社もしくは部署でどれぐらい活躍できていると感じるのか",
            "親しい家族や友人にどの程度自社を勧めたいのか（NPS）"
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
                    
                    # コメント欄（オプション）
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
        
        # 会社の文化・社風に関する自由記述
        st.subheader("会社の文化・社風について")
        culture_comments = st.text_area(
            "具体的に共感できる点、またはそうでない点があれば教えてください。",
            height=100
        )
        all_comments["culture_comments"] = culture_comments
        
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
    
    特に満足度が高かった項目と改善の余地があると感じられた項目について、
    後日改めて個別ヒアリングをお願いする場合がございます。
    """)
    
    if st.button("ダッシュボードを表示", type="primary"):
        st.session_state.page = 'dashboard'
        st.experimental_rerun()

# ダッシュボードページ
def show_dashboard():
    st.title("従業員満足度・期待度ダッシュボード")
    
    # データの読み込み
    df = load_data()
    
    if df.empty:
        st.warning("まだデータがありません。アンケートに回答してください。")
        return
    
    # サイドバーでフィルタリングオプションを提供
    st.sidebar.header("フィルター")
    
    # 部署フィルター
    if 'department' in df.columns:
        departments = ["すべて"] + sorted(df['department'].unique().tolist())
        selected_dept = st.sidebar.selectbox("部署", departments)
        
        if selected_dept != "すべて":
            df = df[df['department'] == selected_dept]
    
    # 役職フィルター
    if 'position' in df.columns:
        positions = ["すべて"] + sorted(df['position'].unique().tolist())
        selected_pos = st.sidebar.selectbox("役職", positions)
        
        if selected_pos != "すべて":
            df = df[df['position'] == selected_pos]
    
    # 勤続年数フィルター
    if 'years_of_service' in df.columns:
        min_years, max_years = int(df['years_of_service'].min()), int(df['years_of_service'].max())
        years_range = st.sidebar.slider(
            "勤続年数の範囲",
            min_value=min_years,
            max_value=max_years,
            value=(min_years, max_years)
        )
        df = df[(df['years_of_service'] >= years_range[0]) & (df['years_of_service'] <= years_range[1])]
    
    # ダッシュボードの表示
    st.header("全体サマリー")
    
    # 回答者数
    st.metric("回答者数", len(df))
    
    # 満足度と期待度のカラムを抽出
    satisfaction_cols = [col for col in df.columns if col.startswith('satisfaction_')]
    expectation_cols = [col for col in df.columns if col.startswith('expectation_')]
    
    # 平均値の計算
    avg_satisfaction = df[satisfaction_cols].mean().mean()
    avg_expectation = df[expectation_cols].mean().mean()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("平均満足度", f"{avg_satisfaction:.2f}/5.00")
    
    with col2:
        st.metric("平均期待度", f"{avg_expectation:.2f}/5.00")
    
    # 満足度と期待度のギャップ分析
    st.header("満足度と期待度のギャップ分析")
    
    # 各質問カテゴリの平均値を計算
    category_data = []
    
    for section, categories in questions.items():
        for category, qs in categories.items():
            for q_idx, question in enumerate(qs):
                q_key = f"{section}_{category}_{q_idx}"
                
                sat_key = f"satisfaction_{q_key}"
                exp_key = f"expectation_{q_key}"
                
                if sat_key in df.columns and exp_key in df.columns:
                    avg_sat = df[sat_key].mean()
                    avg_exp = df[exp_key].mean()
                    gap = avg_exp - avg_sat
                    
                    category_data.append({
                        "セクション": section,
                        "カテゴリ": category,
                        "質問": question,
                        "満足度": avg_sat,
                        "期待度": avg_exp,
                        "ギャップ": gap
                    })
    
    if category_data:
        category_df = pd.DataFrame(category_data)
        
        # ギャップが大きい順にソート
        sorted_df = category_df.sort_values("ギャップ", ascending=False)
        
        # ギャップが最も大きい項目
        st.subheader("改善優先度が高い項目（期待度と満足度のギャップが大きい項目）")
        
        top_gaps = sorted_df.head(5)
        
        for _, row in top_gaps.iterrows():
            with st.expander(f"{row['質問']} (ギャップ: {row['ギャップ']:.2f})"):
                col1, col2, col3 = st.columns(3)
                col1.metric("満足度", f"{row['満足度']:.2f}/5.00")
                col2.metric("期待度", f"{row['期待度']:.2f}/5.00")
                col3.metric("ギャップ", f"{row['ギャップ']:.2f}")
        
        # ギャップチャートの作成
        st.subheader("カテゴリ別満足度・期待度ギャップ")
        
        # カテゴリごとの平均を計算
        category_avg = category_df.groupby("カテゴリ")[["満足度", "期待度", "ギャップ"]].mean().reset_index()
        category_avg = category_avg.sort_values("ギャップ", ascending=False)
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            y=category_avg["カテゴリ"],
            x=category_avg["満足度"],
            name="満足度",
            orientation='h',
            marker=dict(color='rgba(58, 71, 80, 0.6)')
        ))
        
        fig.add_trace(go.Bar(
            y=category_avg["カテゴリ"],
            x=category_avg["期待度"],
            name="期待度",
            orientation='h',
            marker=dict(color='rgba(246, 78, 139, 0.6)')
        ))
        
        fig.update_layout(
            barmode='group',
            title="カテゴリ別 満足度 vs 期待度",
            xaxis_title="スコア (5段階評価)",
            yaxis=dict(
                title="カテゴリ",
                categoryorder='total ascending'
            ),
            legend=dict(
                x=0.1,
                y=1.1,
                orientation="h"
            ),
            height=600
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # NPS分析
    st.header("NPS (Net Promoter Score) 分析")
    
    nps_key = "satisfaction_C. 総合評価_総合評価_3"  # NPS質問のキー
    
    if nps_key in df.columns:
        nps_scores = df[nps_key]
        
        # NPS計算
        promoters = (nps_scores >= 4).sum() / len(nps_scores) * 100
        passives = ((nps_scores == 3)).sum() / len(nps_scores) * 100
        detractors = (nps_scores <= 2).sum() / len(nps_scores) * 100
        
        nps = promoters - detractors
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("NPS", f"{nps:.1f}%")
        
        with col2:
            st.metric("推奨者", f"{promoters:.1f}%")
        
        with col3:
            st.metric("中立者", f"{passives:.1f}%")
        
        with col4:
            st.metric("批判者", f"{detractors:.1f}%")
        
        # NPS分布グラフ
        fig = px.histogram(
            df,
            x=nps_key,
            nbins=5,
            labels={nps_key: "スコア"},
            title="NPS分布",
            color_discrete_sequence=['#3366CC']
        )
        
        fig.update_layout(
            xaxis=dict(
                tickmode='linear',
                tick0=1,
                dtick=1,
                ticktext=["1 (全く勧めない)", "2", "3", "4", "5 (強く勧める)"],
                tickvals=[1, 2, 3, 4, 5]
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # 部署別・役職別分析
    st.header("部署別・役職別分析")
    
    tab1, tab2 = st.tabs(["部署別分析", "役職別分析"])
    
    with tab1:
        if 'department' in df.columns:
            dept_avg = df.groupby('department')[satisfaction_cols].mean().mean(axis=1).reset_index()
            dept_avg.columns = ['部署', '平均満足度']
            
            fig = px.bar(
                dept_avg,
                x='部署',
                y='平均満足度',
                title="部署別平均満足度",
                color='平均満足度',
                color_continuous_scale='Viridis'
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        if 'position' in df.columns:
            pos_avg = df.groupby('position')[satisfaction_cols].mean().mean(axis=1).reset_index()
            pos_avg.columns = ['役職', '平均満足度']
            
            # 役職の順序を設定
            position_order = ["一般社員", "主任", "係長", "課長", "部長", "役員", "その他"]
            pos_avg['役職'] = pd.Categorical(pos_avg['役職'], categories=position_order, ordered=True)
            pos_avg = pos_avg.sort_values('役職')
            
            fig = px.bar(
                pos_avg,
                x='役職',
                y='平均満足度',
                title="役職別平均満足度",
                color='平均満足度',
                color_continuous_scale='Viridis'
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    # 勤続年数と満足度の関係
    st.header("勤続年数と満足度の関係")
    
    if 'years_of_service' in df.columns:
        # 勤続年数ごとの平均満足度を計算
        df['avg_satisfaction'] = df[satisfaction_cols].mean(axis=1)
        
        fig = px.scatter(
            df,
            x='years_of_service',
            y='avg_satisfaction',
            title="勤続年数と満足度の関係",
            labels={'years_of_service': '勤続年数', 'avg_satisfaction': '平均満足度'},
            trendline="ols",
            color='department' if 'department' in df.columns else None
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # 自由記述コメントの表示
    st.header("自由記述コメント")
    
    comment_cols = [col for col in df.columns if col.startswith('comment_')]
    
    if comment_cols:
        # コメントがある列のみを抽出
        comments_df = df[['timestamp'] + comment_cols].copy()
        
        # 空でないコメントのみをフィルタリング
        for col in comment_cols:
            comments_df = comments_df[comments_df[col].notna() & (comments_df[col] != "")]
        
        if not comments_df.empty:
            for col in comment_cols:
                if col in comments_df.columns:
                    # 質問に対応するコメントを表示
                    q_key = col.replace('comment_', '')
                    
                    # セクション、カテゴリ、質問インデックスを抽出
                    parts = q_key.split('_')
                    if len(parts) >= 3:
                        section = parts[0]
                        category = parts[1]
                        q_idx = int(parts[2])
                        
                        # 対応する質問を見つける
                        if section in questions and category in questions[section] and q_idx < len(questions[section][category]):
                            question = questions[section][category][q_idx]
                            
                            with st.expander(f"コメント: {question}"):
                                for _, row in comments_df[comments_df[col].notna() & (comments_df[col] != "")].iterrows():
                                    st.markdown(f"**{row['timestamp']}**")
                                    st.markdown(row[col])
                                    st.divider()
        
        # 特別なコメント欄
        special_comments = ['valued_benefits', 'desired_benefits', 'culture_comments']
        
        for comment_key in special_comments:
            if comment_key in df.columns:
                comments = df[df[comment_key].notna() & (df[comment_key] != "")]
                
                if not comments.empty:
                    comment_title = {
                        'valued_benefits': "評価している福利厚生",
                        'desired_benefits': "希望する福利厚生",
                        'culture_comments': "会社の文化・社風についてのコメント"
                    }.get(comment_key, comment_key)
                    
                    with st.expander(comment_title):
                        for _, row in comments.iterrows():
                            st.markdown(f"**{row['timestamp']}**")
                            st.markdown(row[comment_key])
                            st.divider()
    
    # 新しいアンケートを開始するボタン
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
    elif st.session_state.page == 'dashboard':
        show_dashboard()

if __name__ == "__main__":
    main()
