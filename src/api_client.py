"""Клиент для работы с внешними API (валюты, акции)."""

import os
from typing import Any

import requests


def get_currency_rates(currencies: list[str]) -> list[dict[str, Any]]:
    """
    Получает курсы валют по отношению к рублю через open.er-api.com.

    API возвращает, сколько единиц валюты за 1 RUB.
    Нам нужно наоборот — сколько RUB за 1 единицу валюты.
    Поэтому берём 1 / rate.

    Args:
        currencies: список кодов валют (например, ["USD", "EUR"])

    Returns:
        Список словарей [{"currency": "USD", "rate": 91.74}, ...]
    """
    if not currencies:
        return []

    url = "https://open.er-api.com/v6/latest/RUB"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get("result") != "success":
            return []

        rates = data.get("rates", {})

        result = []
        for currency in currencies:
            rate = rates.get(currency)
            if rate and rate > 0:
                rub_rate = round(1 / float(rate), 2)
                result.append(
                    {
                        "currency": currency,
                        "rate": rub_rate,
                    }
                )
        return result

    except (requests.RequestException, ValueError, KeyError):
        return []


def get_stock_prices(stocks: list[str]) -> list[dict[str, Any]]:
    """
    Получает цены акций через Alpha Vantage.
    При ошибке API — падает обратно на заглушку.
    """
    MOCK_PRICES = {
        "AAPL": 150.12,
        "AMZN": 3173.18,
        "GOOGL": 2742.39,
        "MSFT": 296.71,
        "TSLA": 1007.08,
    }

    api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
    result = []

    for symbol in stocks:
        price: float | None = None

        if api_key:
            try:
                response = requests.get(
                    "https://www.alphavantage.co/query",
                    params={
                        "function": "GLOBAL_QUOTE",
                        "symbol": symbol,
                        "apikey": api_key,
                    },
                    timeout=10,
                )
                response.raise_for_status()
                payload = response.json()
                price = float(payload["Global Quote"]["05. price"])
            except (requests.RequestException, KeyError, ValueError, TypeError):
                price = None

        # Fallback на заглушку
        if price is None:
            price = MOCK_PRICES.get(symbol)

        if price is not None:
            result.append({"stock": symbol, "price": price})

    return result
