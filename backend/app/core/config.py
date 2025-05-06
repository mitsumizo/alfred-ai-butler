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
