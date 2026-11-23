from datetime import datetime
from functools import wraps
from typing import Optional

import pandas as pd
from dateutil.relativedelta import relativedelta


def writing_pd_to_file(function):
    """
    Декоратор, записывает DataFrame в xlsx файл
    """

    @wraps(function)
    def inner(*args, **kwargs):
        df = function(*args, **kwargs)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
        filename = f"report_{timestamp}.xlsx"
        df.to_excel(filename, index=False)
        return df

    return inner


def spending_by_category(transactions: pd.DataFrame, category: str, date_to: Optional[str] = None) -> pd.DataFrame:
    """
    Функция возвращает траты по заданной категории за последние три месяца (от переданной даты),
    при ошибке возвращает пустой DataFrame
    :param transactions: DataFrame с транзакциями
    :param category: название категории
    :param date_to: дата (опциональна)
    :return: DataFrame
    """
    try:
        if date_to:
            date_to = datetime.fromisoformat(date_to)
        else:
            date_to = datetime.now()

        date_from = date_to - relativedelta(months=3)
        filter_date_transactions = transactions[
            (transactions["Дата операции"].between(date_from, date_to)) & (transactions["Категория"] == category)
        ]
        return filter_date_transactions

    except TypeError, KeyError, ValueError:
        return pd.DataFrame()
