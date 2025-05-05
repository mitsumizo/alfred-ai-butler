import streamlit as st
from utils.api import upload_settings


def render_settings_ui():
    """設定UIを描画します。"""
    st.header("設定")

    # 設定ファイルのアップロード
    st.subheader("設定ファイル")
    uploaded_file = st.file_uploader("設定ファイルをアップロード", type=["txt"])

    if uploaded_file is not None:
        # ファイルプレビューを表示
        st.text_area(
            "ファイル内容プレビュー",
            uploaded_file.getvalue().decode("utf-8")[:500] + "...",
            height=150,
            disabled=True,
        )

        if st.button("設定を保存"):
            try:
                # ファイルの内容を読み込む
                file_content = uploaded_file.getvalue().decode("utf-8")

                # APIに送信
                response = upload_settings(file_content)

                if response.get("success"):
                    st.success(response.get("message", "設定が保存されました！"))
                    st.info(f"コンテンツ長: {response.get('content_length', 0)} 文字")
                else:
                    st.error(f"エラー: {response.get('message', '不明なエラー')}")

            except Exception as e:
                st.error(f"エラーが発生しました: {str(e)}")

    # 設定情報の説明
    with st.expander("設定ファイルについて"):
        st.markdown(
            """
        設定ファイルは執事アルフレッドの人格や知識を定義するテキストファイルです。

        以下のような情報を含めることができます：

        - 執事の名前、年齢、経歴
        - 性格の特徴
        - 得意な分野
        - あなたの好みや習慣

        これらの情報に基づいて、AIはあなた専用の執事として応答します。
        """
        )
