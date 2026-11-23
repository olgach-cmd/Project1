import pytest
import pandas as pd

from src.reports import spending_by_category


@pytest.fixture
def sample_transactions():
    data = pd.DataFrame({
        "Дата операции": pd.to_datetime(["2023-10-01", "2023-11-15", "2023-12-01", "2024-01-10", "2024-02-01"]),
        "Категория": ["Еда", "Транспорт", "Еда", "Развлечения", "Еда"],
        "Сумма": [100, 200, 150, 300, 500]
    })
    return pd.DataFrame(data)


@pytest.mark.parametrize( "category, date_to, expected", [
    ("Транспорт", "2024-01-15 15:00", pd.DataFrame({
                                      "Дата операции": pd.to_datetime(["2023-11-15"]),
                                      "Категория": ["Транспорт"],
                                      "Сумма": [200]
                                  })),
    ("Еда", "2024-02-15 15:00", pd.DataFrame({
        "Дата операции": pd.to_datetime([ "2023-12-01","2024-02-01"]),
        "Категория": ["Еда", "Еда"],
        "Сумма": [150, 500]
    })),

] )

def test_spending_by_category(sample_transactions, category, date_to, expected):
    pd.testing.assert_frame_equal(spending_by_category(sample_transactions, category, date_to).reset_index(drop=True),
                                  expected, check_like=True)


def test_spending_by_category_default_date(sample_transactions):
    """тест с текущей датой (данные устарели)"""
    assert spending_by_category(sample_transactions, "Еда").empty


@pytest.mark.parametrize( "category, date_to", [
    ("Перевод", "2024-01-15 15:00"),
    (456, "2024-02-15 15:00"),
    ("Еда", "2024-02"),
    ("Еда", "hdskjfhk"),
] )
def test_spending_by_category_err(sample_transactions, category, date_to):
    assert spending_by_category(sample_transactions, category, date_to).empty

def test_spending_by_category_err_pd():
    assert spending_by_category({}, "Перевод", "2024-01-15 15:00").empty