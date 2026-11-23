import pytest

from src.services import investment_bank


@pytest.fixture
def transactions():
    return [
        {"date": "2025-09-15", "amount": 35.00},
        {"date": "2025-10-26", "amount": 1411.40},
        {"date": "2025-11-01", "amount": 201.00},
        {"date": "2025-11-16", "amount": 421.15},
        {"date": "2025-11-25", "amount": 232.96},
        {"date": "2025-12-05", "amount": 34.00},
        {"date": "2025-12-20", "amount": 309.00},
        {"date": "2026-01-15", "amount": 369.00},
        {"amount": 232.96},
        {"date": "2025-11-08"},
    ]


@pytest.mark.parametrize(
    "month, limit, expected",
    [
        ("2025-11", 50, 94.89),
        ("2025-11", 100, 244.89),
        ("2025-1", 50, 0),
        ("2025-11", 0, 0),
        ("2025-11", -6, 0),
        ("2025-11", "50", 0),
    ],
)
def test_investment_bank(transactions, month, limit, expected):
    assert investment_bank(month, transactions, limit) == expected


def test_investment_bank_no_transactions(transactions):
    assert investment_bank("2025-11", [], 50) == 0
    assert investment_bank("2025-11", {}, 50) == 0
    assert investment_bank("2025-11", "jhlddfh", 50) == 0
