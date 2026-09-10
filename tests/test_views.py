"""Тесты для views.py."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from datetime import datetime  # noqa: E402

import pandas as pd  # noqa: E402

from views import get_cards_info, get_greeting, get_top_transactions  # noqa: E402

# ---------- get_greeting ----------


def test_greeting_morning():
    """06:00–11:59 → Доброе утро."""
    assert get_greeting(datetime(2021, 12, 31, 8, 0)) == "Доброе утро"
    assert get_greeting(datetime(2021, 12, 31, 11, 59)) == "Доброе утро"


def test_greeting_day():
    """12:00–17:59 → Добрый день."""
    assert get_greeting(datetime(2021, 12, 31, 12, 0)) == "Добрый день"
    assert get_greeting(datetime(2021, 12, 31, 17, 59)) == "Добрый день"


def test_greeting_evening():
    """18:00–22:59 → Добрый вечер."""
    assert get_greeting(datetime(2021, 12, 31, 18, 0)) == "Добрый вечер"
    assert get_greeting(datetime(2021, 12, 31, 22, 59)) == "Добрый вечер"


def test_greeting_night():
    """23:00–05:59 → Доброй ночи."""
    assert get_greeting(datetime(2021, 12, 31, 23, 0)) == "Доброй ночи"
    assert get_greeting(datetime(2021, 12, 31, 3, 0)) == "Доброй ночи"
    assert get_greeting(datetime(2021, 12, 31, 5, 59)) == "Доброй ночи"


# ---------- get_cards_info ----------


def _make_cards_data() -> pd.DataFrame:
    """Тестовые данные для карт."""
    return pd.DataFrame(
        {
            "Статус": ["OK", "OK", "OK", "FAILED"],
            "Сумма операции": [-1000.0, -500.0, -300.0, -200.0],
            "Номер карты": ["*1234", "*1234", "*5678", "*1234"],
        }
    )


def test_cards_info_returns_list():
    """Возвращает список."""
    data = _make_cards_data()
    result = get_cards_info(data)
    assert isinstance(result, list)


def test_cards_info_groups_by_card():
    """Группирует по карте."""
    data = _make_cards_data()
    result = get_cards_info(data)
    assert len(result) == 2


def test_cards_info_cashback():
    """Кешбэк = 1% от суммы."""
    data = _make_cards_data()
    result = get_cards_info(data)
    card_1234 = next(c for c in result if c["last_digits"] == "1234")
    assert card_1234["total_spent"] == 1500.0
    assert card_1234["cashback"] == 15.0


# ---------- get_top_transactions ----------


def _make_top_data() -> pd.DataFrame:
    """Тестовые данные для топ-транзакций."""
    return pd.DataFrame(
        {
            "Дата операции": pd.to_datetime(
                [
                    "2021-12-01 10:00:00",
                    "2021-12-02 10:00:00",
                    "2021-12-03 10:00:00",
                    "2021-12-04 10:00:00",
                    "2021-12-05 10:00:00",
                    "2021-12-06 10:00:00",
                ]
            ),
            "Статус": ["OK"] * 6,
            "Сумма платежа": [-100.0, -500.0, -3000.0, -200.0, -50.0, -1000.0],
            "Категория": [
                "Супермаркеты",
                "Супермаркеты",
                "Электроника",
                "Фастфуд",
                "Такси",
                "Переводы",
            ],
            "Описание": ["A", "B", "C", "D", "E", "F"],
        }
    )


def test_top_transactions_returns_5():
    """Возвращает ровно 5 транзакций по умолчанию."""
    data = _make_top_data()
    result = get_top_transactions(data)
    assert len(result) == 5


def test_top_transactions_sorted_by_amount():
    """Отсортированы по убыванию суммы."""
    data = _make_top_data()
    result = get_top_transactions(data)
    amounts = [abs(tx["amount"]) for tx in result]
    assert amounts == sorted(amounts, reverse=True)


def test_top_transactions_excludes_transfers():
    """Переводы не попадают в топ."""
    data = _make_top_data()
    result = get_top_transactions(data)
    categories = [tx["category"] for tx in result]
    assert "Переводы" not in categories
