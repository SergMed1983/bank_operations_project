"""Тесты для services.py."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import pandas as pd  # noqa: E402

from services import cashback_categories  # noqa: E402


def _make_test_data() -> pd.DataFrame:
    """Создаёт тестовый DataFrame с транзакциями."""
    return pd.DataFrame(
        {
            "Дата операции": pd.to_datetime(
                [
                    "2021-12-01 10:00:00",  # расход, OK, декабрь
                    "2021-12-15 12:00:00",  # расход, OK, декабрь
                    "2021-12-20 15:00:00",  # перевод, OK, декабрь
                    "2021-12-25 18:00:00",  # расход, FAILED, декабрь
                    "2021-11-10 10:00:00",  # расход, OK, ноябрь
                    "2021-12-30 20:00:00",  # пополнение (положительное), декабрь
                ]
            ),
            "Статус": ["OK", "OK", "OK", "FAILED", "OK", "OK"],
            "Сумма операции": [-1000.0, -500.0, -3000.0, -200.0, -1500.0, 5000.0],
            "Категория": [
                "Супермаркеты",
                "Супермаркеты",
                "Переводы",
                "Фастфуд",
                "Супермаркеты",
                "Пополнения",
            ],
        }
    )


def test_cashback_returns_dict():
    """Проверяет, что функция возвращает словарь."""
    data = _make_test_data()
    result = cashback_categories(data, year=2021, month=12)
    assert isinstance(result, dict)


def test_cashback_supermarkets():
    """Проверяет сумму кешбэка по категории 'Супермаркеты'."""
    data = _make_test_data()
    result = cashback_categories(data, year=2021, month=12)
    # Супермаркеты: (1000 + 500) * 0.01 = 15.0
    assert result["Супермаркеты"] == 15.0


def test_cashback_excludes_transfers():
    """Проверяет, что 'Переводы' не попадают в результат."""
    data = _make_test_data()
    result = cashback_categories(data, year=2021, month=12)
    assert "Переводы" not in result


def test_cashback_excludes_income():
    """Проверяет, что 'Пополнения' не попадают в результат."""
    data = _make_test_data()
    result = cashback_categories(data, year=2021, month=12)
    assert "Пополнения" not in result


def test_cashback_excludes_failed():
    """Проверяет, что FAILED-транзакции не учитываются."""
    data = _make_test_data()
    result = cashback_categories(data, year=2021, month=12)
    assert "Фастфуд" not in result


def test_cashback_excludes_other_months():
    """Проверяет, что транзакции за другие месяцы не учитываются."""
    data = _make_test_data()
    result_dec = cashback_categories(data, year=2021, month=12)
    result_nov = cashback_categories(data, year=2021, month=11)
    # В ноябре — только одна транзакция (Супермаркеты, -1500)
    assert result_nov == {"Супермаркеты": 15.0}
    # В декабре — две (Супермаркеты: 1000 + 500 = 15.0)
    assert result_dec["Супермаркеты"] == 15.0
