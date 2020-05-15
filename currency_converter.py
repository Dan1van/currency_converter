from forex_python.converter import CurrencyRates, RatesNotAvailableError
from datetime import datetime

c = CurrencyRates()


def currency_converter(from_currency, to_currency, value, date_obj=datetime.now()):
    return str(c.convert(from_currency, to_currency, value, date_obj)) + ' ' + to_currency


def set_history(value, from_currency, to_currency, result):
    exchange_rate = c.get_rate(to_currency, from_currency)
    history_db = open('history-db', 'a')
    history_db.write(
        'Конвертация {0} {1} в {2} по курсу {3:.3f}: {4}'.format(value, from_currency, to_currency, exchange_rate,
                                                                 result) + '\n')
    history_db.close()


def get_history():
    history_db = open('history-db', 'r')
    print('История конвертаций:\n')
    [print(readline) for readline in history_db.readlines()]
    history_db.close()


while True:

    entered_value = input('1. Конвертировать валюту\n2. Посмотреть историю конвертаций\n3. Выйти из программы\n')

    try:
        entered_value = int(entered_value)
    except ValueError:
        print('Неверное значение! Попробуйте снова!')
        continue
    if entered_value == 1:
        while True:
            from_currency_name = input('Какую валюту Вы хотели бы конвертировать?\n')

            try:
                c.get_rates(from_currency_name)
            except RatesNotAvailableError:
                print('Неверная валюта! Попробуйте снова...')
                continue
            break

        while True:
            to_currency_name = input('В какую валюту Вы хотели бы конвертировать {0}?\n'.format(from_currency_name))

            if to_currency_name not in c.get_rates(from_currency_name) or to_currency_name == from_currency_name:
                print('Неверная валюта! Попробуйте снова...')
                continue
            break

        while True:
            money_value = input('Какую сумму Вы хотели бы конвертировать?\n')
            try:
                money_value = int(money_value)
            except (TypeError, ValueError):
                print('Неверная сумма! Попробуйте снова!')
                continue

            if money_value < 1:
                print('Неверная сумма! Попробуйте снова!')
                continue
            break

        while True:
            input_date_answer = input(
                'Хотели бы Вы конвертировать валюту в ретроспективе?\nВведите "Да" или "Нет"\n')
            if input_date_answer == 'Да':
                while True:
                    date = input('Введите дату в формате ДД.ММ.ГГГГ (до 2020 года)\n')
                    try:
                        date = datetime.strptime(date, '%d.%m.%Y')
                    except ValueError:
                        print('Неверная дата! Попробуйте снова!')
                        continue
                    if date >= datetime.now():
                        print('Неверная дата! Попробуйте снова!')
                        continue
                    break
                result = currency_converter(from_currency_name, to_currency_name, money_value, date)
                print(result + '\n\n')
                set_history(money_value, from_currency_name, to_currency_name, result)
            elif input_date_answer == 'Нет':
                result = currency_converter(from_currency_name, to_currency_name, money_value)
                print(result + '\n\n')
                set_history(money_value, from_currency_name, to_currency_name, result)
            else:
                print('Неверный ответ! Попробуйте снова...')
                continue
            break
    elif entered_value == 2:
        get_history()
    elif entered_value == 3:
        break
