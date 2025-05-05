from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Dict, Any, Optional, List

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
    responses={404: {"description": "Not found"}},
)


class ChatInput(BaseModel):
    """チャットメッセージの入力モデル"""

    message: str


class ChatResponse(BaseModel):
    """チャットメッセージの出力モデル"""

    response: str
    source_documents: Optional[List[Dict[str, Any]]] = None


@router.post("/", response_model=ChatResponse)
async def chat(chat_input: ChatInput) -> Dict[str, Any]:
    """
    ユーザーのメッセージに対してAI執事として応答します。
    """
    try:
        # 注：実際の実装では、ここでLangChainエージェントを呼び出して
        # RAGベースの応答生成を行います

        # TODO: 実際のLangChain実装を追加する
        # 現在はモックレスポンスを返します
        mock_response = f"ご質問ありがとうございます。「{chat_input.message}」についてお答えいたします。"

        return ChatResponse(
            response=mock_response,
            source_documents=[],  # 将来的には参照した文書情報を含める
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"チャット処理中にエラーが発生しました: {str(e)}",
        )
