"""Отчёты по банковским операциям."""
import json
from datetime import datetime
from functools import wraps
from pathlib import Path
from typing import Callable, Optional

import pandas as pd


def save_report(filename: Optional[str] = None):
    """
    Декоратор для сохранения результата отчёта в файл.

    Args:
        filename: имя файла (если None — используется имя по умолчанию)

    Returns:
        Декоратор
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            # Определяем имя файла
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filepath = Path(f"{func.__name__}_{timestamp}.json")
            else:
                filepath = Path(filename)

            # Преобразуем DataFrame в JSON-совместимый вид
            if isinstance(result, pd.DataFrame):
                data = result.to_dict(orient="records")
                for record in data:
                    for key, value in record.items():
                        if isinstance(value, pd.Timestamp):
                            record[key] = value.strftime("%Y-%m-%d %H:%M:%S")
            else:
                data = result

            # Сохраняем в файл
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2, default=str)

            print(f"Отчёт сохранён: {filepath}")
            return result

        return wrapper

    return decorator


@save_report()
def spending_by_category(
    transactions: pd.DataFrame,
    category: str,
    date: Optional[str] = None,
) -> pd.DataFrame:
    """
    Возвращает траты по заданной категории за последние 3 месяца.

    Args:
        transactions: DataFrame с транзакциями
        category: название категории
        date: дата в формате 'YYYY-MM-DD' (по умолчанию — сегодня)

    Returns:
        DataFrame с тратами по категории за 3 месяца
    """
    # 1. Определяем дату отсчёта (конец дня)
    if date is None:
        end_date = datetime.now()
    else:
        end_date = datetime.strptime(date, "%Y-%m-%d").replace(
            hour=23, minute=59, second=59
        )

    # 2. Начало периода: 3 месяца назад
    start_date = end_date - pd.DateOffset(months=3)

    # 3. Фильтруем по категории, статусу и дате
    filtered = transactions[
        (transactions["Категория"] == category)
        & (transactions["Статус"] == "OK")
        & (transactions["Дата операции"] >= start_date)
        & (transactions["Дата операции"] <= end_date)
        & (transactions["Сумма операции"] < 0)
    ]

    return filtered
