import sqlite3
from datetime import datetime

DB_PATH = "database/biblioteca.db"

# 1. Empréstimos ativos
def relatorio_emprestimos_ativos(cursor):
    print("\n=== Empréstimos Ativos ===")
    cursor.execute('''
        SELECT c.nome, c.email, c.numero, l.titulo, l.autor, l.isbn, e.data_emprestimo, e.data_devolucao_prevista
        FROM emprestimos e
        JOIN clientes c ON e.cliente_id = c.id
        JOIN livros l ON e.livro_id = l.id
        WHERE e.status = 'ativo'
        ORDER BY e.data_emprestimo DESC
    ''')
    for row in cursor.fetchall():
        nome, email, numero, titulo, autor, isbn, data_emp, data_prev = row
        dias_restantes = (datetime.strptime(data_prev, "%Y-%m-%d %H:%M:%S") - datetime.now()).days
        print(f"Cliente: {nome} | Email: {email} | Tel: {numero}\n  Livro: {titulo} ({autor}) | ISBN: {isbn}\n  Empréstimo: {data_emp} | Prev. Devolução: {data_prev} | Dias Restantes: {dias_restantes}\n")

# 2. Livros mais emprestados
def relatorio_livros_mais_emprestados(cursor):
    print("\n=== Livros Mais Emprestados ===")
    cursor.execute('''
        SELECT l.titulo, l.autor, COUNT(e.id) as total
        FROM livros l
        LEFT JOIN emprestimos e ON l.id = e.livro_id
        GROUP BY l.id
        ORDER BY total DESC
        LIMIT 10
    ''')
    for titulo, autor, total in cursor.fetchall():
        print(f"{titulo} ({autor}) - {total} empréstimos")

# 3. Clientes com mais empréstimos
def relatorio_clientes_mais_emprestimos(cursor):
    print("\n=== Clientes com Mais Empréstimos ===")
    cursor.execute('''
        SELECT c.nome, c.email, COUNT(e.id) as total
        FROM clientes c
        LEFT JOIN emprestimos e ON c.id = e.cliente_id
        GROUP BY c.id
        ORDER BY total DESC
        LIMIT 10
    ''')
    for nome, email, total in cursor.fetchall():
        print(f"{nome} | {email} | {total} empréstimos")

# 4. Multas em aberto (fictício: considera atraso > 0)
def relatorio_multas_em_aberto(cursor):
    print("\n=== Multas em Aberto (Fictício) ===")
    cursor.execute('''
        SELECT c.nome, l.titulo, e.data_devolucao_prevista, e.data_emprestimo
        FROM emprestimos e
        JOIN clientes c ON e.cliente_id = c.id
        JOIN livros l ON e.livro_id = l.id
        WHERE e.status = 'ativo'
    ''')
    for nome, titulo, data_prev, data_emp in cursor.fetchall():
        if data_prev:
            dias_atraso = (datetime.now() - datetime.strptime(data_prev, "%Y-%m-%d %H:%M:%S")).days
            if dias_atraso > 0:
                valor_multa = dias_atraso * 2.0  # R$2,00 por dia de atraso (fictício)
                print(f"Cliente: {nome} | Livro: {titulo} | Dias de atraso: {dias_atraso} | Multa: R$ {valor_multa:.2f}")

# 5. Livros em atraso
def relatorio_livros_em_atraso(cursor):
    print("\n=== Livros em Atraso ===")
    cursor.execute('''
        SELECT c.nome, l.titulo, e.data_devolucao_prevista
        FROM emprestimos e
        JOIN clientes c ON e.cliente_id = c.id
        JOIN livros l ON e.livro_id = l.id
        WHERE e.status = 'ativo'
    ''')
    for nome, titulo, data_prev in cursor.fetchall():
        if data_prev:
            dias_atraso = (datetime.now() - datetime.strptime(data_prev, "%Y-%m-%d %H:%M:%S")).days
            if dias_atraso > 0:
                print(f"Cliente: {nome} | Livro: {titulo} | Dias de atraso: {dias_atraso}")

def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    relatorio_emprestimos_ativos(cursor)
    relatorio_livros_mais_emprestados(cursor)
    relatorio_clientes_mais_emprestimos(cursor)
    relatorio_multas_em_aberto(cursor)
    relatorio_livros_em_atraso(cursor)
    conn.close()

if __name__ == "__main__":
    main() 