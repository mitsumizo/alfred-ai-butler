# app/services/embedding.py
import os
import traceback
from typing import List, Dict, Any
from sqlalchemy.orm import Session
import time
from sqlalchemy import select
from app.utils.llm_util import get_embeddings
from app.services.storage import StorageService
from app.models.files import Chunk, RAGFile


class EmbeddingService:
    """テキスト埋め込み（エンベディング）生成と管理を行うサービス"""

    def __init__(self, db: Session):
        self.db = db
        self.storage_service = StorageService()
        self.embedding_type = os.getenv("EMBEDDING_TYPE", "openai")

    def _get_embedding_openai(self, text: str) -> List[float]:
        """OpenAIのEmbedding APIを使用して埋め込みベクトルを生成"""

        # API呼び出し回数制限を考慮して少し待機
        time.sleep(0.5)

        model = get_embeddings(model="text-embedding-3-small")

        response = model.embed_query(text)

        return response

    def _get_embedding_local(self, text: str) -> List[float]:
        """ローカルのSentence Transformerモデルを使用して埋め込みベクトルを生成"""
        embedding = self.model.encode(text)
        return embedding.tolist()

    def get_embedding(self, text: str) -> List[float]:
        """テキストの埋め込みベクトルを生成"""
        if self.embedding_type == "openai":
            return self._get_embedding_openai(text)
        else:
            return self._get_embedding_local(text)

    def chunk_text(
        self, text: str, chunk_size: int = 1000, overlap: int = 200
    ) -> List[str]:
        """テキストを指定サイズのチャンクに分割する効率的な実装"""
        if not text or len(text) == 0:
            return []

        chunks = []

        # 文や段落で分割する自然な区切りを使う
        # 改行で分割してから再結合する方法
        paragraphs = text.split("\n\n")
        current_chunk = ""

        for paragraph in paragraphs:
            # 長すぎる段落は文で分割
            if len(paragraph) > chunk_size:
                sentences = paragraph.replace("\n", " ").split(". ")
                for sentence in sentences:
                    if len(current_chunk) + len(sentence) + 2 <= chunk_size:
                        current_chunk += sentence + ". "
                    else:
                        # チャンクがすでに内容を持っていれば追加
                        if current_chunk:
                            chunks.append(current_chunk.strip())

                        # 文自体が長すぎる場合は強制的に分割
                        if len(sentence) > chunk_size:
                            # 長い文を単語レベルで分割
                            words = sentence.split()
                            current_chunk = ""
                            for word in words:
                                if len(current_chunk) + len(word) + 1 <= chunk_size:
                                    current_chunk += word + " "
                                else:
                                    chunks.append(current_chunk.strip())
                                    current_chunk = word + " "
                        else:
                            current_chunk = sentence + ". "
            else:
                # 段落が追加できるかチェック
                if len(current_chunk) + len(paragraph) + 2 <= chunk_size:
                    current_chunk += paragraph + "\n\n"
                else:
                    # 現在のチャンクを保存して新しいチャンクを開始
                    chunks.append(current_chunk.strip())
                    current_chunk = paragraph + "\n\n"

        # 最後のチャンクを追加
        if current_chunk:
            chunks.append(current_chunk.strip())

        # 空のチャンクを除外
        chunks = [chunk for chunk in chunks if chunk.strip()]

        # チャンクが生成されなかった場合、元のテキストを返す（チャンクサイズより小さい場合）
        if not chunks and text.strip():
            return [text.strip()]

        return chunks

    def process_file(self, text: str, filename: str) -> Dict[str, Any]:
        """アップロードされたファイルを処理し、埋め込みベクトルを生成して保存"""
        try:
            # ファイル名からRAGFileレコードを取得
            file = self.db.query(RAGFile).filter(RAGFile.filename == filename).first()

            if not file:
                return {
                    "success": False,
                    "message": f"ファイル '{filename}' が見つかりません",
                }

            # テキストをチャンクに分割
            chunks = self.chunk_text(text)

            # 各チャンクの埋め込みベクトルを生成してDBに保存
            for i, chunk in enumerate(chunks):
                # 埋め込みベクトルの生成
                embedding = self.get_embedding(chunk)

                # DocumentChunkモデルの作成と保存
                doc_chunk = Chunk(file_id=file.id, text=chunk, embedding=embedding)

                self.db.add(doc_chunk)
                if (i + 1) % 5 == 0 or i == len(chunks) - 1:
                    print(f"進捗: {i + 1}/{len(chunks)} チャンク処理済み")

            # 変更をコミット
            self.db.commit()

            return {
                "success": True,
                "message": f"ファイル '{file.filename}' の処理が完了しました",
                "chunks": len(chunks),
            }

        except Exception as e:
            self.db.rollback()
            traceback.print_exc()
            return {
                "success": False,
                "message": f"ファイル処理中にエラーが発生しました: {str(e)}",
            }

    def similarity_search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        クエリテキストに類似したドキュメントチャンクを検索
        """
        try:
            # クエリの埋め込みベクトルを生成
            query_embedding = self.get_embedding(query)

            # PostgreSQLのpgvectorを使った類似度検索
            # ベクトル類似度に基づいて上位N件を取得
            # SQLAlchemy の表現内で、pgvector.sqlalchemy.Vector 型が提供する <=> 演算子を使用
            stmt = (
                select(
                    Chunk,
                    Chunk.embedding.cosine_distance(query_embedding).label("distance"),
                )  # Chunk オブジェクトとコサイン距離を選択
                .order_by(
                    Chunk.embedding.cosine_distance(query_embedding).desc()
                )  # コサイン距離で降順に並べ替え
                .limit(limit)  # 上位k件を取得
            )

            results = self.db.execute(stmt).all()

            # 結果をフォーマット
            formatted_results = []
            for result in results:
                chunk = result[0]  # Chunkオブジェクト
                distance = result[1]  # コサイン距離

                # ファイル情報を取得
                file = (
                    self.db.query(RAGFile).filter(RAGFile.id == chunk.file_id).first()
                )
                source = file.filename if file else "不明"

                formatted_results.append(
                    {
                        "source": source,
                        "text": chunk.text,
                        "id": str(chunk.id),
                        "distance": float(distance),
                    }
                )

            return formatted_results

        except Exception as e:
            traceback.print_exc()
            print(f"検索処理中にエラーが発生しました: {str(e)}")
            return []
