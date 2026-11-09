from datetime import datetime


def investment_bank(month: str, transactions: list[dict[str, any]], limit: int) -> float:
    """
    Функция расчитывает и возвращает сумму, которую удалось бы отложить в «Инвесткопилку».
    :param month: месяц, для которого рассчитывается отложенная сумма (строка в формате 'YYYY-MM').
    :param transactions: список словарей, содержащий информацию о транзакциях, в которых содержатся следующие поля:
        "date" - Дата операции (дата, когда произошла транзакция (строка в формате 'YYYY-MM-DD'))
        "amount" - Сумма операции (сумма транзакции в оригинальной валюте (число))
    :param limit: предел, до которого нужно округлять суммы операций (целое число)
    :return: сумма, которую удалось бы отложить в «Инвесткопилку»
    """
    try:
        if len(month) == 7 and month[4] == '-' and limit > 0:
            # дополнительно проверяю, что month переводиться в datetime (если нет, уйдет в except)
            datetime.strptime(month, "%Y-%m")

            summ = 0
            for transaction in transactions:
                if transaction.get("date") and transaction.get("amount") and transaction["date"].startswith(month):
                    summ += limit - round(transaction.get("amount") % limit,2)

            return round(summ,2)
        else:
            return 0

    except ValueError, TypeError, AttributeError:
        return 0




