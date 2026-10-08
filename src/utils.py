from datetime import datetime
import pandas as pd
import os

import json

import requests
from dotenv import load_dotenv

load_dotenv()


def greetings() -> str:
    """
    Функция возвращает приветствие в зависимости от текущего времени
    06:00–11:59 — «Доброе утро»,
    12:00–17:59 — «Добрый день»,
    18:00–22:59 — «Добрый вечер»,
    23:00–05:59 — «Доброй ночи»
    """
    current_time = datetime.now().hour
    if 6 <= current_time < 12:
        return "Доброе утро"
    elif 12 <= current_time < 18:
        return "Добрый день"
    elif 18 <= current_time < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def parse_xlsx_file(file_path: str, date_from: datetime, date_to: datetime) -> pd.DataFrame:
    """
    Функция принимает на вход путь до xlsx-файла и возвращает pandas.DataFrame и диапазон дат
    Если файл пустой или не найден, функция возвращает пустой DataFrame
    :param file_path: путь к файлу
    :param date_from: начальная дата (str, формат 'YYYY-MM-DD HH:MM')
    :param date_to: конечная дата (str, формат 'YYYY-MM-DD HH:MM')
    :return: DataFrame
    """
    try:
        df = pd.read_excel(file_path)
        df['Дата операции'] = pd.to_datetime(df['Дата операции'], format='%d.%m.%Y %H:%M:%S')
        df['Дата платежа'] = pd.to_datetime(df['Дата платежа'], format='%d.%m.%Y')
        filter_date_df = df[df["Дата операции"].between(date_from, date_to)]
        return filter_date_df
    except (FileNotFoundError, pd.errors.EmptyDataError):
        return pd.DataFrame()


def get_card_summary(df: pd.DataFrame) -> list[dict]:
    """
    Функция возвращает общую сумму расходов и кэшбэк по каждой карте за период.
    :param df:DataFrame с транзакциями

    :return: список словарей с ключами:
        - last_digits: последние 4 цифры карты
        - total_spent: общая сумма расходов
        - cashback: кэшбэк
    """

    summary = df[df['Сумма операции'] < 0].groupby(['Номер карты']).agg({
        'Сумма операции': 'sum', 'Кэшбэк': 'sum'
    }).abs().reset_index().rename(columns={
        'Номер карты': 'last_digits',
        'Сумма операции': 'total_spent',
        'Кэшбэк': 'cashback'
    })
    summary_dic = summary.to_dict(orient="records")
    return summary_dic

def get_top_transactions(df: pd.DataFrame) -> list[dict]:
    """
    Функция выводит Топ-5 транзакций по сумме платежа.
    :param df:
    :return:
    """
    df_subset = df[['Дата операции', 'Сумма операции', 'Категория', 'Описание']].sort_values(by='Сумма операции').head()
    df_subset['Дата операции'] = df_subset['Дата операции'].dt.strftime('%d.%m.%Y')
    df_subset = df_subset.rename(columns={
        'Дата операции':'date',
        'Сумма операции': 'amount',
        'Категория':'category',
        'Описание':'description'
    })
    df_subset_dic = df_subset.to_dict(orient="records")
    return df_subset_dic


def parse_json_file(file_path: str) -> dict:
    """
    Функция принимает на вход путь до JSON-файла и возвращает список словарей с пользовательскими настройками
    :param file_path:
    :return:
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data
    except (json.decoder.JSONDecodeError, FileNotFoundError) as ex:
        return {}




def get_exchange_rate(user_currencies: list) -> list[dict]:
    """
    Функция выводи курс заданных валют к рублю, если валюта не задана или задана некорректно возвращается пустой список
    """
    try:
        user_currencies_str = ",".join(user_currencies)
        url = "https://api.apilayer.com/exchangerates_data/latest"
        params = {"symbols": user_currencies_str, "base": "RUB"}
        api_key = os.getenv("API_KEY_CURRENCY")
        headers = {"apikey": api_key}

        result_api = requests.get(url, headers=headers, params=params).json()
        # print("Статус код:", result_api.status_code)
        # print("Тело ответа:", result_api.text[:500])
        rates = result_api.get("rates")
        return [{
                "currency" : currency,
                "rate" : round(1/rates[currency],2)
            } for currency in user_currencies]
    except (TypeError, KeyError, requests.exceptions.JSONDecodeError, requests.exceptions.ConnectionError):
        return []


def get_share_price (user_stocks: list) -> list[dict]:
    """
    Функция выводит стоимость заданных акций, если акция не задана или задана некорректно возвращается пустой список
    """
    try:
        if user_stocks:
            url = "https://api.api-ninjas.com/v1/stockprice"
            api_key = os.getenv("API_KEY_STOCK")
            headers = {"X-Api-Key": api_key}
            result = []
            for stock in user_stocks:
                params = {"ticker": stock}
                share_price_api = requests.get(url, headers=headers, params=params).json()
                result.append({
                    "stock": share_price_api["ticker"],
                    "price": share_price_api["price"]
                })
            return result
        else:
            return []
    except (TypeError, KeyError, requests.exceptions.JSONDecodeError, requests.exceptions.ConnectionError):
        return[]
