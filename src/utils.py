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
    from reports import spending_by_category  # noqa: E402

    df = load_transactions("data/operations.xlsx")

    result = spending_by_category(df, category="Супермаркеты", date="2021-12-31")
    print("\nТраты по категории 'Супермаркеты' за последние 3 месяца:")
    print(f"Количество транзакций: {len(result)}")
    print(f"Общая сумма: {result['Сумма операции'].sum():.2f} руб.")
    print("\nПервые 5 транзакций:")
    print(result[["Дата операции", "Сумма операции", "Описание"]].head())
