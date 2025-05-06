# app/db/models.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, Text
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector  # pgvectorの型をインポート
from sqlalchemy.dialects.postgresql import JSONB  # JSONB型をインポート
from app.core.db import Base


class RAGFile(Base):
    """RAG用ファイルモデル"""

    __tablename__ = "files"

    # ファイルID
    id = Column(Integer, primary_key=True, index=True)
    # ファイル名
    filename = Column(String, index=True)
    # Azure BlobのURL
    blob_url = Column(String, nullable=False)
    # アップロード日時
    uploaded_at = Column(DateTime, server_default=func.current_timestamp())
    # アップデート日時
    updated_at = Column(DateTime, server_default=func.current_timestamp())

    # チャンクリレーション
    chunks = relationship("Chunk", back_populates="file")


class Chunk(Base):
    """RAG用チャンクモデル"""

    __tablename__ = "chunks"

    # チャンクID
    id = Column(Integer, primary_key=True, index=True)
    # ファイルID
    file_id = Column(Integer, ForeignKey("files.id"))
    # チャンクテキスト
    text = Column(Text)
    # ベクトルデータ
    embedding = Column(Vector(1536))  # ベクトル次元数はモデルによる
    # その他のメタデータ (e.g., page_number, chunk_index)
    chunk_metadata = Column(JSONB, nullable=True, default={})
    # アップロード日時
    uploaded_at = Column(DateTime, server_default=func.current_timestamp())
    # アップデート日時
    updated_at = Column(DateTime, server_default=func.current_timestamp())

    # ファイルリレーション
    file = relationship("RAGFile", back_populates="chunks")
