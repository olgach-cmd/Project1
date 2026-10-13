import tempfile
from unittest.mock import patch
from datetime import datetime
import pandas as pd
import os
import pytest

from src.utils import greetings, parse_xlsx_file, get_card_summary, get_top_transactions, parse_json_file


@pytest.fixture
def valid_xlsx_file():
    """Создаёт временный xlsx файл с данными"""
    with tempfile.TemporaryFile(suffix='.xlsx', delete=False) as tmp:
        df = pd.DataFrame({
            'col1': [1, 2, 3],
            'col2': ['a', 'b', 'c']
        })
        df.to_excel(tmp.name, index=False)
        yield tmp.name
        os.unlink(tmp.name)


# тест greetings
@pytest.mark.parametrize("hour, expected",[
    (5, "Доброй ночи"),
    (6, "Доброе утро"),
    (10, "Доброе утро"),
    (12, "Добрый день"),
    (15, "Добрый день"),
    (18, "Добрый вечер"),
    (22, "Добрый вечер"),
    (23, "Доброй ночи"),
]
)
@patch("src.utils.datetime")
def test_greetings(mock_datetime,hour, expected):
    mock_datetime.now.return_value.hour = hour
    assert greetings() == expected


# тесты parse_xlsx_file
@pytest.mark.parametrize(
    "date_from, date_to, expected",
    [
        (datetime.fromisoformat("2021-11-01"), datetime.fromisoformat("2021-11-02 09:32:23"),
                # datetime(2021, 11, 1), datetime(2021, 11, 2, 9, 33),
         pd.DataFrame({
            'Дата операции':[datetime.fromisoformat('2021-11-02 09:32:23'),
                             datetime.fromisoformat('2021-11-01 15:32:24'),
                             datetime.fromisoformat('2021-11-01 11:01:19')],
            'Сумма операции':[-5510.8, -228.00, -110.0],
            'Категория':['Каршеринг', 'Супермаркеты', 'Фастфуд']
         })),
        (datetime.fromisoformat("2021-10-01"), datetime.fromisoformat("2021-10-01 15:31:14"),
         pd.DataFrame({
            'Дата операции': [datetime.fromisoformat('2021-10-01 15:21:14'),
                             datetime.fromisoformat('2021-10-01 15:09:03'),
                             datetime.fromisoformat('2021-10-01 14:57:46')],
            'Сумма операции': [-96.78, -15.24, -492.00],
            'Категория': ['Супермаркеты', 'Каршеринг', 'Дом и ремонт']
         })),
    ]
)
def test_parse_xlsx(date_from, date_to, expected):
    """Тестирование корректной работы"""
    pd.testing.assert_frame_equal(parse_xlsx_file("data/operations.xlsx", date_from, date_to)[['Дата операции', 'Сумма операции', 'Категория']].reset_index(drop=True), expected, check_like=True
)

@pytest.mark.parametrize(
    "file_path, date_from, date_to", [
    ("non_file.xlsx", datetime.fromisoformat("2021-10-01"), datetime.fromisoformat("2021-10-01 15:31:14")),
    ("../user_settings.json", datetime.fromisoformat("2021-10-01"), datetime.fromisoformat("2021-10-01 15:31:14")),
    ("data/empty_file.txt", datetime.fromisoformat("2021-10-01"), datetime.fromisoformat("2021-10-01 15:31:14")),
    ("data/operations.xlsx", 233, datetime.fromisoformat("2021-10-01 15:31:14")),
    ("data/operations.xlsx", datetime.fromisoformat("2021-10-01"), "euroiw;r "),
    (45654, datetime.fromisoformat("2021-10-01"), datetime.fromisoformat("2021-10-01 15:31:14")),
])
def test_parse_xlsx_err(file_path, date_from, date_to):
    """Некорректные файлу и неверные типы данных"""
    result_df = parse_xlsx_file(file_path, date_from, date_to)
    assert result_df.empty

# тесты get_card_summary
@pytest.mark.parametrize(
    "df, expected", [
        (parse_xlsx_file("data/operations.xlsx",
                         datetime.fromisoformat("2021-10-06 16:31"),
                         datetime.fromisoformat("2021-10-06 20:31")),
         [{"last_digits": "*4556", "total_spent": 3000.00, "cashback": 0},
          {"last_digits": "*7197", "total_spent": 254.82, "cashback": 0}]),
        (parse_xlsx_file("data/operations.xlsx",
                         datetime.fromisoformat("2021-09-25 12:36"),
                         datetime.fromisoformat("2021-09-25 20:00")),
         [{"last_digits": "*4556", "total_spent": 8798, "cashback": 439},
          {"last_digits": "*7197", "total_spent": 144.45, "cashback": 0}
          ]),
    ]
)
def test_get_card_summary(df, expected):
    assert get_card_summary(df) == expected


# тесты get_top_transactions
@pytest.mark.parametrize(
    "df, expected", [
        (parse_xlsx_file("data/operations.xlsx",
                         datetime.fromisoformat("2021-12-01 01:20"),
                         datetime.fromisoformat("2021-12-04 01:20")),
         [{"date": "02.12.2021", "amount": -5510.8, "category": "Каршеринг", "description": "Ситидрайв"},
         {"date": "03.12.2021", "amount": -3499.0, "category": "Электроника и техника", "description": "DNS"},
         {"date": "02.12.2021", "amount": -496.51, "category": "Супермаркеты", "description": "Магнит"},
         {"date": "03.12.2021", "amount": -496.3, "category": "Аптеки", "description": "Аптека Вита"},
         {"date": "03.12.2021", "amount": -204.8, "category": "Супермаркеты", "description": "Колхоз"}]
         ),
    ]
)
def test_get_top_transactions(df, expected):
    assert get_top_transactions(df) == expected


# тесты parse_json_file
@pytest.mark.parametrize(
    "file_path, expected", [
    ("non_file.json", {}),
    ("data/empty_file.txt", {}),
    ("data/operations.xlsx", {}),
    (45654, {}),
    ("../user_settings.json", {
        "user_currencies": ["USD", "EUR"],
        "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]}),
])
def test_parse_json_file(file_path, expected):
    assert parse_json_file(file_path) == expected


# тесты get_exchange_rate
