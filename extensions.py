import telebot
import requests
import json
from token import money_name
from app import bot

class ConvertionException(Exception):
    pass

class CryptoConvector():
  @staticmethod
  def convert(quote: str,  base: str, amount: str):

    if quote == base:
        raise ConvertionException('Недопустимые параметры перевода')

    try:
        quote_ticker = money_name[quote]
    except KeyError:
        raise ConvertionException(f'Валюта {quote} не доступна')

    try:
        base_ticker = money_name[base]
    except KeyError:
        raise ConvertionException(f'Валюта {base} не доступна')

    try:
        amount = float(amount)
    except ValueError:
        raise ConvertionException(f'Неправильно введено колличество - {amount}')

    answer = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
    total_base = json.loads(answer.content)[money_name[base]]

    return total_base

class Price():
    def get_price(quote: str, base: str, amount: str):
        total_base = CryptoConvector.convert(quote, base, amount)
        total_summ = float(total_base) * float(amount)
        text = f'Цена {amount} {quote} - {total_summ} {base}'
        return text