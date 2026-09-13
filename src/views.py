"""Генерация JSON-ответов для веб-страниц."""

import json
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd

from src.api_client import get_currency_rates, get_stock_prices


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

    Используем 'Сумма платежа', т.к. это сумма в валюте счёта (рубли),
    а не в оригинальной валюте транзакции.

    Args:
        data: DataFrame с транзакциями

    Returns:
        Список словарей с информацией о картах
    """
    expenses = data[(data["Статус"] == "OK") & (data["Сумма платежа"] < 0)].copy()

    cards = []
    for card_number, group in expenses.groupby("Номер карты"):
        digits = str(card_number).replace("*", "").strip()[-4:]
        total_spent = round(float(abs(group["Сумма платежа"].sum())), 2)
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
    Возвращает топ-N транзакций по модулю суммы платежа.

    Args:
        data: DataFrame с транзакциями
        top_n: количество транзакций (по умолчанию 5)

    Returns:
        Список словарей с информацией о транзакциях
    """
    filtered = data[data["Статус"] == "OK"].copy()
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
        JSON-ответ с приветствием, картами, топ-транзакциями,
        курсами валют и ценами акций
    """
    dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")

    # Данные с начала месяца по указанную дату
    start_of_month = dt.replace(day=1, hour=0, minute=0, second=0)
    filtered = data[
        (data["Дата операции"] >= start_of_month) & (data["Дата операции"] <= dt) & (data["Статус"] == "OK")
    ]

    # Настройки пользователя
    settings_path = Path(__file__).parent.parent / "user_settings.json"
    with open(settings_path, "r", encoding="utf-8-sig") as f:
        settings = json.load(f)

    currencies = settings.get("user_currencies", [])
    stocks = settings.get("user_stocks", [])

    return {
        "greeting": get_greeting(dt),
        "cards": get_cards_info(filtered),
        "top_transactions": get_top_transactions(filtered),
        "currency_rates": get_currency_rates(currencies),
        "stock_prices": get_stock_prices(stocks),
    }
