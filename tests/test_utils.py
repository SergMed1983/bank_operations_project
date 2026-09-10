"""Тесты для utils.py."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import pandas as pd  # noqa: E402

from utils import load_transactions  # noqa: E402


def test_load_transactions_returns_dataframe(tmp_path):
    """Проверяет, что функция возвращает DataFrame."""
    test_file = tmp_path / "test.xlsx"
    df = pd.DataFrame({
        "Дата операции": ["01.01.2024"],
        "Сумма операции": [100.0],
        "Категория": ["Супермаркеты"],
    })
    df.to_excel(test_file, index=False)

    result = load_transactions(str(test_file))
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 1