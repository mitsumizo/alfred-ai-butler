import sqlalchemy
from app.core.db import engine, init_db


async def startup_event():
    """アプリケーション起動時に実行される処理"""
    print("Application startup...")
    # データベース接続確認
    try:
        with engine.connect():
            print("Database connection successful!")
            init_db()
    except Exception as e:
        print(f"Database connection failed: {e}")
        # デバッグ中はここで raise e を有効にすると、DB接続失敗時にコンテナが起動しない
        # raise e # 本番環境ではエラーログを出力して続行するなど検討


async def shutdown_event():
    """アプリケーション終了時に実行される処理"""
    print("Application shutdown...")
    # DB接続プールのクローズなど、必要に応じて追加
    if engine:
        engine.dispose()


async def health_check():
    """ヘルスチェック用の関数"""
    try:
        with engine.connect() as connection:
            # 簡単なクエリを実行して接続が生きているか確認
            connection.execute(sqlalchemy.text("SELECT 1"))
            db_status = "ok"
        return {"status": "ok", "database_connection": db_status}
    except Exception:
        return {"status": "warning", "database_connection": "failed"}
