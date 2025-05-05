FROM python:3.13-slim

WORKDIR /app

# 必要なシステムパッケージをインストール
RUN apt-get update && apt-get install -y --no-install-recommends \
  gcc \
  libpq-dev \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# バックエンド用の依存パッケージをインストール
COPY requirements/backend.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# アプリケーションコードをコピー
COPY backend/app /app

# 開発環境用の起動コマンド
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]