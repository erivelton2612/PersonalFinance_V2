# app.py
import streamlit as st
import pandas as pd
import requests
import Levenshtein


API_URL = "http://127.0.0.1:8000"
# Funções auxiliares
def autenticar(username, password):
    response = requests.post(f"{API_URL}/token", data={"username": username, "password": password})
    if response.status_code == 200:
        return response.json()["access_token"]
    return None

def registrar(username, password):
    response = requests.post(f"{API_URL}/register", json={"username": username, "password": password})
    return response

def carregar_dados(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_URL}/extrato", headers=headers)
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    return pd.DataFrame()

def carregar_class(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_URL}/classificacao", headers=headers)
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    return pd.DataFrame()

def enviar_dados(df, token):
    headers = {"Authorization": f"Bearer {token}"}
    erros = 0
    total = len(df)
    for idx, row in df.iterrows():
        payload = row.to_dict()
        try:    
            response = requests.post(f"{API_URL}/extrato", headers=headers, json=payload)
            if response.status_code != 200:
                erros +=1
        except Exception:
            erros += 1
                # st.error(f"Erro ao enviar linha: {payload}")
    st.success(f"Importação finalizada: {total-erros} de {total} registros importados com sucesso. {erros} erro(s) ignorado(s).")

def enviar_class(df, token):
    headers = {"Authorization": f"Bearer {token}"}
    erros = 0
    total = len(df)
    for _, row in df.iterrows():
        payload = row.to_dict()
        try:
            response = requests.post(f"{API_URL}/classificacao", headers=headers, json=payload)
            if response.status_code != 200:
                erros += 1
        except Exception:
            erros += 1
    st.success(f"Importação finalizada: {total-erros} de {total} registros importados com sucesso. {erros} erro(s) ignorado(s).")
#funcoes de classificação
# Classificação de Distancias

# Carrega classificação da API
def carregar_classificacao(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_URL}/classificacao", headers=headers)
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    return pd.DataFrame()

# Função de sugestão de classe
def classificar_descricao(descricao, classificacao):
    melhor_categoria = None
    menor_distancia = float('inf')
    
    for _, row in classificacao.iterrows():
        
        distancia = Levenshtein.distance(descricao.upper(), str(row['Referencia']).upper())
        if distancia < menor_distancia:
            menor_distancia = distancia
            melhor_categoria = row['Tipo']
    
    return melhor_categoria, menor_distancia

def origem_icon(row):
    if row["Classe"] not in [None, ""]:
        return ":writing_hand:"
    elif row["Origem"] == "Distancia":
        return ":triangular_ruler:"
    elif row["Origem"] == "IA":
        return ":chart_with_upwards_trend:"
    else:
        return ":triangular_ruler:"