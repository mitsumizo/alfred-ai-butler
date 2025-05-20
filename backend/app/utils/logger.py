"""
ロギングユーティリティモジュール

アプリケーション全体で一貫したログ出力を行うためのユーティリティ関数を提供します。
"""

from app.core.logging import get_logger


def get_module_logger(module_name):
    """
    指定したモジュール名のロガーを取得する関数

    Args:
        module_name: ロガー名（通常は __name__ を使用）

    Returns:
        logging.Logger: 設定済みのロガーインスタンス

    Example:
        ```python
        from app.utils.logger import get_module_logger

        logger = get_module_logger(__name__)
        logger.info("情報ログ")
        logger.warning("警告ログ")
        logger.error("エラーログ")
        ```
    """
    return get_logger(module_name)


# 共通ロガーのエクスポート（シンプルなログ出力用）
logger = get_module_logger("app")


def log_function_call(func):
    """
    関数呼び出しをログに記録するデコレータ

    Args:
        func: デコレート対象の関数

    Returns:
        wrapper: ラッパー関数

    Example:
        ```python
        from app.utils.logger import log_function_call

        @log_function_call
        def my_function(arg1, arg2):
            return arg1 + arg2
        ```
    """
    module_logger = get_module_logger(func.__module__)

    def wrapper(*args, **kwargs):
        module_logger.debug(
            f"関数呼び出し: {func.__name__}(args={args}, kwargs={kwargs})"
        )
        try:
            result = func(*args, **kwargs)
            module_logger.debug(f"関数終了: {func.__name__} -> {result}")
            return result
        except Exception as e:
            module_logger.exception(f"関数エラー: {func.__name__} -> {e}")
            raise

    return wrapper


def log_startup(message="アプリケーション起動"):
    """アプリケーション起動時のログを出力する関数"""
    logger.info("=" * 50)
    logger.info(message)
    logger.info("=" * 50)


def log_shutdown(message="アプリケーション終了"):
    """アプリケーション終了時のログを出力する関数"""
    logger.info("=" * 50)
    logger.info(message)
    logger.info("=" * 50)
