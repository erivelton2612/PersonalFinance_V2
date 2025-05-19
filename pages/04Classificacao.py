# app.py
import streamlit as st
import pandas as pd
from function import *

if "token" not in st.session_state or not st.session_state.token:
    # st.warning("Você precisa estar logado para acessar esta página.")
    # st.stop()
    st.switch_page("app.py")

st.subheader("Classificações")
arquivo = st.file_uploader("Escolha um arquivo CSV, Excel ou JSON", type=["csv", "xlsx", "xls", "json"])

df = pd.DataFrame()

if arquivo:
    try:
        if arquivo.name.endswith(".csv"):
            df = pd.read_csv(arquivo)
        elif arquivo.name.endswith(".json"):
            df = pd.read_json(arquivo)
        else:
            df = pd.read_excel(arquivo)
    except Exception as e:
        st.error(f"Erro ao ler o arquivo: {e}")

    st.success("Arquivo carregado com sucesso!")

    colunas_esperadas = ['Tipo', 'Subtipo', 'Referencia']

    st.markdown("### Mapeamento de colunas")
    mapeamento = {}
    for col in colunas_esperadas:
        mapeamento[col] = st.selectbox(f"Coluna para '{col}'", options=[None] + list(df.columns), index=0 if col not in df.columns else list(df.columns).index(col))

    df_mapeado = pd.DataFrame()
    for destino, origem in mapeamento.items():
        if origem and origem in df.columns:
            df_mapeado[destino] = df[origem]
        else:
            df_mapeado[destino] = None

    df = df_mapeado.copy()

    # Edição em tempo real
    edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)

    # Troca "Nenhum" e "Nenhuma" por None para evitar erro na API
    edited_df = edited_df.replace(["Nenhum", "Nenhuma"], None)

    
    # Ações
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Enviar para API"):
            enviar_class(edited_df, st.session_state.token)
            st.success("Dados enviados com sucesso!")
    with col2:
        if st.button("Sair"):
            st.session_state.token = None
            st.session_state.username = ""
            st.rerun()
else:
    # Exibe extrato já salvo
    df = carregar_class(st.session_state.token)
    if df.empty:
        st.info("Nenhum dado encontrado para este usuário.")
    else:
        st.dataframe(df, use_container_width=True)
        st.success("Dados carregados com sucesso!")
