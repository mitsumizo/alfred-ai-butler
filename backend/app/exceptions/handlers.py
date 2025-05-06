from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from .base import AppException


async def app_exception_handler(request: Request, exc: AppException):
    """アプリケーション例外のハンドラー"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.error_code,
                "message": exc.detail,
                "status": exc.status_code
            }
        }
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    """標準HTTPException用のハンドラー"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": "HTTP_ERROR",
                "message": exc.detail,
                "status": exc.status_code
            }
        }
    )


async def unhandled_exception_handler(request: Request, exc: Exception):
    """未処理の例外をキャッチするハンドラー"""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "Internal server error has occurred",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR
            }
        }
    ) 