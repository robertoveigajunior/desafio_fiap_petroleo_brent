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
    git clone https://github.com/robertoveigajunior/desafio_fiap_petroleo_brent.git
    cd desafio_fiap_petroleo_brent
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
Acesse a aplicação no seu navegador em http://localhost:8501
```

## Deploy no Heroku

Este projeto está configurado para deploy automatizado no Heroku usando GitHub Actions.

### Configuração do Heroku

1. Aplicativo no Heroku:

    https://app-petroleo-brent-4b13f8521f0d.herokuapp.com/

### Configuração do GitHub Actions

O workflow do GitHub Actions (`.github/workflows/deploy.yml`) está configurado para:

- Instalar dependências
- Fazer login no Heroku
- Deploy automático no Heroku

### Executando o Deploy

Com o GitHub Actions configurado, qualquer push para a branch `main` disparará o workflow de deploy.

## Estrutura do Projeto

- `app.py`: Script principal da aplicação Streamlit.
- `requirements.txt`: Dependências do projeto.
- `Procfile`: Configuração para o Heroku.
- `.github/workflows/deploy.yml`: Workflow de deploy automatizado do GitHub Actions.

## Storytelling do Projeto

### Início

O projeto começou com a necessidade de prever os preços do petróleo Brent para ajudar na tomada de decisões estratégicas. Utilizamos dados históricos do preço do petróleo para treinar um modelo de previsão usando a biblioteca Prophet.

### Desenvolvimento

Criamos uma aplicação interativa usando Streamlit para visualizar os dados históricos e as previsões futuras. A aplicação permite aos usuários ver como os preços do petróleo variaram ao longo do tempo e obter previsões para o futuro.

### Deploy

Optamos por hospedar a aplicação no Heroku para facilitar o acesso e a escalabilidade. Configuramos GitHub Actions para automação do deploy, garantindo que as atualizações sejam refletidas automaticamente na aplicação hospedada.

### Desafios

Enfrentamos alguns desafios durante o deploy, como a instalação de dependências específicas (`beautifulsoup4`, `seaborn`, `lxml`). Resolvemos esses problemas adicionando as dependências necessárias ao arquivo `requirements.txt`.

### Conclusão

O resultado é uma ferramenta poderosa e acessível para prever os preços do petróleo Brent, hospedada no Heroku e pronta para ser utilizada por qualquer pessoa interessada em análises de mercado.

