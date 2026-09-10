"""Тесты для api_client.py."""

import os
import sys
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from api_client import get_currency_rates, get_stock_prices  # noqa: E402


@patch("api_client.requests.get")
def test_get_currency_rates_success(mock_get):
    """Успешный запрос курсов валют."""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "result": "success",
        "rates": {"USD": 0.01, "EUR": 0.009},
    }
    mock_response.raise_for_status = MagicMock()
    mock_get.return_value = mock_response

    result = get_currency_rates(["USD", "EUR"])
    assert len(result) == 2
    assert result[0]["currency"] == "USD"
    assert result[0]["rate"] == 100.0


@patch("api_client.requests.get")
def test_get_currency_rates_error(mock_get):
    """Ошибка сети -> пустой список."""
    import requests

    mock_get.side_effect = requests.RequestException("Network error")
    result = get_currency_rates(["USD"])
    assert result == []


def test_get_currency_rates_empty():
    """Пустой список валют."""
    assert get_currency_rates([]) == []


def test_get_stock_prices():
    """Заглушка возвращает фиксированные цены."""
    result = get_stock_prices(["AAPL", "AMZN"])
    assert len(result) == 2
    assert result[0]["stock"] == "AAPL"


def test_get_stock_prices_unknown():
    """Неизвестный тикер не попадает."""
    result = get_stock_prices(["UNKNOWN"])
    assert result == []
