# 							"Конвертер валют"

#1.Определение:
Конвертер валют — это инструмент, который позволяет пользователям быстро и удобно преобразовывать одну валюту в другую на основе курсов обмена и отобразить график изменения валют за выбранный период.

#2.Функциональность:
Преобразование валют.
 
Как работает конвертер валют?
Ввод данных: Пользователь вводит сумму, исходную и целевую валюту.
Получение курса: Конвертер запрашивает актуальный курс по имеющимся валютам freecurrencyAPI (около 30 валют в бесплатной версии).
Расчет: На основе введенной суммы и полученного курса выполняется расчет.
Вывод результата: Пользователь получает результат конвертации.
Загрузка данных: Пользователь выбирает необходимый диапазон дат с помощью freecurrencyAPI.
Отображение графика: Пользователь может выбрать необходимую валюту, для отображения ее в зависимости от выбранного интервала дат на этапе загрузки данных.

#3.Архитектура проекта:
Имеются три класса, а именно:
3.1. Класс CurrencyConverter: отвечает за загрузку, сохранение и конвертацию текущих курсов валют.
3.2. Класс Currency_data_fether: отвечает за управление загрузкой данных через API, влючая текущие и исторические данные.
3.3. Класс Currency_plot: нужен для построения графика истории и изменения курса валют.


#4.Примеры использования:
4.1.Личные финансы: Люди, путешествующие за границу, могут использовать конвертеры для понимания стоимости товаров и услуг в другой валюте.
4.2.Бизнес: Компании, работающие с международными клиентами или поставщиками, могут использовать конвертеры для расчета цен и затрат.

#5.Заключение:
Конвертер валют — это полезный инструмент для быстрого и точного преобразования денежных единиц. Он играет важную роль в финансовых операциях как для частных лиц, так и для бизнеса, обеспечивая доступ к данным о курсах обмена.

#6.Установка:
1.Клонируйте репозиторий: git clone
2.Установка зависимостей pip install -r requirements.txt
3.Регистрация на FreecurrencyAPI (https://freecurrencyapi.com/) и получение API-ключа.
4.Создание файла  .env : API_KEY = Ваш API-ключ.
5.Запуск проекта: streamlit run app.py
