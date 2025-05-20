import sqlalchemy
from app.core.db import engine, init_db
from app.core.logging import setup_logging
from app.utils.logger import logger, log_startup, log_shutdown


async def startup_event():
    """アプリケーション起動時に実行される処理"""
    # ログシステムの初期化
    setup_logging()

    # アプリケーション起動ログ
    log_startup("AI Butler Alfred API 起動中...")

    # データベース接続確認
    try:
        with engine.connect():
            logger.info("データベース接続成功")
            init_db()
    except Exception as e:
        logger.error(f"データベース接続失敗: {e}")
        # デバッグ中はここで raise e を有効にすると、DB接続失敗時にコンテナが起動しない
        # raise e # 本番環境ではエラーログを出力して続行するなど検討


async def shutdown_event():
    """アプリケーション終了時に実行される処理"""
    log_shutdown("AI Butler Alfred API 終了中...")
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
        logger.debug("ヘルスチェック: OK")
        return {"status": "ok", "database_connection": db_status}
    except Exception as e:
        logger.warning(f"ヘルスチェック失敗: {e}")
        return {"status": "warning", "database_connection": "failed"}
