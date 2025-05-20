import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

from app.core.config import LOG_SETTINGS


def setup_logging():
    """
    アプリケーションのログ設定を初期化する関数

    環境変数やconfigから設定を読み込み、ログハンドラーを設定します。
    """
    # ルートロガーの取得
    logger = logging.getLogger()

    # 既存のハンドラーをクリア（二重登録防止）
    if logger.handlers:
        for handler in logger.handlers:
            logger.removeHandler(handler)

    # ログレベルの設定
    log_level = getattr(logging, LOG_SETTINGS["level"])
    logger.setLevel(log_level)

    # ログフォーマットの設定
    log_format = logging.Formatter(
        fmt=LOG_SETTINGS["format"], datefmt=LOG_SETTINGS["date_format"]
    )

    # コンソールへの出力設定
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_format)
    logger.addHandler(console_handler)

    # ファイルへの出力設定（設定されている場合のみ）
    if LOG_SETTINGS["file_enabled"]:
        # ログディレクトリの作成（存在しない場合）
        log_dir = Path(LOG_SETTINGS["file_dir"])
        log_dir.mkdir(parents=True, exist_ok=True)

        # ログファイルパスの設定
        log_file_path = log_dir / LOG_SETTINGS["file_name"]

        # ローテーティングファイルハンドラーの設定
        file_handler = RotatingFileHandler(
            filename=log_file_path,
            maxBytes=LOG_SETTINGS["max_size"],
            backupCount=LOG_SETTINGS["backup_count"],
            encoding="utf-8",
        )
        file_handler.setFormatter(log_format)
        logger.addHandler(file_handler)

    # 初期化完了ログ
    logging.info("Logging system initialized")
    if LOG_SETTINGS["file_enabled"]:
        logging.info(f"Log file: {log_file_path}")

    return logger


def get_logger(name):
    """
    指定した名前のロガーを取得する関数

    Args:
        name: ロガー名（通常はモジュール名 __name__ を使用）

    Returns:
        logging.Logger: 設定済みのロガーインスタンス
    """
    return logging.getLogger(name)
