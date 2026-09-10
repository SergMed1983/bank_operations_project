"""Сервисы для анализа банковских операций."""
import pandas as pd

# Категории, по которым кешбэк не начисляется
EXCLUDED_CATEGORIES = ["Переводы", "Пополнения"]


def cashback_categories(
    data: pd.DataFrame, year: int, month: int
) -> dict[str, float]:
    """
    Анализирует, сколько кешбэка можно заработать по каждой категории
    за указанный год и месяц.

    Args:
        data: DataFrame с транзакциями
        year: год для анализа
        month: месяц для анализа (1-12)

    Returns:
        dict: {категория: сумма кешбэка}
    """
    # 1. Фильтруем по статусу OK и по дате (год + месяц)
    filtered = data[
        (data["Статус"] == "OK")
        & (data["Дата операции"].dt.year == year)
        & (data["Дата операции"].dt.month == month)
    ]

    # 2. Оставляем только расходы, исключая переводы и пополнения
    expenses = filtered[
        (filtered["Сумма операции"] < 0)
        & (~filtered["Категория"].isin(EXCLUDED_CATEGORIES))
    ].copy()

    # 3. Считаем кешбэк: 1% от суммы трат
    expenses["cashback"] = expenses["Сумма операции"].abs() * 0.01

    # 4. Группируем по категории и суммируем
    grouped = expenses.groupby("Категория")["cashback"].sum()

    # 5. Округляем до 2 знаков и возвращаем dict
    return {cat: round(amount, 2) for cat, amount in grouped.items()}
