from pydantic import BaseModel
from typing import Optional


class DataUploadResponse(BaseModel):
    """データアップロードのレスポンスモデル"""

    # ファイル名
    filename: str
    # ファイルの最初の100文字
    first_100_chars: str
    # 成功フラグ
    success: bool = True
    # メッセージ
    message: Optional[str] = None
