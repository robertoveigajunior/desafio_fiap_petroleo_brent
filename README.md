# Previsão do Preço do Petróleo Brent

Este projeto utiliza dados históricos do preço do petróleo Brent para prever os preços futuros usando a biblioteca Prophet. A aplicação é construída com Streamlit e está hospedada no Heroku com deploy automatizado usando GitHub Actions.

## Visão Geral

A previsão precisa dos preços do petróleo é essencial para a tomada de decisões em diversas indústrias. Este projeto visa fornecer uma ferramenta interativa para visualizar os preços históricos do petróleo Brent e prever preços futuros.

## Tecnologias Utilizadas

- Python
- Streamlit
- Prophet
- BeautifulSoup
- Seaborn
- Pandas
- lxml
- GitHub Actions
- Heroku

## Requisitos

Certifique-se de ter o seguinte instalado:

- Python 3.9 ou superior
- Conta no Heroku
- Conta no GitHub

## Instalação

1. Clone o repositório:

    ```sh
    git clone https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
    cd SEU_REPOSITORIO
    ```

2. Crie e ative um ambiente virtual:

    ```sh
    python -m venv env
    source env/bin/activate  # No Windows, use `env\Scripts\activate`
    ```

3. Instale as dependências:

    ```sh
    pip install -r requirements.txt
    ```

## Uso

Para rodar a aplicação localmente, execute:

```sh
streamlit run app.py
