import requests
from config import MONOBANK_API


class Converter:
    API_URL = MONOBANK_API
    CURRENCY_CODES = {
        "UAH": 980,
        "USD": 840,
        "EUR": 978,
    }

    def __init__(self):
        self.rates = self.get_rates()

    def get_rates(self):
        response = requests.get(self.API_URL, timeout=10)
        response.raise_for_status()
        return response.json()

    def get_rate(self, code_a, code_b):
        for rate in self.rates:
            if (
                rate.get("currencyCodeA") == code_a
                and rate.get("currencyCodeB") == code_b
            ):
                return rate
        return None

    def convert(self, amount: float, currency_from: str, currency_to: str):
        if currency_from == currency_to:
            return amount

        if currency_from not in self.CURRENCY_CODES:
            raise ValueError(f"Невідома валюта: {currency_from}")
        if currency_to not in self.CURRENCY_CODES:
            raise ValueError(f"Невідома валюта: {currency_to}")

        # 1. UAH -> foreign
        if currency_from == "UAH":
            to_code = self.CURRENCY_CODES[currency_to]
            rate = self.get_rate(to_code, 980)  # foreign -> UAH
            if not rate or "rateSell" not in rate:
                raise Exception("Не знайдено курс продажу")
            return amount / rate["rateSell"]

        # 2. foreign -> UAH
        if currency_to == "UAH":
            from_code = self.CURRENCY_CODES[currency_from]
            rate = self.get_rate(from_code, 980)  # foreign -> UAH
            if not rate or "rateBuy" not in rate:
                raise Exception("Не знайдено курс купівлі")
            return amount * rate["rateBuy"]

        # 3. foreign -> foreign через UAH
        to_uah = self.convert(amount, currency_from, "UAH")
        return self.convert(to_uah, "UAH", currency_to)
