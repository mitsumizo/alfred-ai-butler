# app/models.py
import uuid
from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector  # pgvectorのVector型をインポート

from app.db import Base


# ベクトルデータを保存するテーブルのモデル
class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    # UUIDを主キーとする
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    # 元のドキュメントやファイル名などを保存するカラム (オプション)
    source = Column(String, index=True)
    # テキストチャンクの内容
    text = Column(Text)
    # ベクトルデータ。今回は1536次元（OpenAI Embeddingsのデフォルト次元数）を想定
    embedding = Column(
        Vector(1536)
    )  # 使用するEmbeddingモデルの次元数に合わせて変更してください

    def __repr__(self):
        return f"<DocumentChunk(source='{self.source}', text='{self.text[:50]}...')>"


# 必要であれば、他のテーブルモデルもここに追加します
# 例: 会話履歴など
# class ConversationHistory(Base):
#     __tablename__ = "conversation_history"
#     id = Column(Integer, primary_key=True, index=True)
#     user_message = Column(Text)
#     ai_response = Column(Text)
#     timestamp = Column(DateTime, default=datetime.datetime.utcnow)
