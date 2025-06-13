import re
from datetime import datetime

def validar_email(email):
    """Valida se o email está em um formato válido."""
    padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(padrao, email))

def validar_senha(senha):
    """Valida se a senha atende aos requisitos mínimos."""
    if len(senha) < 6:
        return False
    if not re.search(r'[A-Z]', senha):
        return False
    if not re.search(r'[a-z]', senha):
        return False
    if not re.search(r'\d', senha):
        return False
    return True

def formatar_data(data_str):
    """Formata uma string de data para o formato brasileiro."""
    try:
        data = datetime.strptime(data_str, "%Y-%m-%d %H:%M:%S")
        return data.strftime("%d/%m/%Y %H:%M")
    except:
        return data_str

def formatar_moeda(valor):
    """Formata um valor numérico para o formato de moeda brasileira."""
    return f"R$ {valor:.2f}".replace(".", ",")

def calcular_dias_entre_datas(data_inicio, data_fim):
    """Calcula o número de dias entre duas datas."""
    try:
        inicio = datetime.strptime(data_inicio, "%Y-%m-%d %H:%M:%S")
        fim = datetime.strptime(data_fim, "%Y-%m-%d %H:%M:%S")
        return (fim - inicio).days
    except:
        return 0

def validar_isbn(isbn):
    """Valida se o ISBN está em um formato válido."""
    # Remove hífens e espaços
    isbn = isbn.replace("-", "").replace(" ", "")
    
    # Verifica se tem 10 ou 13 dígitos
    if len(isbn) not in [10, 13]:
        return False
        
    # Verifica se todos os caracteres são dígitos (exceto o último que pode ser X)
    if not isbn[:-1].isdigit() or (not isbn[-1].isdigit() and isbn[-1].upper() != 'X'):
        return False
        
    return True

def formatar_telefone(telefone):
    """Formata um número de telefone para o formato brasileiro."""
    # Remove caracteres não numéricos
    numeros = re.sub(r'\D', '', telefone)
    
    if len(numeros) == 11:  # Celular
        return f"({numeros[:2]}) {numeros[2:7]}-{numeros[7:]}"
    elif len(numeros) == 10:  # Telefone fixo
        return f"({numeros[:2]}) {numeros[2:6]}-{numeros[6:]}"
    else:
        return telefone

def gerar_relatorio_emprestimos(emprestimos):
    """Gera um relatório formatado de empréstimos."""
    relatorio = []
    relatorio.append("RELATÓRIO DE EMPRÉSTIMOS")
    relatorio.append("=" * 50)
    
    for emp in emprestimos:
        relatorio.append(f"ID: {emp[0]}")
        relatorio.append(f"Livro: {emp[8]}")  # título do livro
        relatorio.append(f"Usuário: {emp[9]}")  # nome do usuário
        relatorio.append(f"Data Empréstimo: {formatar_data(emp[3])}")
        if emp[4]:  # data_devolucao
            relatorio.append(f"Data Devolução: {formatar_data(emp[4])}")
        relatorio.append(f"Status: {emp[5]}")
        if emp[6]:  # multa
            relatorio.append(f"Multa: {formatar_moeda(emp[6])}")
        relatorio.append("-" * 50)
    
    return "\n".join(relatorio) 