# app.py
import streamlit as st
import pandas as pd
from function import *

st.set_page_config(page_title="Login", layout="wide")

if "token" not in st.session_state:
    st.session_state.token = None
if "username" not in st.session_state:
    st.session_state.username = ""


# LOGIN / REGISTRO
if not st.session_state.token:
    st.title("Acesso ao Sistema")
    aba = st.radio("Escolha uma opção", ["Login", "Registrar"])
    username = st.text_input("Usuário", value=st.session_state.username)
    password = st.text_input("Senha", type="password")

    if aba == "Login":
        if st.button("Entrar"):
            token = autenticar(username, password)
            if token:
                st.session_state.token = token
                st.session_state.username = username
                st.rerun()
            else:
                st.error("Usuário ou senha inválidos")

    elif aba == "Registrar":
        if st.button("Registrar e Entrar"):
            resp = registrar(username, password)
            if resp.status_code == 200:
                token = autenticar(username, password)
                if token:
                    st.session_state.token = token
                    st.session_state.username = username
                    st.rerun()
            else:
                st.error(resp.json().get("detail", "Erro ao registrar"))

    st.stop()

# ÁREA PRINCIPAL
st.sidebar.success(f"Autenticado como {st.session_state.username}")


# Após login bem-sucedido:
st.switch_page("pages/01LandPage.py")  # Caminho relativo ao root do projeto

# pagina = st.sidebar.selectbox("Menu", [ "Main","Sair"])

# if pagina == "Sair":
#     st.session_state.token = None
#     st.session_state.username = ""
#     st.rerun()




