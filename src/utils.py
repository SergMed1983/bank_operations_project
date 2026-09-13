"""Утилиты для работы с данными из Excel-файла."""

import pandas as pd


def load_transactions(filepath: str) -> pd.DataFrame:
    """..."""
    df = pd.read_excel(filepath)
    df["Дата операции"] = pd.to_datetime(
        df["Дата операции"], format="%d.%m.%Y %H:%M:%S", errors="coerce"
    )
    return df
