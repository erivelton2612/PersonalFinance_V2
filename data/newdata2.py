import requests
import json

# URL base da sua API FastAPI
BASE_URL = "http://127.0.0.1:8000"  # Modifique caso sua API esteja em outro endereço

# Teste 1: Incluir um extrato com dados válidos
extrato_valido = {
    "Id": 1,
    "DataDebito": "2025-05-10",  # Data válida
    "DataLancamento": "2025-05-12",  # Data válida
    "MeioPagamento": "Cartão",
    "Lancamento": "Pagamento",
    "Ref1": "Ref001",
    "Saldo": 100.5,
    "Negativo": False,
    "Ref2": "Ref002",
    "ref3": "Ref003",
    "PagoRecebido": "Pago",
    "ValorPrincipal": 150.0
}

# Teste 2: Incluir um extrato com uma data inválida (formato errado)
extrato_invalido = {
    "Id": 2,
    "DataDebito": "10/05/2025",  # Formato de data inválido
    "DataLancamento": "2025-05-12",
    "MeioPagamento": "Cartão",
    "Lancamento": "Pagamento",
    "Ref1": "Ref003",
    "Saldo": 200.0,
    "Negativo": True,
    "Ref2": "Ref004",
    "ref3": "Ref005",
    "PagoRecebido": "Não Pago",
    "ValorPrincipal": 250.0
}

# Teste 3: Incluir uma classificação com dados válidos
classificacao_valida = {
    "IDClass": 1,
    "Tipo": "Despesa",
    "Subtipo": "Alimentação",
    "Referencia": "Ref001"
}

# Função para enviar requisições POST para incluir extratos
def incluir_extrato(data):
    response = requests.post(f"{BASE_URL}/extrato", json=data)
    return response

# Função para enviar requisições POST para incluir classificações
def incluir_classificacao(data):
    response = requests.post(f"{BASE_URL}/classificacao", json=data)
    return response

# Teste 1: Incluir um extrato válido
print("Testando extrato válido...")
response = incluir_extrato(extrato_valido)
print(f"Status Code: {response.status_code}")
print(f"Resposta: {response.json()}")

# Teste 2: Incluir um extrato inválido (data errada)
print("\nTestando extrato inválido (data errada)...")
response = incluir_extrato(extrato_invalido)
print(f"Status Code: {response.status_code}")
print(f"Resposta: {response.json()}")

# Teste 3: Incluir uma classificação válida
print("\nTestando classificação válida...")
response = incluir_classificacao(classificacao_valida)
print(f"Status Code: {response.status_code}")
print(f"Resposta: {response.json()}")
