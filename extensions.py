import json
import requests
from config import keys


class ConvertionException(Exception):
    pass


class ValuteConverter:
    @staticmethod
    def convert( valute1: str, valute2: str, count: str):
        if valute1 == valute2:
            raise ConvertionException('Неудалось произвести конвертацию. Валюты должны быть разными')
        try:
            valute1_ticker = keys[valute1]
        except KeyError:
            raise ConvertionException(f'Неудалось произвести конвертацию. Валюта {valute1} не найдена')
        try:
            valute2_ticker = keys[valute2]
        except KeyError:
            raise ConvertionException(f'Неудалось произвести конвертацию. Валюта {valute2} не найдена')

        try:
            count = float(count)
        except ValueError:
            raise ConvertionException(f'Некорректно введена сумма для конвертации {count}')
        data = requests.get(
            f'https://min-api.cryptocompare.com/data/price?fsym={valute1_ticker}&tsyms={valute2_ticker}')
        total = json.loads(data.content)[keys[valute2]]
        return total*count
