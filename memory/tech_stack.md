# 技術スタック

## バックエンド
- **フレームワーク**: FastAPI 0.115.12
- **サーバー**: Uvicorn 0.34.2
- **データ検証**: Pydantic 2.11.4
- **設定管理**: Pydantic Settings 2.9.1
- **ORM**: SQLAlchemy 2.0.40
- **データベースドライバ**: psycopg2-binary 2.9.10
- **環境変数管理**: python-dotenv 1.1.0
- **ベクトルデータベース**: pgvector 0.4.1

## AIエンジン
- **フレームワーク**: Langchain 0.3.25
  - langchain-community 0.3.23
  - langchain-core 0.3.58
  - langchain-openai 0.3.16
  - langchain-text-splitters 0.3.8
- **LLM**: OpenAI 1.77.0
- **トークン化**: Tiktoken 0.9.0
- **リトライ処理**: Tenacity 8.1.0+

## フロントエンド
- **フレームワーク**: Streamlit 1.36.0
- **HTTP クライアント**: Requests 2.32.3
- **環境変数管理**: python-dotenv 1.1.0
- **リトライ処理**: Tenacity 8.1.0+

## データベース
- **主データベース**: PostgreSQL
- **ベクトル拡張**: pgvector

## 開発・運用
- **コンテナ化**: Docker & Docker Compose
- **開発環境**: Python 仮想環境 (venv)
- **データベース管理**: pgAdmin 4 