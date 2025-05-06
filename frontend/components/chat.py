import streamlit as st
from utils.api import send_chat_message, search_documents


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
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "いらっしゃいませ。執事アルフレッドがご質問にお答えします。",
            }
        ]

    # チャット履歴を表示
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # チャット入力
    if prompt := st.chat_input("メッセージを入力してください..."):
        # ユーザーメッセージをチャット履歴に追加
        st.session_state.messages.append({"role": "user", "content": prompt})

        # ユーザーのメッセージを表示
        with st.chat_message("user"):
            st.markdown(prompt)

        # RAG検索を実行して関連情報を取得
        relevant_context = ""
        try:
            with st.spinner("関連情報を検索中..."):
                search_results = search_documents(prompt)

                if search_results.get("results") and len(search_results["results"]) > 0:
                    for result in search_results["results"]:
                        relevant_context += result.get("content", "") + "\n\n"
        except Exception as e:
            st.error(f"情報検索中にエラーが発生しました: {str(e)}", icon="🔍")

        # APIレスポンスを待機中表示
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("🤔 考え中...")

            try:
                # APIにメッセージを送信（関連情報も送信）
                response = send_chat_message(
                    prompt, context=relevant_context if relevant_context else None
                )
                assistant_response = response.get(
                    "response", "申し訳ありません。応答を生成できませんでした。"
                )

                # アシスタントの応答をチャット履歴に追加
                st.session_state.messages.append(
                    {"role": "assistant", "content": assistant_response}
                )

                # 応答を表示
                message_placeholder.markdown(assistant_response)

            except Exception as e:
                error_message = f"エラーが発生しました: {str(e)}"
                message_placeholder.markdown(f"🚫 {error_message}")
                st.session_state.messages.append(
                    {"role": "assistant", "content": error_message}
                )
