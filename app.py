import streamlit as st
import plotly.express as px
import freecurrencyapi
import os
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime, timedelta
import time
import json

# Загрузка API-ключа из .env файла
load_dotenv()
API_KEY = os.getenv("API_KEY")
client = freecurrencyapi.Client(API_KEY)
CSV_FILE_PATH = 'currency_rates.csv'

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
    
class Currency_data_fether: 
    """Класс, который получает информацию, о последних изменениях курсов валют и подгрузка их."""
    def __init__(self):
        """Инициализация клиента API"""
        self.client = client
        self.converter = CurrencyConverter()

    def fetch_and_save_rates(self, date: str, csv_file: str):
        """Запрашивает и сохраняет исторические курсы валют на указанную дату.
        
        Параметры:
            date (str): Дата для запроса в формате 'YYYY-MM-DD'.
            csv_file (str): Путь к CSV файлу для сохранения данных.
        """
        try:
            result = self.client.historical(date)
            rates = result.get('data', {}).get(date, {})
            
            df = pd.DataFrame([rates])
            df['date'] = date
            df = df[['date'] + [col for col in df.columns if col != 'date']]

            if not os.path.isfile(csv_file):
                df.to_csv(csv_file, index=False)
            else:
                df.to_csv(csv_file, mode='a', header=False, index=False)
            
            print(f"Данные за {date} успешно сохранены в {csv_file}.")
        except Exception as e:
            st.error(f"Ошибка при запросе данных за {date}: {e}")

    def fetch_data_for_date_range(self, start_date, end_date):
        """Запрашивает и сохраняет исторические данные за диапазон дат, учитывая ограничения API.
        
        Параметры:
            start_date (datetime): Начальная дата диапазона.
            end_date (datetime): Конечная дата диапазона.
        """
        current_date = start_date
        request_count = 0

        while current_date <= end_date:
            date_str = current_date.strftime('%Y-%m-%d')
            self.fetch_and_save_rates(date_str, CSV_FILE_PATH)
            request_count += 1
            current_date += timedelta(days=1)

            # Ограничение запросов: пауза после каждых 10 запросов
            if request_count == 10:
                st.info("Достигнут лимит запросов API. Ожидание 60 секунд...")
                time.sleep(60)
                request_count = 0

        st.success(f"Данные за период с {start_date.strftime('%Y-%m-%d')} по {end_date.strftime('%Y-%m-%d')} успешно загружены!")

    def fetch_exchange_rates(self):
        """Запрашивает текущие курсы валют через API и сохраняет их локально."""
        try:
            data = self.client.latest(base_currency=self.converter.base_currency)
            self.converter.rates = data.get("data", {})
            self.converter.save_rates(self.converter.rates)
            st.success("Курсы валют обновлены.")
        except Exception:
            st.error("Не удалось обновить курсы. Используются последние сохранённые данные.")

class Currency_plot:
    """Класс, который будет рисовать график, исходя от курса валют."""

    def __init__ (self, csv_file_path):
        """Инициализация графика."""
        self.csv_file_path = csv_file_path 

    def plot_graph(self, currency:str):
        if os.path.isfile(self.csv_file_path):
            df = pd.read_csv(self.csv_file_path )
            df['date'] = pd.to_datetime(df['date'])

            # Выбор валюты для отображения графика
            currency = st.selectbox("Выберите валюту для графика", options=df.columns[1:])

            if currency in df.columns:
                st.write(f"История курса {currency}")
                fig = px.line(df, x='date', y=currency, title=f"История курса {currency} за период")
                fig.update_layout(
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    xaxis_title="Дата",
                    yaxis_title=f"Курс ({currency})",
                    font=dict(size=14)
                )
                st.plotly_chart(fig)
            else:
                st.warning("Данные для выбранной валюты недоступны.")
        else:
            st.warning("Файл с историческими данными не найден. Пожалуйста, загрузите данные для отображения графика.")

# Инициализация класса конвертера валют

fetcher = Currency_data_fether()
converter = fetcher.converter
graph = Currency_plot(CSV_FILE_PATH)

# Интерфейс Streamlit для конвертации валют
st.title("Конвертер валют с историческими данными 💰")

# Обновление курсов валют и конвертация
if st.button("Обновить курсы валют"):
    fetcher.fetch_exchange_rates()

if converter.rates:
    amount = st.number_input("Сумма", min_value=0.0, format="%.2f", label_visibility = "visible")
    from_currency = st.selectbox("Из валюты", options=list(converter.rates.keys()))
    to_currency = st.selectbox("В валюту", options=list(converter.rates.keys()))

    if st.button("Конвертировать", type="primary"):
        result = converter.convert(amount, from_currency, to_currency)
        st.write(f"{amount} {from_currency} = {result:.2f} {to_currency}")
else:
    st.warning("Курсы валют не загружены. Нажмите 'Обновить курсы валют' для загрузки данных.")


# Выбор диапазона дат для загрузки исторических данных
st.header("Загрузка исторических данных", divider=True)
start_date = st.date_input("Начальная дата", datetime.now() - timedelta(days=365))
end_date = st.date_input("Конечная дата", datetime.now())

# Кнопка для загрузки данных
if st.button("Загрузить исторические данные"):
    fetcher.fetch_data_for_date_range(start_date, end_date)

# Отображение графика исторических курсов валют
st.header("График изменения курса валют", divider=True)

if converter.rates:
    currency = st.selectbox("Выберете валюту для отображения графика", options=list(converter.rates.keys()))
    graph.plot_graph(currency)
else:
    st.warning("Файл с историческими данными не найден. Пожалуйста, загрузите данные для отображения графика.")