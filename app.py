import pandas as pd
import requests
import streamlit as st
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import seaborn as sns
from prophet import Prophet
import numpy as np

# Função para carregar e processar os dados
def load_data():
    url_ipea = 'http://www.ipeadata.gov.br/ExibeSerie.aspx?module=m&serid=1650971490&oper=view'
    response = requests.get(url_ipea)

    df = pd.DataFrame()
    if response.status_code != 200:
        st.error('Erro HTTP ao baixar os dados do módulo: ' + url_ipea)
    else:
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', class_='dxgvControl')

        if table:
            df = pd.read_html(str(table))[1]
            df = df.rename(mapper=df.iloc[0], axis=1).drop(0, axis=0).reset_index(drop=True)
            df.rename(columns={df.columns[0]: 'ds', df.columns[1]: 'y'}, inplace=True)
            df['y'] = df['y'].astype('int64')
        else:
            st.error("Nenhuma tabela carregada")
    
    if not df.empty:
        df['y'] = df['y'].astype('float64').apply(lambda x: x/100)
        df['ds'] = pd.to_datetime(df['ds'], format='%d/%m/%Y')
    
    return df

# Carregar dados
df = load_data()

# Treinar o modelo Prophet
model = Prophet()
model.fit(df)

# Prever dados futuros
future = model.make_future_dataframe(periods=365)
forecast = model.predict(future)
forecast = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]

# Função para filtrar dados por período
def filter_data(df, start_date, end_date):
    start_date = pd.to_datetime(start_date)  # Conversão para datetime64[ns]
    end_date = pd.to_datetime(end_date)  # Conversão para datetime64[ns]
    mask = (df['ds'] >= start_date) & (df['ds'] <= end_date)
    return df.loc[mask]

# Criar interface no Streamlit
st.title('Previsão do Preço do Petróleo Brent')
st.write('Modelo de Previsão usando Prophet')

# Mostrar dados reais
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

# Dashboard 1: Análise de Tendências
st.subheader('Dashboard 1: Análise de Tendências')
start_date = st.date_input('Data de Início', df['ds'].min())
end_date = st.date_input('Data de Fim', df['ds'].max())
if st.button('Recarregar'):
    st.experimental_rerun()
filtered_data = filter_data(df, start_date, end_date)
st.line_chart(filtered_data[['ds', 'y']].set_index('ds'))

# Dashboard 2: Análise de Sazonalidade
st.subheader('Dashboard 2: Análise de Sazonalidade')
monthly_data = df.resample('M', on='ds').mean()
st.line_chart(monthly_data['y'])

# Dashboard 3: Distribuição de Preços
st.subheader('Dashboard 3: Distribuição de Preços')
filtered_data = filter_data(df, start_date, end_date)
plt.figure(figsize=(12, 6))
sns.histplot(filtered_data['y'], kde=True)
plt.title('Distribuição de Preços')
plt.xlabel('Preço de Fechamento (USD)')
plt.ylabel('Frequência')
plt.tight_layout()
st.pyplot(plt)

# Dashboard 4: Correlação com Outros Indicadores
st.subheader('Dashboard 4: Correlação com Outros Indicadores')
# Supondo que temos um DataFrame `other_indicators` com dados de outros indicadores econômicos
# other_indicators = pd.read_csv('path_to_other_indicators.csv')  # Carregar outros indicadores
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
