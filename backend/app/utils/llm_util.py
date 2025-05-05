from langchain_openai import ChatOpenAI
from os import getenv
from langchain_openai import OpenAIEmbeddings


def get_openrouter(
    model: str = "moonshotai/moonlight-16b-a3b-instruct:free",
) -> ChatOpenAI:
    """OpenRouter APIを使用してLLMにアクセスするためのChatOpenAIインスタンスを返す

    OpenRouterは複数のLLMプロバイダーへの統一的なアクセスを提供するサービスです。
    直接OpenAIを使用する場合は、ChatOpenAI(model="gpt-4")のように指定することもできます。

    Args:
        model: 使用するモデル名。デフォルトはClaude 3 Sonnet

    Returns:
        ChatOpenAI: 設定済みのChatOpenAIインスタンス
    """
    return ChatOpenAI(
        model=model,
        openai_api_key=getenv("OPENROUTER_API_KEY"),
        openai_api_base="https://openrouter.ai/api/v1",
    )


def get_embeddings(model: str = "text-embedding-3-small") -> OpenAIEmbeddings:
    """埋め込みモデルにアクセスするためのOpenAIEmbeddingsインスタンスを返す

    Args:
        model: 使用するモデル名。デフォルトはtext-embedding-3-small

    Returns:
        OpenAIEmbeddings: 設定済みのOpenAIEmbeddingsインスタンス
    """
    return OpenAIEmbeddings(model=model)
