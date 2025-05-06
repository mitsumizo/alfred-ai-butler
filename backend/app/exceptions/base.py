from fastapi import HTTPException, status
from typing import Any, Dict, Optional


class AppException(HTTPException):
    """アプリケーション共通の基本例外クラス"""
    def __init__(
        self,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail: Any = "Internal server error",
        headers: Optional[Dict[str, str]] = None,
        error_code: str = "ERROR_GENERAL"
    ):
        self.error_code = error_code
        super().__init__(status_code=status_code, detail=detail, headers=headers) 