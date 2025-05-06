import streamlit as st
import os
from dotenv import load_dotenv
from components.chat import render_chat_ui
from components.settings import render_settings_ui

# 環境変数を読み込む
load_dotenv()

# APIのベースURL
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

# アプリケーションのタイトルとデザイン設定
st.set_page_config(
    page_title="執事アルフレッド",
    page_icon="👨‍💼",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# タイトルと説明
st.title("執事アルフレッド")
st.markdown("*あなた専用のAI執事が、設定に基づいて対話します*")

# サイドバーに設定を追加
with st.sidebar:
    render_settings_ui()

# メインエリアにチャットUIを表示
render_chat_ui()

# フッター
st.markdown("---")
st.caption("© 2024 執事アルフレッド - AI執事チャットボット")
