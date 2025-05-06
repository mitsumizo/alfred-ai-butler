from fastapi import status
from typing import Any, Dict, Optional
from .base import AppException


class NotFoundError(AppException):
    """リソースが見つからない場合の例外"""

    def __init__(
        self,
        detail: Any = "Resource not found",
        headers: Optional[Dict[str, str]] = None,
        error_code: str = "ERROR_NOT_FOUND",
    ):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
            headers=headers,
            error_code=error_code,
        )


class ValidationError(AppException):
    """バリデーションエラー用の例外"""

    def __init__(
        self,
        detail: Any = "Validation error",
        headers: Optional[Dict[str, str]] = None,
        error_code: str = "ERROR_VALIDATION",
    ):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
            headers=headers,
            error_code=error_code,
        )


class AuthenticationError(AppException):
    """認証エラー用の例外"""

    def __init__(
        self,
        detail: Any = "Authentication error",
        headers: Optional[Dict[str, str]] = None,
        error_code: str = "ERROR_AUTHENTICATION",
    ):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers=headers,
            error_code=error_code,
        )


class AuthorizationError(AppException):
    """権限エラー用の例外"""

    def __init__(
        self,
        detail: Any = "Permission denied",
        headers: Optional[Dict[str, str]] = None,
        error_code: str = "ERROR_AUTHORIZATION",
    ):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
            headers=headers,
            error_code=error_code,
        )
