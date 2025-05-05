# AI執事チャットボット「執事アルフレッド」

## 1. プロジェクト概要

### 1.1 目的

- ユーザーが用意した設定資料（テキストファイル）に基づいて対話するAI執事の開発
- 最新技術（FastAPI, Streamlit, Langchain, pgvector）を活用した実践的な学習
- パーソナルなデータを活用した愛着の湧くアプリケーション開発

### 1.2 システム構成

- バックエンド: FastAPI
- フロントエンド: Streamlit
- AIエンジン: Langchain Agent
- データベース: PostgreSQL + pgvector
- コンテナ化: Docker

## 2. プロジェクト構成

```
ai_tutor/                     # プロジェクトルートディレクトリ
│
├── backend/                  # バックエンド（FastAPI）
│   └── app/                  # FastAPIアプリケーション
│       ├── api/              # APIエンドポイント
│       │   ├── __init__.py
│       │   ├── chat.py       # チャットエンドポイント
│       │   └── settings.py   # 設定エンドポイント
│       │
│       ├── core/             # コア機能
│       │   └── __init__.py
│       │
│       ├── db/               # データベース関連
│       │   └── __init__.py
│       │
│       ├── services/         # ビジネスロジック
│       │   └── __init__.py
│       │
│       ├── utils/            # ユーティリティ
│       │   └── __init__.py
│       │
│       └── main.py           # FastAPIアプリケーションエントリーポイント
│
├── frontend/                 # フロントエンド（Streamlit）
│   ├── app.py                # メインのStreamlitアプリ
│   ├── components/           # UIコンポーネント
│   │   ├── __init__.py
│   │   ├── chat.py           # チャットUI
│   │   └── settings.py       # 設定UI
│   │
│   ├── utils/                # フロントエンド用ユーティリティ
│   │   ├── __init__.py
│   │   └── api.py            # API通信
│   │
│   └── assets/               # 静的ファイル
│
├── docker/                   # Docker関連ファイル
│   ├── backend.Dockerfile    # バックエンド用Dockerfile
│   └── frontend.Dockerfile   # フロントエンド用Dockerfile
│
├── requirements/              # 依存関係
│   ├── base.txt              # 共通の依存パッケージ
│   ├── backend.txt           # バックエンド用依存パッケージ
│   └── frontend.txt          # フロントエンド用依存パッケージ
│
├── .env-example              # 環境変数サンプル
├── .gitignore                # Gitの無視設定
└── docker-compose.yml        # Dockerコンテナ構成
```

## 3. 機能要件

### 3.1 コア機能（MVP）
| 機能ID | 機能名         | 要件詳細                                                                         | 優先度 |
| ------ | -------------- | -------------------------------------------------------------------------------- | ------ |
| F2     | 設定資料の記憶 | - テキストファイルの読み込み<br>- チャンク分割とベクトル化<br>- pgvectorへの保存 | 高     |
| F3     | ユーザー入力   | - チャット形式での質問入力<br>- 自然言語での問い合わせ                           | 高     |
| F4     | AI応答         | - Langchain Agentによる応答生成<br>- 人間らしい文章での返答                      | 高     |
| F5     | RAG機能        | - 設定資料の参照<br>- 正確な情報に基づく応答                                     | 高     |

### 3.2 拡張機能
| 機能ID | 機能名     | 要件詳細                                                 | 優先度 |
| ------ | ---------- | -------------------------------------------------------- | ------ |
| F1     | チャットUI | - シンプルなチャットインターフェース<br>- 会話履歴の表示 | 中     |
| F6     | 会話記憶   | - 文脈理解<br>- 前回の会話を踏まえた応答                 | 中     |
| F7     | 追加機能   | - 計算ツール<br>- ランダム応答機能                       | 中     |

## 4. 開発環境の起動方法

1. 環境変数の設定
```bash
cp .env-example .env
# .envファイルを編集して必要な値を設定
```

2. Dockerコンテナの起動
```bash
docker-compose up -d
```

3. アプリケーションへのアクセス
   - FastAPI: http://localhost:8000
   - Streamlit: http://localhost:8501
   - pgAdmin: http://localhost:5050

## 5. 開発環境構築（ローカル開発用）

### 5.1 バックエンド開発環境

```bash
# Python 仮想環境を作成
python -m venv backend_venv

# 仮想環境をアクティベート
# Windows
backend_venv\Scripts\activate
# Unix/Mac
source backend_venv/bin/activate

# 依存パッケージのインストール
pip install -r requirements/backend.txt

# 開発サーバーの起動
cd backend
uvicorn app.main:app --reload
```

### 5.2 フロントエンド開発環境

```bash
# Python 仮想環境を作成
python -m venv frontend_venv

# 仮想環境をアクティベート
# Windows
frontend_venv\Scripts\activate
# Unix/Mac
source frontend_venv/bin/activate

# 依存パッケージのインストール
pip install -r requirements/frontend.txt

# 開発サーバーの起動
cd frontend
streamlit run app.py
```