# app/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# .env ファイルから環境変数を読み込む
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../../.env"))

# 環境変数が見つからない場合はデフォルト値を使用
# ホスト名を「postgres」から「localhost」に変更
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://postgres:password@localhost:5432/tutordb"
)


print(f"Database URL: {DATABASE_URL}")  # 接続文字列を表示（デバッグ用）

# SQLAlchemy エンジンを作成
# connect_args={"check_same_thread": False} は SQLite の場合に必要な設定ですが、
# PostgreSQLでも警告回避などのためにつける場合があります。
# PostgreSQLでは通常不要ですが、念のため記述例として残しておきます。
engine = create_engine(DATABASE_URL)

# セッションメーカーを作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# データベースモデルのベースクラスを作成
Base = declarative_base()


# DBセッションを取得するためのDependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# テーブルをドロップして再作成する関数 (開発用)
def drop_and_create_tables():
    try:
        print("Dropping database tables...")
        Base.metadata.drop_all(bind=engine)
        print("Database tables dropped.")

        print("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        print("Database tables created.")
    except Exception as e:
        print(f"Error in drop_and_create_tables: {e}")
        print("Continuing without dropping/creating tables...")


# アプリケーション起動時に接続確認とテーブル作成を行う関数
def init_db():
    print("Initializing database...")
    # 接続確認
    try:
        with engine.connect():
            print("Database connection successful!")
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False

    # テーブル作成
    try:
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully.")
        return True
    except Exception as e:
        print(f"Error creating tables: {e}")
        return False


# アプリケーション起動時にテーブルを作成する場合は main.py から呼び出す
# from .database import create_tables
# @app.on_event("startup")
# async def startup_event():
#     print("Application startup...")
#     create_tables() # テーブル作成関数を呼び出す
#     # 既存のDB接続確認ロジックもここに統合
#     try:
#         with engine.connect() as connection:
#             print("Database connection successful!")
#     except Exception as e:
#         print(f"Database connection failed: {e}")
#         # 起動を停止したい場合は raise e
