# app/main.py
from fastapi import FastAPI, HTTPException

# 設定とイベントハンドラーのインポート
from app.core.config import APP_SETTINGS
from app.core.events import startup_event, shutdown_event
from app.exceptions import (
    AppException,
    app_exception_handler,
    http_exception_handler,
    unhandled_exception_handler,
)

# ルーターのインポート
from app.routers.base import router as base_router
from app.routers.files import router as file_router
from app.routers.chat import router as chat_router

# FastAPI アプリケーションのインスタンスを作成
application = FastAPI(
    title=APP_SETTINGS["title"],
    description=APP_SETTINGS["description"],
    version=APP_SETTINGS["version"],
)


# 例外ハンドラーの登録
application.add_exception_handler(AppException, app_exception_handler)
application.add_exception_handler(HTTPException, http_exception_handler)
application.add_exception_handler(Exception, unhandled_exception_handler)


# アプリケーション起動・終了イベント設定
application.add_event_handler("startup", startup_event)
application.add_event_handler("shutdown", shutdown_event)


# ルーターをアプリケーションに含める
application.include_router(base_router)  # 基本ルートとヘルスチェック用ルーター
application.include_router(file_router)
application.include_router(chat_router)
