from unittest.mock import patch
from datetime import datetime
import pytest

from src.views import greetings

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
@patch("src.views.datetime")
def test_greetings(mock_datetime,hour, expected):
    mock_datetime.now.return_value.hour = hour
    assert greetings() == expected


# тесты parse_xlsx_file
@patch("src.views.pd.read_excel")
def test_parse_csv_file_ok(mock_read_csv, result_ok, fake_dataframe):
    fake_df = fake_dataframe
    mock_read_csv.return_value = fake_df
    assert parse_xlsx_file("fake_file.xlsx") == result_ok
