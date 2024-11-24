import streamlit as st
import os
import pandas as pd
import plotly.express as px

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
