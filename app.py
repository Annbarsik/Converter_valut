from Currency_data_fether import *
from Currency_plot import *


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