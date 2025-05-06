from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
from sqlalchemy.orm import Session
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain

from app.utils.llm_util import get_openrouter
from app.services.embedding import EmbeddingService
from app.core.db import get_db

# 追加予定: LangChain関連のインポート
# from langchain.chat_models import ChatOpenAI
# from langchain.chains import ConversationalRetrievalChain
# など

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
    responses={404: {"description": "Not found"}},
)


# チャットメッセージの入力モデル
class ChatInput(BaseModel):
    message: str


# チャットメッセージの出力モデル
class ChatResponse(BaseModel):
    response: str
    source_documents: Optional[List[Dict[str, Any]]] = None


# LangChainとRAGを使用したチャットエンドポイント
@router.post("/", response_model=ChatResponse)
async def chat(chat_input: ChatInput, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    ユーザーのメッセージに対してAI執事として応答します。
    RAG (Retrieval Augmented Generation) を使用してドキュメントに基づいた回答を生成します。
    """
    try:
        # 埋め込みサービスを初期化
        embedding_service = EmbeddingService(db)

        # ユーザークエリに関連するドキュメントを検索
        relevant_docs = embedding_service.similarity_search(chat_input.message, limit=5)

        # LangChainドキュメント形式に変換
        langchain_docs = [
            Document(page_content=doc["text"], metadata={"source": doc["source"]})
            for doc in relevant_docs
        ]

        # LLMとチェーンを初期化
        llm = get_openrouter(model="openai/gpt-4o-mini")

        # プロンプトテンプレートを作成（執事のペルソナを含む）
        prompt = ChatPromptTemplate.from_template(
            """
        あなたは知識豊富で礼儀正しい執事です。
        以下の質問に対して、提供された情報源をもとに丁寧に回答してください。

        情報源:
        {context}
        
        質問: {input}
        """
        )

        # ドキュメントチェーンを作成
        document_chain = create_stuff_documents_chain(llm, prompt)

        # 最終的な応答を生成
        result = document_chain.invoke(
            {"input": chat_input.message, "context": langchain_docs}
        )

        # 結果をフォーマット
        return ChatResponse(
            response=result,
            source_documents=relevant_docs,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"チャット処理中にエラーが発生しました: {str(e)}",
        )
