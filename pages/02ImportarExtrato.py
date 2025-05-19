# app.py
import streamlit as st
import pandas as pd
from function import *

if "token" not in st.session_state or not st.session_state.token:
    # st.warning("Você precisa estar logado para acessar esta página.")
    # st.stop()
    st.switch_page("app.py")

st.set_page_config(page_title="Importar Arquivo", layout="wide")

# Importação de Arquivo
st.subheader("Importar Arquivo")
arquivo = st.file_uploader("Escolha um arquivo CSV, Excel ou JSON", type=["csv", "xlsx", "xls", "json"])

valor_decimal_virgula = st.checkbox("Decimal com vírgula (padrão: ponto)?")


df = pd.DataFrame()

if arquivo:
    try:
        if arquivo.name.endswith(".csv"):
            df = pd.read_csv(arquivo, decimal="," if valor_decimal_virgula else ".")
        elif arquivo.name.endswith(".json"):
            df = pd.read_json(arquivo)
        else:
            df = pd.read_excel(arquivo)
    except Exception as e:
        st.error(f"Erro ao ler o arquivo: {e}")

    st.success("Arquivo carregado com sucesso!")
    usar_data_fixa = st.checkbox("Importar com data fixa para todos")
    if usar_data_fixa:
        data_fixa = st.date_input("Padrão para 'Data Debito'")
    usar_meio_pagamento_fixo = st.checkbox("Meio Pagamento fixo para todos")
    if usar_meio_pagamento_fixo:
        meio_pagamento_fixo = st.selectbox("Valor padrão para 'MeioPagamento'",
                                        [None, "Crédito", "Débito", 
                                            "Transferência", "Dinheiro", "Cheque", "Boleto", "PIX", "Outros"], index=0)
    data_fixa = None
    meio_pagamento_fixo = None
    valor_negativo_recebido = st.checkbox("Valores negativos são recebidos (inverter lógica padrão?)")

    colunas_esperadas = ['DataDebito', 'DataLancamento', 'MeioPagamento', 'Lancamento', 'Ref1', 'Ref2', 'ref3', 'PagoRecebido', 'ValorPrincipal', 'ClasseSugerida','Accurace','Classe', 'Origem']
    colunas_esperadas = ['DataDebito', 'DataLancamento', 'MeioPagamento', 'Lancamento', 'Ref1', 'Ref2', 'ref3', 'PagoRecebido', 'ValorPrincipal', 'Classe']

    st.markdown("### Mapeamento de colunas")
    mapeamento = {}
    num_cols = 3
    cols = st.columns(num_cols)
    for i, col in enumerate(colunas_esperadas):
        with cols[i % num_cols]:
            mapeamento[col] = st.selectbox(f"'{col}'", 
                                            options=[None] + list(df.columns),
                                            index=0 if col not in df.columns 
                                            else list(df.columns).index(col))
    # for col in colunas_esperadas:
    #     mapeamento[col] = st.selectbox(f"Coluna para '{col}'", options=[None] + list(df.columns), index=0 if col not in df.columns else list(df.columns).index(col))

    df_mapeado = pd.DataFrame()
    for destino, origem in mapeamento.items():
        if origem and origem in df.columns:
            df_mapeado[destino] = df[origem]
        else:
            df_mapeado[destino] = None

    df = df_mapeado.copy()

    # Preenchimento automático de campos adicionais
    if data_fixa:
        df['DataDebito'] = pd.to_datetime(data_fixa)
    if meio_pagamento_fixo:
        df['MeioPagamento'] = meio_pagamento_fixo

    # ValorPrincipal pode vir com vírgula
    if 'ValorPrincipal' in df.columns:
        # Troca vírgula por ponto antes de converter
        df['ValorPrincipal'] = df['ValorPrincipal'].astype(str).str.replace(',', '.', regex=False)
        df['ValorPrincipal'] = pd.to_numeric(df['ValorPrincipal'], errors='coerce')


    # Definir PagoRecebido com base no ValorPrincipal
    if 'ValorPrincipal' in df.columns:
        df['PagoRecebido'] = df['ValorPrincipal'].apply(lambda x: 'Recebido' if (x < 0 if valor_negativo_recebido else x > 0) else 'Pago')
    
    # # Caso ja esteja classificado
    # if 'Classe' in df.columns:
    #     df['Origem'] = df['Classe'].apply(lambda x: 'Classe' if None else '💪')

    # Edição em tempo real
    edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)

    # Ajusta DataDebito para string no formato YYYY-MM-DD antes de enviar
    if 'DataDebito' in edited_df.columns:
        edited_df['DataDebito'] = pd.to_datetime(edited_df['DataDebito'], errors='coerce',dayfirst=True).dt.strftime('%Y-%m-%d')

    # Troca "Nenhum" por None (NaN) para evitar erro na API
    edited_df = edited_df.replace("Nenhum", None)
    edited_df = edited_df.replace("Nenhuma", None)

    # Ações
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Enviar para API"):
            enviar_dados(edited_df, st.session_state.token)
            st.success("Dados enviados com sucesso!")
    with col2:
        if st.button("Sair"):
            st.session_state.token = None
            st.session_state.username = ""
            st.rerun()
else:
    # Exibe extrato já salvo
    df = carregar_dados(st.session_state.token)
    if df.empty:
        st.info("Nenhum dado encontrado para este usuário.")
    else:
        st.dataframe(df, use_container_width=True)
        st.success("Dados carregados com sucesso!")
