from database.database import Database
from datetime import datetime, timedelta

class Emprestimo:
    def __init__(self):
        self.db = Database()
        self.dias_emprestimo = 15
        self.valor_multa_dia = 1.0
        
    def criar(self, livro_id, usuario_id):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        try:
            # Verifica se o livro está disponível
            cursor.execute("SELECT disponivel FROM livros WHERE id = ?", (livro_id,))
            disponivel = cursor.fetchone()
            
            if not disponivel or disponivel[0] <= 0:
                return False, "Livro não disponível"
                
            # Cria o empréstimo
            cursor.execute(
                """
                INSERT INTO emprestimos (livro_id, usuario_id, status)
                VALUES (?, ?, ?)
                """,
                (livro_id, usuario_id, "emprestado")
            )
            
            # Atualiza a disponibilidade do livro
            cursor.execute(
                "UPDATE livros SET disponivel = disponivel - 1 WHERE id = ?",
                (livro_id,)
            )
            
            conn.commit()
            return True, "Empréstimo realizado com sucesso"
        except Exception as e:
            conn.rollback()
            return False, str(e)
        finally:
            conn.close()
            
    def devolver(self, emprestimo_id):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        try:
            # Busca informações do empréstimo
            cursor.execute(
                """
                SELECT livro_id, data_emprestimo 
                FROM emprestimos 
                WHERE id = ? AND status = 'emprestado'
                """,
                (emprestimo_id,)
            )
            emprestimo = cursor.fetchone()
            
            if not emprestimo:
                return False, "Empréstimo não encontrado"
                
            livro_id, data_emprestimo = emprestimo
            
            # Calcula multa se houver atraso
            data_devolucao = datetime.now()
            data_limite = datetime.strptime(data_emprestimo, "%Y-%m-%d %H:%M:%S") + timedelta(days=self.dias_emprestimo)
            
            multa = 0
            if data_devolucao > data_limite:
                dias_atraso = (data_devolucao - data_limite).days
                multa = dias_atraso * self.valor_multa_dia
            
            # Atualiza o empréstimo
            cursor.execute(
                """
                UPDATE emprestimos 
                SET status = ?, data_devolucao = ?, multa = ?
                WHERE id = ?
                """,
                ("devolvido", data_devolucao.strftime("%Y-%m-%d %H:%M:%S"), multa, emprestimo_id)
            )
            
            # Atualiza a disponibilidade do livro
            cursor.execute(
                "UPDATE livros SET disponivel = disponivel + 1 WHERE id = ?",
                (livro_id,)
            )
            
            conn.commit()
            return True, f"Devolução realizada com sucesso. Multa: R$ {multa:.2f}" if multa > 0 else "Devolução realizada com sucesso"
        except Exception as e:
            conn.rollback()
            return False, str(e)
        finally:
            conn.close()
            
    def listar_todos(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """
            SELECT e.*, l.titulo, u.nome
            FROM emprestimos e
            JOIN livros l ON e.livro_id = l.id
            JOIN usuarios u ON e.usuario_id = u.id
            ORDER BY e.data_emprestimo DESC
            """
        )
        emprestimos = cursor.fetchall()
        
        conn.close()
        return emprestimos
        
    def listar_ativos(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """
            SELECT e.*, l.titulo, u.nome
            FROM emprestimos e
            JOIN livros l ON e.livro_id = l.id
            JOIN usuarios u ON e.usuario_id = u.id
            WHERE e.status = 'emprestado'
            ORDER BY e.data_emprestimo DESC
            """
        )
        emprestimos = cursor.fetchall()
        
        conn.close()
        return emprestimos
        
    def buscar_por_usuario(self, usuario_id):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """
            SELECT e.*, l.titulo
            FROM emprestimos e
            JOIN livros l ON e.livro_id = l.id
            WHERE e.usuario_id = ?
            ORDER BY e.data_emprestimo DESC
            """,
            (usuario_id,)
        )
        emprestimos = cursor.fetchall()
        
        conn.close()
        return emprestimos
        
    def buscar_por_livro(self, livro_id):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """
            SELECT e.*, u.nome
            FROM emprestimos e
            JOIN usuarios u ON e.usuario_id = u.id
            WHERE e.livro_id = ?
            ORDER BY e.data_emprestimo DESC
            """,
            (livro_id,)
        )
        emprestimos = cursor.fetchall()
        
        conn.close()
        return emprestimos 