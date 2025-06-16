from database.database import Database
from datetime import datetime, timedelta

class Emprestimo:
    def __init__(self):
        self.db = Database()
        
    def adicionar(self, cliente_id, livro_id, dias):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        try:
            # Verifica se o livro está disponível
            cursor.execute("SELECT disponivel FROM livros WHERE id = ?", (livro_id,))
            disponivel = cursor.fetchone()[0]
            
            if disponivel <= 0:
                return False, "Livro não disponível para empréstimo"
            
            # Calcula a data de devolução prevista
            data_emprestimo = datetime.now()
            data_devolucao = data_emprestimo + timedelta(days=dias)
            
            # Registra o empréstimo
            cursor.execute(
                """
                INSERT INTO emprestimos (cliente_id, livro_id, data_devolucao_prevista)
                VALUES (?, ?, ?)
                """,
                (cliente_id, livro_id, data_devolucao)
            )
            
            # Atualiza a quantidade disponível do livro
            cursor.execute(
                "UPDATE livros SET disponivel = disponivel - 1 WHERE id = ?",
                (livro_id,)
            )
            
            conn.commit()
            return True, "Empréstimo registrado com sucesso"
            
        except Exception as e:
            conn.rollback()
            return False, f"Erro ao registrar empréstimo: {str(e)}"
        finally:
            conn.close()
            
    def listar_todos(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """
            SELECT e.*, c.nome as cliente_nome, l.titulo as livro_titulo
            FROM emprestimos e
            JOIN clientes c ON e.cliente_id = c.id
            JOIN livros l ON e.livro_id = l.id
            ORDER BY e.data_emprestimo DESC
            """
        )
        emprestimos = cursor.fetchall()
        
        conn.close()
        return emprestimos
        
    def buscar_por_cliente(self, cliente_id):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """
            SELECT e.*, c.nome as cliente_nome, l.titulo as livro_titulo
            FROM emprestimos e
            JOIN clientes c ON e.cliente_id = c.id
            JOIN livros l ON e.livro_id = l.id
            WHERE e.cliente_id = ?
            ORDER BY e.data_emprestimo DESC
            """,
            (cliente_id,)
        )
        emprestimos = cursor.fetchall()
        
        conn.close()
        return emprestimos
        
    def buscar_por_livro(self, livro_id):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """
            SELECT e.*, c.nome as cliente_nome, l.titulo as livro_titulo
            FROM emprestimos e
            JOIN clientes c ON e.cliente_id = c.id
            JOIN livros l ON e.livro_id = l.id
            WHERE e.livro_id = ?
            ORDER BY e.data_emprestimo DESC
            """,
            (livro_id,)
        )
        emprestimos = cursor.fetchall()
        
        conn.close()
        return emprestimos
        
    def registrar_devolucao(self, emprestimo_id):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        try:
            # Busca informações do empréstimo
            cursor.execute(
                "SELECT livro_id, data_devolucao_prevista FROM emprestimos WHERE id = ?",
                (emprestimo_id,)
            )
            emprestimo = cursor.fetchone()
            
            if not emprestimo:
                return False, "Empréstimo não encontrado"
                
            livro_id, data_prevista = emprestimo
            
            # Registra a devolução
            cursor.execute(
                """
                UPDATE emprestimos 
                SET data_devolucao_real = CURRENT_TIMESTAMP,
                    status = 'devolvido'
                WHERE id = ?
                """,
                (emprestimo_id,)
            )
            
            # Atualiza a quantidade disponível do livro
            cursor.execute(
                "UPDATE livros SET disponivel = disponivel + 1 WHERE id = ?",
                (livro_id,)
            )
            
            conn.commit()
            return True, "Devolução registrada com sucesso"
            
        except Exception as e:
            conn.rollback()
            return False, f"Erro ao registrar devolução: {str(e)}"
        finally:
            conn.close() 