import json
import streamlit as st

class CurrencyConverter:
    """Класс для управления конвертацией валют с использованием текущих курсов."""

    def __init__(self):
        """Инициализирует конвертер с базовой валютой и загружает сохранённые курсы, если они доступны."""
        self.base_currency = 'USD'
        self.rates = self.load_rates()

    def load_rates(self):
        """Загружает сохранённые курсы валют из JSON файла, если он существует.
        
        Возвращает:
            dict: Словарь сохранённых курсов валют.
        """
        try:
            with open('rates.json', "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_rates(self, rates):
        """Сохраняет текущие курсы валют в JSON файл.
        
        Параметры:
            rates (dict): Словарь курсов валют для сохранения.
        """
        with open('rates.json', "w") as f:
            json.dump(rates, f)

    def convert(self, amount: float, from_currency: str, to_currency: str) -> float:
        """Конвертирует сумму из одной валюты в другую.
        
        Параметры:
            amount (float): Сумма для конвертации.
            from_currency (str): Валюта, из которой выполняется конвертация.
            to_currency (str): Валюта, в которую выполняется конвертация.
        
        Возвращает:
            float: Конвертированная сумма в целевой валюте.
        """
        if not self.rates:
            st.warning("Курсы валют не загружены.")
            return 0
        if from_currency != self.base_currency:
            amount /= self.rates.get(from_currency, 1)
        return amount * self.rates.get(to_currency, 1)