import sqlite3

db_path = "database/biblioteca.db"

def main():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 1. Cria a nova tabela com a estrutura correta
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS emprestimos_nova (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER NOT NULL,
            livro_id INTEGER NOT NULL,
            data_emprestimo TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            data_devolucao_prevista TIMESTAMP NOT NULL,
            data_devolucao_real TIMESTAMP,
            status TEXT NOT NULL DEFAULT 'ativo'
        )
    """)

    # 2. Copia os dados compatíveis da tabela antiga para a nova
    try:
        cursor.execute("""
            INSERT INTO emprestimos_nova (id, cliente_id, livro_id, data_emprestimo, data_devolucao_prevista, data_devolucao_real, status)
            SELECT id,
                   COALESCE(cliente_id, 1),
                   livro_id,
                   data_emprestimo,
                   COALESCE(data_devolucao_prevista, data_emprestimo),
                   data_devolucao_real,
                   COALESCE(status, 'ativo')
            FROM emprestimos
        """)
    except Exception as e:
        print("Erro ao copiar dados:", e)
        print("Se a estrutura da tabela antiga for muito diferente, pode ser necessário ajustar manualmente.")
        conn.close()
        return

    # 3. Remove a tabela antiga
    cursor.execute("DROP TABLE emprestimos")

    # 4. Renomeia a nova tabela
    cursor.execute("ALTER TABLE emprestimos_nova RENAME TO emprestimos")

    conn.commit()
    conn.close()
    print("Migração concluída com sucesso!")

if __name__ == "__main__":
    main() 