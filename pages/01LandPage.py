# app.py
import streamlit as st
import pandas as pd
from function import *

# LandPage.py
st.set_page_config(page_title="Página Inicial")

st.title("Sistema de Classificação")
st.write("Bem-vindo ao sistema de classificação. Selecione uma opção no menu lateral.")
# st.sidebar.markdown("### Opções")
# st.sidebar.markdown("- [Importar Extrato](pages/ImportarExtrato.py)")
# st.sidebar.markdown("- [Classificações](pages/Classificacao.py)")


df = pd.DataFrame()
df = carregar_dados(st.session_state.token)
df["Detalhes"] = "Ver detalhes"

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
        "Classe": st.column_config.TextColumn("Classe"),
        "Origem": st.column_config.TextColumn("Origem",width="small"),
        "Detalhes": st.column_config.LinkColumn(
        "Det", 
        help="Clique para ver detalhes", 
        display_text="👻",width="small"),
        #url="https://www.myapp.com/detalhes/"  # ou use um valor dinâmico se quiser
    },
    column_order=["DataDebito", "DataLancamento", "MeioPagamento",
                    "Lancamento", "PagoRecebido",
                    "ValorPrincipal", "ClasseSugerida", "Classe", "Origem","Detalhes", 
                    "Ref1", "Ref2", "ref3","Accurace"],
    disabled=["Id", "user_id","DataDebito"],
    hide_index=True,
)

pagina = st.sidebar.selectbox("Menu", [ "Main","Sair"])

if pagina == "Sair":
    st.session_state.token = None
    st.session_state.username = ""
    st.rerun()
