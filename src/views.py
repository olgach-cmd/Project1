from datetime import datetime
import pandas as pd

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


def parse_xlsx_file(file_path: str) -> pd.DataFrame:
    """
    Функция принимает на вход путь до xlsx-файла и возвращает pandas.DataFrame
    Если файл пустой или не найден, функция возвращает пустой DataFrame
    """
    try:
        df = pd.read_excel(file_path)
        df['Дата операции'] = pd.to_datetime(df['Дата операции'], format='%d.%m.%Y %H:%M:%S')
        df['Дата платежа'] = pd.to_datetime(df['Дата платежа'], format='%d.%m.%Y')
        return df
    except (FileNotFoundError, pd.errors.EmptyDataError):
        return pd.DataFrame()

def get_card_summary(df: pd.DataFrame, date_from: datetime, date_to: datetime) -> pd.DataFrame:
    """
    Функция возвращает сводку по картам за период: последние 4 цифры карты, общая сумма расходов и кэшбэк
    :param df:DataFrame с транзакциями
    :param date_from: начальная дата (str, формат 'YYYY-MM-DD HH:MM')
    :param date_to: конечная дата (str, формат 'YYYY-MM-DD HH:MM')
    :return: DataFrame с колонками [Номер карты, Валюта, Сумма расходов, Кэшбэк]
    """
    filter_date_df = df[df["Дата операции"].between(date_from, date_to)]
    result = filter_date_df.groupby(['Номер карты']).agg({
        'Сумма операции': 'sum', 'Кэшбэк': 'sum'
    }).abs().reset_index()
    return result