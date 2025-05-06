# セットアップガイド

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