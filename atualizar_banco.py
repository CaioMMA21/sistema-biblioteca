import sqlite3

db_path = "database/biblioteca.db"

def coluna_existe(cursor, tabela, coluna):
    cursor.execute(f"PRAGMA table_info({tabela})")
    return coluna in [info[1] for info in cursor.fetchall()]

def adicionar_coluna(cursor, tabela, coluna, tipo):
    if not coluna_existe(cursor, tabela, coluna):
        cursor.execute(f"ALTER TABLE {tabela} ADD COLUMN {coluna} {tipo}")

def main():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Adiciona as colunas se não existirem
    adicionar_coluna(cursor, "emprestimos", "cliente_id", "INTEGER")
    adicionar_coluna(cursor, "emprestimos", "data_devolucao_prevista", "TIMESTAMP")
    adicionar_coluna(cursor, "emprestimos", "data_devolucao_real", "TIMESTAMP")

    conn.commit()
    conn.close()
    print("Colunas adicionadas (se necessário) com sucesso!")

if __name__ == "__main__":
    main() 