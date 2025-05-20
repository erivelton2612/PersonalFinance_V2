# PersonalFinance

Sistema de classificação e análise de extratos financeiros, desenvolvido em Python com Streamlit e FastAPI.

## Funcionalidades

- Importação de extratos em CSV, Excel ou JSON
- Classificação automática de lançamentos
- Edição manual e revisão de classificações
- Visualização dinâmica de dados (tabela, gráficos, métricas)
- Tabela dinâmica interativa com agrupamento, filtros e totais (AgGrid)
- Integração com API FastAPI para persistência dos dados

## Estrutura do Projeto
PersonalFinance/ │ ├── .venv/ # Ambiente virtual (não versionar) ├── requirements.txt # Dependências do projeto ├── README.md # Este arquivo ├── parameters.py # Configurações globais (ex: API_URL) ├── function.py # Funções auxiliares e integração com API ├── backend/ # (Opcional) Código da API FastAPI │ ├── main.py │ ├── models.py │ └── ... ├── pages/ # Páginas do Streamlit │ ├── 01LandPage.py │ ├── 02ImportarExtrato.py │ ├── 03AnalisarExtrato.py │ └── ... └── data/ # (Opcional) Arquivos de dados de exemplo


## Como rodar localmente

1. **Clone o repositório:**
   ```sh
   git clone https://github.com/seuusuario/PersonalFinance.git
   cd PersonalFinance

   
   
## Como rodar localmente

1. **Clone o repositório:**
   ```sh
   git clone https://github.com/seuusuario/PersonalFinance.git
   cd PersonalFinance

   Crie e ative o ambiente virtual:

   python -m venv .venv
.venv\Scripts\activate   # Windows
# ou
source .venv/bin/activate  # Linux/Mac

Instale as dependências:

pip install -r requirements.txt

Configure o arquivo parameters.py:

Defina o API_URL para o endereço da sua API (local ou cloud).
Rode o backend (se estiver usando FastAPI local):

Rode o backend (se estiver usando FastAPI local):

uvicorn backend.main:app --reload
streamlit run app.py



## Deploy na Streamlit Cloud
Suba o projeto para o GitHub.
Certifique-se de que requirements.txt e parameters.py estão corretos para o ambiente cloud.
Faça o deploy em streamlit.io/cloud.



## Observações
Não versionar a pasta .venv (adicione ao .gitignore).
Para variáveis sensíveis, use arquivos .env ou variáveis de ambiente.
Para dúvidas ou sugestões, abra uma issue.