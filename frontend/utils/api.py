import requests
import os
from typing import Dict, Any, Optional

# APIのベースURL
API_URL = os.getenv("API_URL", "http://localhost:8000")


def send_chat_message(message: str, context: Optional[str] = None) -> Dict[str, Any]:
    """
    チャットメッセージをAPIに送信し、応答を取得します。

    Args:
        message: ユーザーからのメッセージ
        context: 検索結果などの追加コンテキスト（オプション）

    Returns:
        APIからの応答（辞書形式）

    Raises:
        Exception: 通信エラーが発生した場合
    """
    try:
        payload = {"message": message}
        if context:
            payload["context"] = context

        response = requests.post(f"{API_URL}/chat", json=payload)
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
        response = requests.post(f"{API_URL}/files/upload", json={"content": content})
        response.raise_for_status()  # HTTPエラーがあれば例外を発生
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"API通信エラー: {str(e)}")


def upload_rag_file(file_content: bytes, filename: str) -> Dict[str, Any]:
    """
    RAG用のファイルをAPIに送信します。

    Args:
        file_content: ファイルのバイトデータ
        filename: ファイル名

    Returns:
        APIからの応答（辞書形式）

    Raises:
        Exception: 通信エラーが発生した場合
    """
    try:
        files = {"file": (filename, file_content, "text/markdown")}
        response = requests.post(f"{API_URL}/files/upload/", files=files)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"API通信エラー: {str(e)}")


def search_documents(query: str, limit: int = 5) -> Dict[str, Any]:
    """
    RAG用のドキュメントを検索します。

    Args:
        query: 検索クエリ
        limit: 取得する結果の最大数

    Returns:
        APIからの応答（辞書形式）

    Raises:
        Exception: 通信エラーが発生した場合
    """
    try:
        response = requests.get(
            f"{API_URL}/files/search/", params={"query": query, "limit": limit}
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"API通信エラー: {str(e)}")
