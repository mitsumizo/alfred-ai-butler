# app/services/storage.py
import os
from azure.storage.blob import BlobServiceClient, ContentSettings
import uuid
import traceback


class StorageService:
    def __init__(self):
        # Azuriteに接続するための接続文字列
        # Docker環境では'azurite'、ローカル環境では'localhost'を使用
        host = os.environ.get("STORAGE_HOST", "localhost")

        connect_str = os.getenv(
            "AZURE_STORAGE_CONNECTION_STRING",
            f"DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://{host}:10000/devstoreaccount1;",
        )

        print(f"Azurite接続先: http://{host}:10000")

        try:
            # BlobServiceClientの作成
            self.blob_service_client = BlobServiceClient.from_connection_string(
                connect_str
            )

            # コンテナ名
            self.container_name = os.getenv("AZURE_STORAGE_CONTAINER", "documents")

            # コンテナが存在することを確認
            self._ensure_container_exists()
        except Exception as e:
            print(f"Azurite接続中にエラーが発生しました: {str(e)}")
            traceback.print_exc()
            # 初期化エラーでもサービスは続行できるようにする
            self.blob_service_client = None

    def _ensure_container_exists(self):
        """コンテナが存在しない場合は作成する"""
        try:
            if not self.blob_service_client:
                print(
                    "BlobServiceClientが初期化されていないため、コンテナ作成をスキップします"
                )
                return

            container_client = self.blob_service_client.get_container_client(
                self.container_name
            )
            if not container_client.exists():
                container_client = self.blob_service_client.create_container(
                    self.container_name
                )
                print(f"コンテナ '{self.container_name}' を作成しました")
        except Exception as e:
            print(f"コンテナの確認/作成中にエラーが発生しました: {str(e)}")
            traceback.print_exc()
            raise

    def upload_file(self, file_content, filename, content_type=None):
        """ファイルをAzure Blob Storageにアップロード"""
        try:
            if not self.blob_service_client:
                print(
                    "BlobServiceClientが初期化されていないため、アップロードをスキップします"
                )
                return {"success": False, "error": "ストレージサービスが利用できません"}

            # ユニークなBLOB名を生成
            uuid_str = str(uuid.uuid4())
            blob_name = f"{uuid_str}_{filename}"

            # BLOBクライアントを取得
            blob_client = self.blob_service_client.get_blob_client(
                container=self.container_name, blob=blob_name
            )

            # コンテンツタイプの設定（オプション）
            content_settings = None
            if content_type:
                content_settings = ContentSettings(content_type=content_type)

            # ファイルをアップロード
            blob_client.upload_blob(
                file_content, content_settings=content_settings, overwrite=True
            )

            # BLOBのURLを返す
            return {
                "success": True,
                "blob_name": blob_name,
                "url": blob_client.url,
                "uuid": uuid_str,
            }

        except Exception as e:
            print(f"ファイルアップロード中にエラーが発生しました: {str(e)}")
            traceback.print_exc()
            return {"success": False, "error": str(e)}

    def download_file(self, blob_name):
        """Azure Blob Storageからファイルをダウンロード"""
        try:
            if not self.blob_service_client:
                print(
                    "BlobServiceClientが初期化されていないため、ダウンロードをスキップします"
                )
                return {"success": False, "error": "ストレージサービスが利用できません"}

            # BLOBクライアントを取得
            blob_client = self.blob_service_client.get_blob_client(
                container=self.container_name, blob=blob_name
            )

            # BLOBをダウンロード
            download_stream = blob_client.download_blob()

            return {
                "success": True,
                "content": download_stream.readall(),
            }

        except Exception as e:
            print(f"ファイルダウンロード中にエラーが発生しました: {str(e)}")
            traceback.print_exc()
            return {"success": False, "error": str(e)}

    def delete_file(self, blob_name):
        """Azure Blob Storageからファイルを削除"""
        try:
            if not self.blob_service_client:
                print("BlobServiceClientが初期化されていないため、削除をスキップします")
                return {"success": False, "error": "ストレージサービスが利用できません"}

            # BLOBクライアントを取得
            blob_client = self.blob_service_client.get_blob_client(
                container=self.container_name, blob=blob_name
            )

            # BLOBを削除
            blob_client.delete_blob()

            return {
                "success": True,
                "message": f"ファイル '{blob_name}' を削除しました",
            }

        except Exception as e:
            print(f"ファイル削除中にエラーが発生しました: {str(e)}")
            traceback.print_exc()
            return {"success": False, "error": str(e)}
