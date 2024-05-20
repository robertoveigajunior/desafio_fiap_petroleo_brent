import pandas as pd
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from prophet import Prophet

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

model = Prophet()
model.fit(df)
future = model.make_future_dataframe(periods=365)
forecast = model.predict(future)
forecast = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]

model.plot(forecast)

forecast.yhat

df_predict = pd.concat([future, forecast.yhat], axis=1)
df.ds = pd.to_datetime(df.ds, format='%d/%m/%Y')

plt.figure(figsize=(12, 6))
sns.set_style('whitegrid')
sns.lineplot(data=df, x='ds', y='y', label='real')
sns.lineplot(data=df_predict, x='ds', y='yhat', label='modelo')
plt.title('Preço do Petróleo Brent (1987 - Presente)')
plt.xlabel('Data')
plt.ylabel('Preço de Fechamento (USD)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


st.write('Feito com Streamlit :)')