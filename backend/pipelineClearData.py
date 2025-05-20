from datetime import datetime
import re

def limpar_data(data: str) -> str:
    """Limpa e formata a data para o formato YYYY-MM-DD"""
    if not data:
        return "1900-01-01"  # Define valor padrão se estiver vazio
    try:
        return datetime.strptime(data, "%Y-%m-%d").strftime("%Y-%m-%d")
    except ValueError:
        raise ValueError(f"Data inválida: {data}. Use o formato YYYY-MM-DD.")

def limpar_valor(valor: str) -> float:
    """Limpa valores monetários e converte para float"""
    if valor is None or valor == "":
        return 0.0
    # Remove R$ e vírgulas
    valor = re.sub(r'[^\d,.-]', '', str(valor))
    valor = valor.replace(",", ".")  # Garante que vírgulas sejam convertidas para ponto
    return float(valor)

def limpar_booleano(valor: str) -> bool:
    """Converte valores para booleano (True/False)"""
    if valor in ["Sim", "sim", "True", "1"]:
        return True
    elif valor in ["Não", "não", "False", "0"]:
        return False
    return False

def limpar_campos_extrato(item):
    """Limpa e ajusta os campos de um item de extrato antes de gravar"""
    item['DataDebito'] = limpar_data(item['DataDebito'])
    item['DataLancamento'] = limpar_data(item['DataLancamento'])
    item['Saldo'] = limpar_valor(item['Saldo'])
    item['ValorPrincipal'] = limpar_valor(item['ValorPrincipal'])
    item['Negativo'] = limpar_booleano(item['Negativo'])
    # Adicione outras limpezas se necessário (ex: remover espaços extras, validar campos obrigatórios, etc.)
    return item

def limpar_classificacao(item):
    """Limpa e ajusta os campos de classificação antes de gravar"""
    item['Referencia'] = item['Referencia'].strip() if item['Referencia'] else ""
    item['Tipo'] = item['Tipo'].strip() if item['Tipo'] else ""
    item['Subtipo'] = item['Subtipo'].strip() if item['Subtipo'] else ""
    return item
