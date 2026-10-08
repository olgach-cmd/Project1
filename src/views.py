from datetime import datetime
from src.utils import parse_xlsx_file, parse_json_file, greetings, get_card_summary, get_top_transactions, \
    get_exchange_rate, get_share_price


def home_page(date: str) -> dict:

    # диапазон дат для вычисления расходов
    to_dt = datetime.fromisoformat(date)
    from_dt = datetime(to_dt.year, to_dt.month, 1)

    # выгрузка DataFrame
    df = parse_xlsx_file("../data/operations.xlsx", from_dt,to_dt)

    # выгрузка пользовательских настроек
    user_settings = parse_json_file("../user_settings.json")

    # get_exchange_rate(user_settings.get("user_currencies"))

    result = {
        "greeting": greetings(),
        "cards": get_card_summary(df),
        "top_transactions": get_top_transactions(df),
        "currency_rates": get_exchange_rate(user_settings.get("user_currencies")),
        "stock_prices": get_share_price(user_settings.get("user_stocks"))
    }
    return result

if __name__ == "__main__":
    home_page("2021-12-04 01:20")