def is_valid_file_extension(
    filename: str, allowed_extensions: list[str] = [".md"]
) -> bool:
    """
    ファイルの拡張子が許可されたものかどうかをチェックする

    Args:
        filename (str): チェックするファイル名
        allowed_extensions (list[str], optional): 許可する拡張子のリスト. デフォルトは [".md"]

    Returns:
        bool: 拡張子が許可されている場合はTrue、そうでない場合はFalse
    """
    return any(filename.lower().endswith(ext) for ext in allowed_extensions)
