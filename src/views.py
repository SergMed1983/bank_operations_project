"""Генерация JSON-ответов для веб-страниц."""
from datetime import datetime
from typing import Any, Optional

import pandas as pd


def get_greeting(dt: datetime) -> str:
    """
    Возвращает приветствие в зависимости от времени суток.

    Args:
        dt: дата и время

    Returns:
        Строка приветствия
    """
    hour = dt.hour
    if 6 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def get_cards_info(data: pd.DataFrame) -> list[dict[str, Any]]:
    """
    Возвращает информацию по каждой карте: последние 4 цифры,
    общая сумма расходов и кешбэк (1% от суммы).

    Args:
        data: DataFrame с транзакциями

    Returns:
        Список словарей с информацией о картах
    """
    # Оставляем только расходы (отрицательные суммы) и статус OK
    expenses = data[(data["Статус"] == "OK") & (data["Сумма операции"] < 0)].copy()

    # Группируем по номеру карты
    cards = []
    for card_number, group in expenses.groupby("Номер карты"):
        # Берём последние 4 цифры
        digits = str(card_number).replace("*", "").strip()[-4:]

        total_spent = round(float(abs(group["Сумма операции"].sum())), 2)
        cashback = round(total_spent * 0.01, 2)

        cards.append(
            {
                "last_digits": digits,
                "total_spent": total_spent,
                "cashback": cashback,
            }
        )

    return cards


def get_top_transactions(data: pd.DataFrame, top_n: int = 5) -> list[dict[str, Any]]:
    """
    Возвращает топ-N транзакций по сумме платежа (только расходы).

    Args:
        data: DataFrame с транзакциями
        top_n: количество транзакций (по умолчанию 5)

    Returns:
        Список словарей с информацией о транзакциях
    """
    # Исключаем переводы и пополнения, оставляем только расходы
    excluded = ["Переводы", "Пополнения"]
    filtered = data[
        (data["Статус"] == "OK")
        & (data["Сумма платежа"] < 0)
        & (~data["Категория"].isin(excluded))
    ].copy()

    # Сортируем по модулю суммы платежа (крупные расходы)
    filtered["abs_amount"] = filtered["Сумма платежа"].abs()
    top = filtered.nlargest(top_n, "abs_amount")

    result = []
    for _, row in top.iterrows():
        result.append(
            {
                "date": row["Дата операции"].strftime("%d.%m.%Y"),
                "amount": round(float(row["Сумма платежа"]), 2),
                "category": row["Категория"],
                "description": row["Описание"],
            }
        )

    return result


def main_page(date_str: str, data: pd.DataFrame) -> dict[str, Any]:
    """
    Главная функция для веб-страницы «Главная».

    Args:
        date_str: дата в формате 'YYYY-MM-DD HH:MM:SS'
        data: DataFrame с транзакциями

    Returns:
        JSON-ответ с приветствием, картами, топ-транзакциями
    """
    # 1. Парсим дату
    dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")

    # 2. Фильтруем данные с начала месяца по указанную дату
    start_of_month = dt.replace(day=1, hour=0, minute=0, second=0)
    filtered = data[
        (data["Дата операции"] >= start_of_month)
        & (data["Дата операции"] <= dt)
        & (data["Статус"] == "OK")
    ]

    # 3. Собираем ответ
    return {
        "greeting": get_greeting(dt),
        "cards": get_cards_info(filtered),
        "top_transactions": get_top_transactions(filtered),
        "currency_rates": [],  # TODO: добавим позже
        "stock_prices": [],  # TODO: добавим позже
    }
