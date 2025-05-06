# app/routers/data.py
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.schemas.data import DataUploadResponse
from app.services.embedding import EmbeddingService
from app.models.files import RAGFile
from app.services.storage import StorageService
from app.utils.files import is_valid_file_extension

router = APIRouter(
    prefix="/files",
    tags=["RAG用ファイル"],
)


@router.post("/upload/", response_model=DataUploadResponse)
async def upload_data(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    print(f"Received file: {file.filename}")

    try:
        # ファイル拡張子のチェック
        if not is_valid_file_extension(file.filename):
            raise HTTPException(
                status_code=400, detail="Markdownファイル(.md)のみアップロード可能です"
            )

        content = await file.read()
        text = content.decode("utf-8")

        # Azureストレージにファイルをアップロードするためのサービスを初期化
        storage_service = StorageService()

        # ファイルをAzure Blobストレージにアップロード
        content_type = "text/markdown"  # Markdown用のMIMEタイプを指定
        upload_result = storage_service.upload_file(
            content, file.filename, content_type
        )

        if not upload_result["success"]:
            raise HTTPException(
                status_code=500,
                detail=f"ファイルストレージへのアップロードに失敗しました: {upload_result.get('error')}",
            )

        # UploadedFileモデルを使ってファイル情報をDBに保存
        db_file = RAGFile(
            filename=file.filename,
            blob_url=upload_result["blob_name"],
        )

        db.add(db_file)
        db.commit()
        db.refresh(db_file)  # DBに保存されたファイルの最新情報を取得

        # EmbeddingServiceを使ってファイルを処理
        embedding_service = EmbeddingService(db)
        result = embedding_service.process_file(text, file.filename)

        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["message"])

        return DataUploadResponse(
            filename=file.filename,
            first_100_chars=text[:100],
            message=f"ファイルが正常にアップロードされ、{result['chunks']}チャンクが処理されました",
        )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"ファイル処理中にエラーが発生しました: {str(e)}"
        )


# 他のデータ関連のエンドポイント（例: データの削除、一覧取得など）もここに追加


# 既存のドキュメントを検索するエンドポイント
@router.get("/search/")
async def search_documents(
    query: str,
    limit: int = 5,
    db: Session = Depends(get_db),
):
    try:
        embedding_service = EmbeddingService(db)
        results = embedding_service.similarity_search(query, limit)
        return {"results": results}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"検索処理中にエラーが発生しました: {str(e)}"
        )
