"""Утилиты для работы с данными из Excel-файла."""
import pandas as pd


def load_transactions(filepath: str) -> pd.DataFrame:
    """
    Загружает транзакции из Excel-файла.

    Args:
        filepath: путь к Excel-файлу

    Returns:
        DataFrame с транзакциями, где 'Дата операции' — datetime
    """
    df = pd.read_excel(filepath)
    df["Дата операции"] = pd.to_datetime(
        df["Дата операции"], format="%d.%m.%Y %H:%M:%S", errors="coerce"
    )
    return df


if __name__ == "__main__":
    df = load_transactions("data/operations.xlsx")
    print("Тип 'Дата операции':", df["Дата операции"].dtype)
    print("\nПервые 3 даты:")
    print(df["Дата операции"].head(3))
    print("\nУникальные категории:", df["Категория"].unique()[:10])
    print("\nСтатусы:", df["Статус"].unique())
    print("\nДиапазон дат:", df["Дата операции"].min(), "—", df["Дата операции"].max())

if __name__ == "__main__":
    from services import cashback_categories  # noqa: E402

    df = load_transactions("data/operations.xlsx")
    result = cashback_categories(df, year=2021, month=12)
    print("\nКешбэк по категориям за декабрь 2021:")
    for cat, amount in sorted(result.items(), key=lambda x: -x[1]):
        print(f"  {cat}: {amount}" )

