import streamlit as st
from utils.api import send_chat_message


def initialize_chat_state():
    """チャット用のセッション状態を初期化します。"""
    if "messages" not in st.session_state:
        st.session_state.messages = []


def display_chat_history():
    """チャット履歴を表示します。"""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def handle_user_input(prompt: str):
    """
    ユーザー入力を処理し、APIに送信して応答を表示します。

    Args:
        prompt: ユーザーからの入力メッセージ
    """
    if not prompt:
        return

    # ユーザーメッセージを表示
    with st.chat_message("user"):
        st.markdown(prompt)

    # メッセージをセッション状態に追加
    st.session_state.messages.append({"role": "user", "content": prompt})

    # APIリクエスト
    with st.spinner("考え中..."):
        try:
            # APIにメッセージを送信
            response_data = send_chat_message(prompt)

            # 応答を取得
            assistant_response = response_data.get(
                "response", "申し訳ありません、応答を生成できませんでした。"
            )

        except Exception as e:
            assistant_response = f"エラーが発生しました: {str(e)}"

    # アシスタントの返答を表示
    with st.chat_message("assistant"):
        st.markdown(assistant_response)

    # メッセージをセッション状態に追加
    st.session_state.messages.append(
        {"role": "assistant", "content": assistant_response}
    )


def render_chat_ui():
    """チャットUIを描画します。"""
    # セッション状態の初期化
    initialize_chat_state()

    # チャット履歴の表示
    display_chat_history()

    # ユーザー入力欄
    prompt = st.chat_input("執事アルフレッドに話しかける")

    # 入力があれば処理
    if prompt:
        handle_user_input(prompt)
