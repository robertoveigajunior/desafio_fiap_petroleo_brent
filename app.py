import pandas as pd
import requests
import streamlit as st
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from prophet import Prophet

# Carregar dados
url_ipea = 'http://www.ipeadata.gov.br/ExibeSerie.aspx?module=m&serid=1650971490&oper=view'
response = requests.get(url_ipea)

df = pd.DataFrame()
if response.status_code != 200:
    print(' HTTP error while downloading the module ' + url_ipea)
else:

    print(' HTTP response from the module ' + url_ipea)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', class_='dxgvControl')

    if table:
        df = pd.read_html(str(table))[1]  # Se houver mais de uma tabela, ajuste o índice
        df = df.rename(mapper = df.iloc[0], axis=1).drop(0, axis=0).reset_index(drop=True)
        df.rename(columns={df.columns[0]: 'ds', df.columns[1]: 'y'}, inplace=True)
        df.y = df.y.astype('int64')

    else:
        print("Not table loaded")

df.head()      
df.ds.unique()
df.isna().any()
df.duplicated().any()
df.iloc[:, 1].describe()
df.y = df.y.astype('float64').apply(lambda x: x/100)

# Treinar o modelo Prophet
model = Prophet()
model.fit(df)

# Prever dados futuros
future = model.make_future_dataframe(periods=365)
forecast = model.predict(future)
forecast = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]

# Criar interface no Streamlit
st.title('Previsão do Preço do Petróleo Brent')
st.write('Modelo de Previsão usando Prophet')

# Mostrar dados reais
st.subheader('Dados Reais')
st.line_chart(df[['ds', 'y']].set_index('ds'))

# Mostrar previsão do modelo
st.subheader('Previsão do Modelo')
st.line_chart(forecast[['ds', 'yhat']].set_index('ds'))

st.write('Feito com Streamlit')