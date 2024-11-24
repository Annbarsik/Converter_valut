from CurrencyConverter import *
import os
import pandas as pd
from dotenv import load_dotenv
import time
import freecurrencyapi
from datetime import datetime, timedelta


# Загрузка API-ключа из .env файла
load_dotenv()
API_KEY = os.getenv("API_KEY")
client = freecurrencyapi.Client(API_KEY)
CSV_FILE_PATH = 'currency_rates.csv'


    
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