# app.py
import streamlit as st
import pandas as pd
from function import *

if "token" not in st.session_state or not st.session_state.token:
    # st.warning("Você precisa estar logado para acessar esta página.")
    # st.stop()
    st.switch_page("app.py")


st.subheader("Analisar Extrato")
# if "df_importado" not in st.session_state:
#     st.warning("Nenhum extrato importado encontrado. Vá para a aba 'Importar Extrato'.")
#     st.stop()

df = carregar_dados(st.session_state.token)
if df.empty:
    st.info("Nenhum dado encontrado para este usuário.")
    st.stop()


# Carrega classificações
dfClass = carregar_classificacao(st.session_state.token)
if not dfClass.empty:
    df[['ClasseSugerida','Accurace']] = df['Lancamento'].astype(str).apply(lambda x: pd.Series(classificar_descricao(x, dfClass)))
else:
    st.warning("Não foi possível carregar a tabela de classificação.")

# edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)

# Supondo que dfClass['Tipo'] contém as opções únicas de classe
opcoes_classe = dfClass['Tipo'].dropna().unique().tolist()

df["Origem"] = df["Origem"].astype(str).apply(lambda x: "Origem" if x == "" else "🦾")
edited_df = st.data_editor(
        df, 
        num_rows="dynamic", 
        use_container_width=True,
        column_config={
            "DataDebito": st.column_config.TextColumn("Débito",width="small"),
            "DataLancamento": st.column_config.TextColumn("Lançamento",width="small"),
            "MeioPagamento": st.column_config.TextColumn("Meio",width="small"),
            "Lancamento": st.column_config.TextColumn("Lançamento"),
            "Ref1": st.column_config.TextColumn("Ref1",width="small"),
            "Ref2": st.column_config.TextColumn("Ref2",width="small"),
            "ref3": st.column_config.TextColumn("ref3",width="small"),
            "PagoRecebido": st.column_config.TextColumn("P/R",width="small"),
            "ValorPrincipal": st.column_config.Column("Valor Principal"),
            "ClasseSugerida": st.column_config.TextColumn("Classe Sugerida"),
            # "Classe": st.column_config.SelectboxColumn("Classe"),
            # ...outras colunas...
            "Classe": st.column_config.SelectboxColumn(
                "Classe",
                options=opcoes_classe,
                required=False,
                width="small"
            ),
            "Origem": st.column_config.TextColumn("Origem",width="small"),
            "Detalhes": st.column_config.LinkColumn(
            "Det", 
            help="Clique para ver detalhes", 
            display_text="👻",width="small",),
            #url="https://www.myapp.com/detalhes/"  # ou use um valor dinâmico se quiser
        },
        column_order=["DataDebito", "DataLancamento", "MeioPagamento",
                        "Lancamento", "PagoRecebido",
                        "ValorPrincipal", "ClasseSugerida","Accurace", "Classe", "Origem","Detalhes", 
                        "Ref1", "Ref2", "ref3"],
        disabled=["Id", "user_id","DataDebito","Lancamento"],
        hide_index=True,
    )

# Processar Classificações
if st.button("Processar Classificações"):
    edited_df['Classe'] = edited_df.apply(
        lambda row: row['Classe'] if pd.notnull(row['Classe']) and row['Classe'] != '' and row['Accurace']>11 
        else row['ClasseSugerida'],
        axis=1
    )
    st.success("Campo 'Classe' preenchido com base em 'ClasseSugerida'")

edited_df["Origem"] = edited_df.apply(origem_icon, axis=1)

# edited_df["Origem"].astype(str).apply(lambda x: "Origem" if x == "" else "🦾")
edited_df = st.data_editor(
        edited_df, 
        num_rows="dynamic", 
        use_container_width=True,
        column_config={
            "DataDebito": st.column_config.TextColumn("Débito",width="small"),
            "DataLancamento": st.column_config.TextColumn("Lançamento",width="small"),
            "MeioPagamento": st.column_config.TextColumn("Meio",width="small"),
            "Lancamento": st.column_config.TextColumn("Lançamento"),
            "Ref1": st.column_config.TextColumn("Ref1",width="small"),
            "Ref2": st.column_config.TextColumn("Ref2",width="small"),
            "ref3": st.column_config.TextColumn("ref3",width="small"),
            "PagoRecebido": st.column_config.TextColumn("P/R",width="small"),
            "ValorPrincipal": st.column_config.Column("Valor Principal"),
            "ClasseSugerida": st.column_config.TextColumn("Classe Sugerida"),
            "Classe": st.column_config.TextColumn("Classe"),
            "Origem": st.column_config.TextColumn("Origem",width="small"),
            "Detalhes": st.column_config.LinkColumn(
            "Det", 
            help="Clique para ver detalhes", 
            display_text="👻",width="small",),
            #url="https://www.myapp.com/detalhes/"  # ou use um valor dinâmico se quiser
        },
        column_order=["DataDebito", "DataLancamento", "MeioPagamento",
                        "Lancamento", "PagoRecebido",
                        "ValorPrincipal", "ClasseSugerida","Accurace", "Classe", "Origem","Detalhes", 
                        "Ref1", "Ref2", "ref3"],
        disabled=["Id", "user_id","DataDebito","Lancamento"],
        hide_index=True,
    )

col1, col2 = st.columns(2)
with col1:
    if st.button("Enviar para API"):
        enviar_dados(edited_df, st.session_state.token)
        st.success("Dados enviados com sucesso!")
with col2:
    if st.button("Voltar"):
        st.switch_page("app.py")

col1, col2 = st.columns(2)
with col1:
    # Exibir gráfico de barras
    if st.button("Gerar Gráfico de Classes"):
        classes = df['Classe'].value_counts()
        st.bar_chart(classes)
with col2:
# Exibir gráfico de pizza
    if st.button("Gerar Gráfico de Classes (Pizza)"):
        classes = df['Classe'].value_counts()
        st.pyplot(classes.plot.pie(autopct='%1.1f%%', startangle=90).get_figure())
