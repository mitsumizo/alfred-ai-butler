import requests
import os
from typing import Dict, Any

# APIのベースURL
API_URL = os.getenv("API_URL", "http://localhost:8000")


def send_chat_message(message: str) -> Dict[str, Any]:
    """
    チャットメッセージをAPIに送信し、応答を取得します。

    Args:
        message: ユーザーからのメッセージ

    Returns:
        APIからの応答（辞書形式）

    Raises:
        Exception: 通信エラーが発生した場合
    """
    try:
        response = requests.post(f"{API_URL}/chat", json={"message": message})
        response.raise_for_status()  # HTTPエラーがあれば例外を発生
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"API通信エラー: {str(e)}")


def upload_settings(content: str) -> Dict[str, Any]:
    """
    設定ファイルの内容をAPIに送信します。

    Args:
        content: 設定ファイルの内容（テキスト）

    Returns:
        APIからの応答（辞書形式）

    Raises:
        Exception: 通信エラーが発生した場合
    """
    try:
        response = requests.post(
            f"{API_URL}/settings/upload", json={"content": content}
        )
        response.raise_for_status()  # HTTPエラーがあれば例外を発生
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"API通信エラー: {str(e)}")
