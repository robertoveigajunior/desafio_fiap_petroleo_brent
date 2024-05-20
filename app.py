import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from prophet import Prophet

# Título do aplicativo
st.title('Previsão de Preços do Petróleo Brent')

# Descrição do projeto
st.write("""
A previsão precisa dos preços do petróleo é essencial para a tomada de decisões em diversas indústrias.
Este projeto visa fornecer uma ferramenta interativa para visualizar os preços históricos do petróleo Brent e prever preços futuros.
""")

# Função para carregar os dados
@st.cache
def load_data():
    url_ipea = 'http://www.ipeadata.gov.br/ExibeSerie.aspx?module=m&serid=1650971490&oper=view'
    response = requests.get(url_ipea)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', class_='dxgvControl')
        if table:
            df = pd.read_html(str(table))[1]
            df = df.rename(mapper = df.iloc[0], axis=1).drop(0, axis=0).reset_index(drop=True)
            df.rename(columns={df.columns[0]: 'ds', df.columns[1]: 'y'}, inplace=True)
            df['ds'] = pd.to_datetime(df['ds'], dayfirst=True)
            df['y'] = df['y'].astype('int64')
            return df
    return pd.DataFrame()

# Carregar dados
df = load_data()

# Mostrar os dados carregados
st.subheader('Dados Históricos')
st.write(df.head())

# Visualização dos dados
st.subheader('Visualização dos Dados Históricos')
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(df['ds'], df['y'], label='Preço do Petróleo Brent')
ax.set_xlabel('Data')
ax.set_ylabel('Preço (em R$)')
ax.set_title('Preços Históricos do Petróleo Brent')
ax.legend()
st.pyplot(fig)

# Treinamento do modelo Prophet
model = Prophet()
model.fit(df)

# Fazer previsões futuras
future = model.make_future_dataframe(periods=365)
forecast = model.predict(future)

# Visualização das previsões
st.subheader('Previsões Futuras')
fig2 = model.plot(forecast)
st.pyplot(fig2)

# Visualização dos componentes das previsões
st.subheader('Componentes das Previsões')
fig3 = model.plot_components(forecast)
st.pyplot(fig3)
