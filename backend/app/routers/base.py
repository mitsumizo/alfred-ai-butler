from fastapi import APIRouter, HTTPException, status
from app.core.events import health_check
from app.exceptions import (
    AppException,
    NotFoundError,
    ValidationError,
    AuthenticationError,
    AuthorizationError,
)

# 基本ルーター作成
router = APIRouter(tags=["base"])


@router.get("/")
async def read_root():
    """
    基本的な疎通確認用エンドポイント
    """
    return {"message": "AI Butler Alfred API is running!"}


@router.get("/health")
async def health_check_endpoint():
    """
    ヘルスチェック用エンドポイント
    """
    return await health_check()


# 例外テスト用エンドポイント
@router.get("/exceptions/{exception_type}")
async def test_exception(exception_type: str):
    """
    各種例外をテストするためのエンドポイント

    例外の種類:
    - standard: 標準のHTTPException
    - app: アプリケーション例外
    - not_found: NotFoundError
    - validation: ValidationError
    - auth: 認証エラー
    - permission: 権限エラー
    - unhandled: 未処理の例外
    """
    if exception_type == "standard":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Standard HTTP exception test",
        )

    elif exception_type == "app":
        raise AppException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Application exception test",
            error_code="TEST_ERROR",
        )

    elif exception_type == "not_found":
        raise NotFoundError(detail="Resource not found test")

    elif exception_type == "validation":
        raise ValidationError(detail="Validation error test")

    elif exception_type == "auth":
        raise AuthenticationError(detail="Authentication error test")

    elif exception_type == "permission":
        raise AuthorizationError(detail="Permission denied test")

    elif exception_type == "unhandled":
        # 未処理例外のテスト
        raise ValueError("Unhandled exception test")

    else:
        return {"message": f"No exception triggered. Unknown type: {exception_type}"}
