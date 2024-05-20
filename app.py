import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from prophet import Prophet
import seaborn as sns
import numpy as np
import statsmodels.api as sm

# Título do aplicativo
st.title('Previsão de Preços do Petróleo Brent')

# Descrição do projeto
st.write("""
A previsão precisa dos preços do petróleo é essencial para a tomada de decisões em diversas indústrias.
Este projeto visa fornecer uma ferramenta interativa para visualizar os preços históricos do petróleo Brent e prever preços futuros.
""")

# Função para filtrar dados por período
def filter_data(df, start_date, end_date):
    start_date = pd.to_datetime(start_date)  # Conversão para datetime64[ns]
    end_date = pd.to_datetime(end_date)  # Conversão para datetime64[ns]
    mask = (df['ds'] >= start_date) & (df['ds'] <= end_date)
    return df.loc[mask]

# Função para carregar os dados
@st.cache_data
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
forecast2 = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]

# Visualização das previsões
st.subheader('Previsões Futuras')
fig2 = model.plot(forecast)
fig3 = model.plot(forecast2)
st.pyplot(fig2)
st.pyplot(fig3)

# Visualização dos componentes das previsões
st.subheader('Componentes das Previsões')
fig4 = model.plot_components(forecast)
st.pyplot(fig4)

# Dados reais
st.subheader('Dados Reais')
st.line_chart(df[['ds', 'y']].set_index('ds'))

# Mostrar previsão do modelo
st.subheader('Previsão do Modelo')
st.line_chart(forecast[['ds', 'yhat']].set_index('ds'))

# Visualização principal com matplotlib e seaborn
st.subheader('Visualização Completa')
plt.figure(figsize=(12, 6))
sns.set_style('whitegrid')
sns.lineplot(data=df, x='ds', y='y', label='Real')
sns.lineplot(data=forecast, x='ds', y='yhat', label='Modelo')
plt.title('Preço do Petróleo Brent (1987 - Presente)')
plt.xlabel('Data')
plt.ylabel('Preço de Fechamento (USD)')
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(plt)

# Análise de Tendências
st.subheader('Análise de Tendências')
start_date = st.date_input('Data de Início', df['ds'].min())
end_date = st.date_input('Data de Fim', df['ds'].max())
if st.button('Recarregar'):
    st.experimental_rerun()
filtered_data = filter_data(df, start_date, end_date)
st.line_chart(filtered_data[['ds', 'y']].set_index('ds'))

# Análise de Sazonalidade
st.subheader('Análise de Sazonalidade')
monthly_data = df.resample('M', on='ds').mean()
st.line_chart(monthly_data['y'])

# Dashboard 3: Distribuição de Preços
st.subheader('Distribuição de Preços')
filtered_data = filter_data(df, start_date, end_date)
plt.figure(figsize=(12, 6))
sns.histplot(filtered_data['y'], kde=True)
plt.title('Distribuição de Preços')
plt.xlabel('Preço de Fechamento (USD)')
plt.ylabel('Frequência')
plt.tight_layout()
st.pyplot(plt)

# ARIMA
st.subheader('ARIMA')
df_pred = forecast[['ds','yhat']].set_index('ds')
model = sm.tsa.ARIMA(df_pred, order=(1,1,1))  # Escolha dos parâmetros p, d, q
results = model.fit()
results.plot_diagnostics(figsize=(12, 8))
st.pyplot(plt)

# Correlação com Outros Indicadores
st.subheader('Correlação com Outros Indicadores')
# Aqui vamos simular um DataFrame de indicadores econômicos
np.random.seed(0)
periods = min(len(df), 400)  # Ajustar para um limite razoável
other_indicators = pd.DataFrame({
    'ds': pd.date_range(start=df['ds'].min(), periods=periods, freq='M'),
    'indicator_1': np.random.randn(periods),
    'indicator_2': np.random.randn(periods)
})
other_indicators.set_index('ds', inplace=True)
combined_data = df.set_index('ds').join(other_indicators)
correlation_matrix = combined_data.corr()

st.write('Matriz de Correlação')
st.dataframe(correlation_matrix)
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
plt.title('Matriz de Correlação entre Preço do Petróleo e Outros Indicadores')
st.pyplot(plt)
