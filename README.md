# AI Tutor - インタラクティブ学習プラットフォーム

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Last Updated](https://img.shields.io/badge/Last%20Updated-2025--05--06_170806-informational)](CHANGELOG.md)

AIを活用したインタラクティブな学習プラットフォームです。プログラミング学習をパーソナライズされた体験で進めることができます。

## 目次

- [機能要件](#機能要件)
- [使用技術](#使用技術)
- [プロジェクト構造](#プロジェクト構造)
- [セットアップガイド](#セットアップガイド)
- [API仕様](#api仕様)

## プロジェクト構造

- **.vscode/**
  - launch.json
- **backend/**
  - **app/**
    - **api/**
      - __init__.py
      - chat.py
      - settings.py
    - **core/**
      - config.py
      - db.py
      - events.py
    - **exceptions/**
      - __init__.py
      - base.py
      - handlers.py
      - http.py
    - **models/**
      - documents.py
      - files.py
      - uploaded_file.py
    - **routers/**
      - __init__.py
      - base.py
      - chat.py
      - files.py
      - settings.py
    - **schemas/**
      - auth.py
      - chat.py
      - data.py
      - settings.py
    - **services/**
      - embedding.py
      - storage.py
    - **utils/**
      - files.py
      - llm_util.py
    - main.py
  - **tests/**
  - **uploads/**
  - requirements.txt
- **docker/**
  - backend.Dockerfile
  - frontend.Dockerfile
- **frontend/**
  - **assets/**
  - **components/**
    - __init__.py
    - chat.py
    - settings.py
  - **utils/**
    - __init__.py
    - api.py
  - app.py
- **memory/**
  - api_docs.md
  - development_setup.md
  - features.md
  - functionality.md
  - last_update.md
  - project_overview.md
  - project_structure.md
  - setup_guide.md
  - tech_stack.md
- **requirements/**
  - backend.txt
  - base.txt
  - frontend.txt
  - requirements.txt
- **tasks/**
  - **git_hooks/**
    - post-commit
  - install_git_hooks.py
  - README_RE_WRITE.md
  - schedule_readme_update.py
  - update_readme.py
- .env
- .env.example
- .python-version
- docker-compose.yml
- pyproject.toml
- README.md

## 機能要件

## コア機能（MVP）
| 機能ID | 機能名         | 要件詳細                                                                         | 優先度 |
| ------ | -------------- | -------------------------------------------------------------------------------- | ------ |
| F2     | 設定資料の記憶 | - テキストファイルの読み込み<br>- チャンク分割とベクトル化<br>- pgvectorへの保存 | 高     |
| F3     | ユーザー入力   | - チャット形式での質問入力<br>- 自然言語での問い合わせ                           | 高     |
| F4     | AI応答         | - Langchain Agentによる応答生成<br>- 人間らしい文章での返答                      | 高     |
| F5     | RAG機能        | - 設定資料の参照<br>- 正確な情報に基づく応答                                     | 高     |

## 拡張機能
| 機能ID | 機能名     | 要件詳細                                                 | 優先度 |
| ------ | ---------- | -------------------------------------------------------- | ------ |
| F1     | チャットUI | - シンプルなチャットインターフェース<br>- 会話履歴の表示 | 中     |
| F6     | 会話記憶   | - 文脈理解<br>- 前回の会話を踏まえた応答                 | 中     |
| F7     | 追加機能   | - 計算ツール<br>- ランダム応答機能                       | 中     |

## 使用技術

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

## セットアップガイド

## 前提条件
- Python 3.9以上
- Docker および Docker Compose
- Node.js 16以上（フロントエンド開発用）

## インストール手順

### 1. リポジトリのクローン
```bash
git clone https://github.com/yourusername/ai_tutor.git
cd ai_tutor
```

### 2. バックエンド環境構築（Python）
```bash
# 仮想環境作成
python -m venv .venv

# 仮想環境アクティベート
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# 依存パッケージインストール
pip install -r requirements/dev.txt
```

### 3. フロントエンド環境構築
```bash
cd frontend
npm install
```

### 4. Dockerを使った開発環境起動
```bash
docker-compose up -d
```

### 5. アプリケーション起動
```bash
# バックエンド起動
cd backend
python manage.py runserver

# 別ターミナルでフロントエンド起動
cd frontend
npm run dev
```

## 環境変数設定
`.env`ファイルをプロジェクトルートに作成し、以下の設定を行ってください：

```
API_KEY=your_api_key
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
DEBUG=True
```

## API仕様

## ユーザー認証API

| API名        | エンドポイント   | メソッド | 役割                       |
| ------------ | ---------------- | -------- | -------------------------- |
| ユーザー登録 | `/auth/register` | POST     | 新規ユーザーアカウント作成 |
| ログイン     | `/auth/login`    | POST     | ユーザー認証とトークン発行 |
| ログアウト   | `/auth/logout`   | POST     | 現在のセッションを終了     |
| トークン更新 | `/auth/refresh`  | POST     | アクセストークンの更新     |

## 設定資料API

| API名                    | エンドポイント              | メソッド | 役割                                 |
| ------------------------ | --------------------------- | -------- | ------------------------------------ |
| 設定ファイル一覧取得     | `/settings/files`           | GET      | 保存済み設定ファイル一覧の取得       |
| 設定ファイルアップロード | `/settings/upload`          | POST     | 新規設定ファイルのアップロードと処理 |
| 設定ファイル取得         | `/settings/files/{file_id}` | GET      | 特定の設定ファイル内容の取得         |
| 設定ファイル更新         | `/settings/files/{file_id}` | PUT      | 既存設定ファイルの内容更新           |
| 設定ファイル削除         | `/settings/files/{file_id}` | DELETE   | 設定ファイルの削除                   |
| 設定カテゴリ作成         | `/settings/categories`      | POST     | 設定ファイルのカテゴリ作成           |
| 設定カテゴリ一覧         | `/settings/categories`      | GET      | 設定ファイルカテゴリ一覧取得         |

## チャットAPI

| API名                | エンドポイント  | メソッド | 役割                             |
| -------------------- | --------------- | -------- | -------------------------------- |
| メッセージ送信       | `/chat/message` | POST     | ユーザーメッセージ送信と応答取得 |
| 会話履歴取得         | `/chat/history` | GET      | 過去の会話履歴の取得             |
| 会話履歴削除         | `/chat/history` | DELETE   | 会話履歴の削除                   |
| 会話コンテキスト設定 | `/chat/context` | POST     | チャットの文脈情報の設定         |
| 会話開始             | `/chat/start`   | POST     | 新規会話セッションの開始         |
| 会話終了             | `/chat/end`     | POST     | 現在の会話セッションの終了       |

## 執事キャラクターAPI

| API名            | エンドポイント    | メソッド | 役割                       |
| ---------------- | ----------------- | -------- | -------------------------- |
| 執事設定取得     | `/butler/profile` | GET      | 執事の人格設定情報取得     |
| 執事設定更新     | `/butler/profile` | PUT      | 執事の人格設定の更新       |
| 対応スタイル一覧 | `/butler/styles`  | GET      | 使用可能な応対スタイル一覧 |
| 対応スタイル変更 | `/butler/style`   | PUT      | 執事の対応スタイル変更     |

## 管理API
| API名            | エンドポイント           | メソッド | 役割                         |
| ---------------- | ------------------------ | -------- | ---------------------------- |
| システム状態     | `/admin/status`          | GET      | システムの稼働状態確認       |
| ベクトルDB再構築 | `/admin/rebuild-vectors` | POST     | ベクトルデータベースの再構築 |
| 使用統計         | `/admin/stats`           | GET      | 使用状況の統計情報取得       |
| キャッシュクリア | `/admin/clear-cache`     | POST     | システムキャッシュのクリア   |

## 検索API
| API名          | エンドポイント    | メソッド | 役割                   |
| -------------- | ----------------- | -------- | ---------------------- |
| 設定情報検索   | `/search`         | POST     | 設定情報の検索         |
| 類似文書検索   | `/search/similar` | POST     | 類似文書の検索         |
| キーワード検索 | `/search/keyword` | POST     | キーワードベースの検索 |

各APIはJSONフォーマットでデータをやり取りし、認証が必要なエンドポイントではリクエストヘッダーに`Authorization: Bearer {token}`の形式でアクセストークンを含める設計です。

バックエンドAPIは FastAPI で実装され、以下のエンドポイントが提供されています。
ベースURL: `http://localhost:8000`

## チャットAPI

### メッセージ送信
- **エンドポイント**: `/chat`
- **メソッド**: POST
- **説明**: ユーザーのメッセージに対してAI執事として応答します
- **リクエスト本文**:
  ```json
  {
    "message": "ユーザーからの質問やメッセージ"
  }
  ```
- **レスポンス**:
  ```json
  {
    "response": "AI執事からの応答メッセージ",
    "source_documents": [
      {
        "content": "参照された設定資料の内容",
        "metadata": {
          "source": "設定ファイル名/ID"
        }
      }
    ]
  }
  ```

## 設定API

### 設定ファイルのアップロード
- **エンドポイント**: `/settings/upload`
- **メソッド**: POST
- **説明**: 設定ファイルの内容をアップロードし、ベクトルデータベースに保存します
- **リクエスト本文**:
  ```json
  {
    "content": "設定ファイルのテキスト内容"
  }
  ```
- **レスポンス**:
  ```json
  {
    "success": true,
    "message": "設定ファイルが正常に処理されました",
    "content_length": 1234
  }
  ```

## エラーレスポンス

すべてのエンドポイントは、エラー発生時に以下の形式でレスポンスを返します：

```json
{
  "detail": "エラーメッセージの詳細"
}
```

主なHTTPステータスコード：
- 400: リクエストの形式が不正
- 404: リソースが見つからない
- 500: サーバー内部エラー

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細は[LICENSE](LICENSE)ファイルを参照してください。
