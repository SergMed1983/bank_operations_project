"""Тесты для reports.py."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import pandas as pd  # noqa: E402

from reports import spending_by_category  # noqa: E402


def _make_test_data() -> pd.DataFrame:
    """Создаёт тестовый DataFrame с транзакциями."""
    return pd.DataFrame(
        {
            "Дата операции": pd.to_datetime(
                [
                    "2021-12-15 10:00:00",  # попадает (декабрь)
                    "2021-12-01 10:00:00",  # попадает (декабрь)
                    "2021-11-15 10:00:00",  # попадает (в пределах 3 мес)
                    "2021-10-15 10:00:00",  # попадает (в пределах 3 мес)
                    "2021-09-15 10:00:00",  # НЕ попадает (больше 3 мес)
                    "2021-12-20 10:00:00",  # другая категория
                    "2021-12-20 10:00:00",  # FAILED
                ]
            ),
            "Статус": ["OK", "OK", "OK", "OK", "OK", "OK", "FAILED"],
            "Сумма операции": [-1000.0, -500.0, -300.0, -200.0, -100.0, -400.0, -100.0],
            "Категория": [
                "Супермаркеты",
                "Супермаркеты",
                "Супермаркеты",
                "Супермаркеты",
                "Супермаркеты",
                "Фастфуд",
                "Супермаркеты",
            ],
        }
    )


def test_returns_dataframe():
    """Проверяет, что функция возвращает DataFrame."""
    data = _make_test_data()
    result = spending_by_category(data, category="Супермаркеты", date="2021-12-31")
    assert isinstance(result, pd.DataFrame)


def test_only_selected_category():
    """Проверяет, что возвращаются только транзакции выбранной категории."""
    data = _make_test_data()
    result = spending_by_category(data, category="Супермаркеты", date="2021-12-31")
    assert all(result["Категория"] == "Супермаркеты")


def test_last_three_months_only():
    """Проверяет, что старые транзакции не попадают."""
    data = _make_test_data()
    result = spending_by_category(data, category="Супермаркеты", date="2021-12-31")
    # 2021-09-15 должен быть исключён (больше 3 месяцев)
    assert len(result) == 4  # 4 транзакции: дек×2, ноя, окт


def test_ignores_failed():
    """Проверяет, что FAILED-транзакции не попадают."""
    data = _make_test_data()
    result = spending_by_category(data, category="Супермаркеты", date="2021-12-31")
    assert all(result["Статус"] == "OK")


def test_only_expenses():
    """Проверяет, что возвращаются только расходы."""
    data = _make_test_data()
    result = spending_by_category(data, category="Супермаркеты", date="2021-12-31")
    assert all(result["Сумма операции"] < 0)
