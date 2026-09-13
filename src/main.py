"""Точка входа приложения для анализа банковских операций."""

import json

from src.reports import spending_by_category
from src.services import cashback_categories
from src.utils import load_transactions
from src.views import main_page


def run() -> None:
    """Запускает основные функции приложения."""
    # Загружаем данные один раз — в utils.py, не в бизнес-логике
    df = load_transactions("data/operations.xlsx")

    # Дата для теста — попадает в диапазон данных (декабрь 2021)
    date_str = "2021-12-31 16:44:00"

    # 1. Страница «Главная»
    print("=== Главная страница ===")
    result = main_page(date_str, df)
    print(json.dumps(result, ensure_ascii=False, indent=2))

    # 2. Сервис «Выгодные категории кешбэка»
    print("\n=== Выгодные категории кешбэка (декабрь 2021) ===")
    cashback = cashback_categories(df, year=2021, month=12)
    print(json.dumps(cashback, ensure_ascii=False, indent=2))

    # 3. Отчёт «Траты по категории»
    #    Декоратор save_report сам сохранит результат в JSON
    print("\n=== Траты по категории «Супермаркеты» ===")
    report = spending_by_category(df, category="Супермаркеты", date="2021-12-31")
    print(report)
    print(f"\nСтрок в отчёте: {len(report)}")


if __name__ == "__main__":
    run()
