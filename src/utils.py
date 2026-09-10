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
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], format="%d.%m.%Y %H:%M:%S", errors="coerce")
    return df


if __name__ == "__main__":
    import json

    from views import main_page

    df = load_transactions("data/operations.xlsx")

    result = main_page("2021-12-31 16:44:00", df)

    print("\n=== Ответ главной страницы ===")
    print(f"\nПриветствие: {result['greeting']}")
    print(f"\nКарты ({len(result['cards'])}):")
    for card in result["cards"]:
        print(f"  {card}")
    print("\nТоп-5 транзакций:")
    for tx in result["top_transactions"]:
        print(f"  {tx['date']} | {tx['amount']} | {tx['category']} | {tx['description']}")
    print(f"\nCurrency rates: {result['currency_rates']}")
    print(f"Stock prices: {result['stock_prices']}")

    print("\n=== JSON ===")
    print(json.dumps(result, ensure_ascii=False, indent=2))
