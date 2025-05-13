# 期待項目ページ
def show_expectation():
    scroll_to_top()
    st.title("期待項目の確認")
    st.markdown("以下の項目について、今の会社にどの程度**期待**しているかを率直にお答えください。")
    
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
                        st.experimental_rerun()
            
            # 各ボタンの下に説明を表示
            cols = st.columns(5)
            for i, option in enumerate(expectation_options_5):
                with cols[i]:
                    st.markdown(f"<div style='text-align: center; font-size: 0.8em;'>{option}</div>", unsafe_allow_html=True)
            
            st.markdown("<hr>", unsafe_allow_html=True)
    
    # 次へ進むボタン
    if st.button("次へ進む", type="primary", key="next_button_exp"):
        st.session_state.current_page = 5
        st.experimental_rerun()

# 満足項目ページ
def show_satisfaction():
    scroll_to_top()
    st.title("満足項目の確認")
    st.markdown("以下の項目について、今の会社にどの程度**満足**しているかを率直にお答えください。")
    
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
                        st.experimental_rerun()
            
            # 各ボタンの下に説明を表示
            cols = st.columns(5)
            for i, option in enumerate(rating_options_5):
                with cols[i]:
                    st.markdown(f"<div style='text-align: center; font-size: 0.8em;'>{option}</div>", unsafe_allow_html=True)
            
            st.markdown("<hr>", unsafe_allow_html=True)
    
    # 送信ボタン
    if st.button("回答を送信する", type="primary", key="submit_button_sat"):
        # タイムスタンプを追加
        st.session_state.responses['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # データを保存
        save_data(st.session_state.responses)
        
        # サンキューページへ
        st.session_state.current_page = 6
        st.experimental_rerun()
