# backend/app/main.py
import os
from fastapi import FastAPI
from dotenv import load_dotenv
import sqlalchemy
from app.api import chat, settings

# .env ファイルから環境変数を読み込む
load_dotenv()

# FastAPI アプリケーションのインスタンスを作成
app = FastAPI(
    title="AI Butler Alfred API",
    description="User-configured AI butler chatbot API",
    version="0.1.0",
)

# ルーターを追加
app.include_router(chat.router)
app.include_router(settings.router)

# データベース接続URLを取得
DATABASE_URL = os.getenv("DATABASE_URL")


# データベース接続の確認
@app.on_event("startup")
async def startup_db_client():
    print(f"Attempting to connect to database: {DATABASE_URL}")
    try:
        engine = sqlalchemy.create_engine(DATABASE_URL)
        # connectionを試みる
        with engine.connect():
            print("Database connection successful!")
    except Exception as e:
        print(f"Database connection failed: {e}")


@app.on_event("shutdown")
async def shutdown_db_client():
    # アプリケーション終了時の処理
    pass


# 基本的な疎通確認用エンドポイント
@app.get("/")
async def read_root():
    return {"message": "AI Butler Alfred API is running!"}


@app.get("/health")
async def health_check():
    return {"status": "ok", "database_connection": "check_startup_logs"}
