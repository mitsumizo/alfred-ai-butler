import os
from dotenv import load_dotenv

# .env ファイルから環境変数を読み込む（2階層上の.envファイルを指定）
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../../.env"))

# データベース接続URL
DATABASE_URL = os.getenv("DATABASE_URL")

# アプリケーション設定
APP_SETTINGS = {
    "title": "AI Butler Alfred API",
    "description": "User-configured AI butler chatbot API",
    "version": "0.1.0",
}

# ログ設定
LOG_SETTINGS = {
    # ログレベル（DEBUG, INFO, WARNING, ERROR, CRITICAL）
    "level": os.getenv("LOG_LEVEL", "INFO"),
    # ログフォーマット
    "format": os.getenv(
        "LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    ),
    "date_format": os.getenv("LOG_DATE_FORMAT", "%Y-%m-%d %H:%M:%S"),
    # ファイルログの設定
    "file_enabled": os.getenv("LOG_FILE_ENABLED", "true").lower() == "true",
    "file_dir": os.getenv("LOG_FILE_DIR", "logs"),
    "file_name": os.getenv("LOG_FILE_NAME", "app.log"),
    # ローテーション設定（10MBごとにローテーション、5世代まで保存）
    "max_size": int(os.getenv("LOG_MAX_SIZE", 10 * 1024 * 1024)),  # 10MB
    "backup_count": int(os.getenv("LOG_BACKUP_COUNT", 5)),
}
