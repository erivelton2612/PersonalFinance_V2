import requests

base_url = "http://127.0.0.1:8000"

extrato_data = [
    {
        "Id": 1, "DataDebito": "2025-01-03", "DataLancamento": "2025-01-03", "MeioPagamento": "PIX",
        "Lancamento": "Supermercado Pão de Açúcar", "Ref1": "Alimentação", "Saldo": 3200.00,
        "Negativo": False, "Ref2": "", "ref3": "", "PagoRecebido": "Pago", "ValorPrincipal": 235.80
    },
    {
        "Id": 2, "DataDebito": "2025-01-10", "DataLancamento": "2025-01-10", "MeioPagamento": "Débito",
        "Lancamento": "Cinema Multiplex", "Ref1": "Lazer", "Saldo": 2950.00,
        "Negativo": False, "Ref2": "", "ref3": "", "PagoRecebido": "Pago", "ValorPrincipal": 60.00
    },
    {
        "Id": 3, "DataDebito": "2025-02-05", "DataLancamento": "2025-02-05", "MeioPagamento": "PIX",
        "Lancamento": "Salário ACME S/A", "Ref1": "Receita", "Saldo": 6950.00,
        "Negativo": False, "Ref2": "", "ref3": "", "PagoRecebido": "Recebido", "ValorPrincipal": 4000.00
    },
    {
        "Id": 4, "DataDebito": "2025-02-15", "DataLancamento": "2025-02-15", "MeioPagamento": "Crédito",
        "Lancamento": "Rappi Pedido", "Ref1": "Delivery", "Saldo": 6770.00,
        "Negativo": False, "Ref2": "", "ref3": "", "PagoRecebido": "Pago", "ValorPrincipal": 180.00
    },
    {
        "Id": 5, "DataDebito": "2025-03-01", "DataLancamento": "2025-03-01", "MeioPagamento": "PIX",
        "Lancamento": "IPTU Prefeitura", "Ref1": "Moradia", "Saldo": 6200.00,
        "Negativo": False, "Ref2": "", "ref3": "", "PagoRecebido": "Pago", "ValorPrincipal": 570.00
    }
]

classificacao_data = [
    {"IDClass": 1, "Tipo": "Despesa", "Subtipo": "Alimentação", "Referencia": "supermercado"},
    {"IDClass": 2, "Tipo": "Despesa", "Subtipo": "Lazer", "Referencia": "cinema"},
    {"IDClass": 3, "Tipo": "Receita", "Subtipo": "Salário", "Referencia": "salário"},
    {"IDClass": 4, "Tipo": "Despesa", "Subtipo": "Delivery", "Referencia": "rappi"},
    {"IDClass": 5, "Tipo": "Despesa", "Subtipo": "Moradia", "Referencia": "iptu"}
]

# Inserir dados em Extrato
print("Inserindo dados na tabela Extrato...")
for item in extrato_data:
    resp = requests.post(f"{base_url}/extrato", json=item)
    print(f"Extrato {item['Id']}: {resp.status_code} - {resp.json()}")

# Inserir dados em Classificacao
print("\nInserindo dados na tabela Classificacao...")
for item in classificacao_data:
    resp = requests.post(f"{base_url}/classificacao", json=item)
    print(f"Classificação {item['IDClass']}: {resp.status_code} - {resp.json()}")
