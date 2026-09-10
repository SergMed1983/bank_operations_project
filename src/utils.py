"""Утилиты для работы с данными из Excel-файла."""
import pandas as pd


def load_transactions(filepath: str) -> pd.DataFrame:
    """
    Загружает транзакции из Excel-файла.

    Args:
        filepath: путь к Excel-файлу

    Returns:
        DataFrame с транзакциями
    """
    return pd.read_excel(filepath)
