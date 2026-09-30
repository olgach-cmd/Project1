from datetime import datetime
import pandas as pd
from views import greetings, parse_xlsx_file, get_card_summary


def main(date: str):
    print(greetings())
    df = parse_xlsx_file("../data/operations.xlsx")

    # print(df)
    # print(df['Дата операции'].dtype)
    dt = datetime.fromisoformat(date)
    from_dt = datetime(dt.year, dt.month, 1)
    filter_date_df = df[df["Дата операции"].between(from_dt,dt)]

    print(get_card_summary(df,from_dt,dt))


if __name__ == "__main__":
    main("2021-12-02 01:20")