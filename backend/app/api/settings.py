from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Dict, Any

router = APIRouter(
    prefix="/settings",
    tags=["settings"],
    responses={404: {"description": "Not found"}},
)


class SettingsUpload(BaseModel):
    """設定ファイルのアップロードモデル"""

    content: str


@router.post("/upload")
async def upload_settings(settings: SettingsUpload) -> Dict[str, Any]:
    """
    設定ファイルの内容をアップロードし、処理します。
    """
    try:
        # 注：実際の実装では、ここでテキストをベクトル化してデータベースに保存します
        # TODO: テキスト分割、ベクトル化、保存の実装を追加

        # ファイル内容の確認（デバッグ用）
        content_preview = (
            settings.content[:100] + "..."
            if len(settings.content) > 100
            else settings.content
        )
        print(f"受信した設定ファイル内容: {content_preview}")

        # 成功レスポンス
        return {
            "success": True,
            "message": "設定ファイルが正常に処理されました",
            "content_length": len(settings.content),
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"設定ファイルの処理中にエラーが発生しました: {str(e)}",
        )
