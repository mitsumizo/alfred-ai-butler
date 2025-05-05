FROM python:3.13-slim

WORKDIR /app

# 必要なシステムパッケージをインストール
RUN apt-get update && apt-get install -y --no-install-recommends \
  gcc \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# フロントエンド用の依存パッケージをインストール
COPY ../requirements/frontend.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# アプリケーションコードをコピー
COPY . /app

# Streamlitアプリケーションを起動
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

