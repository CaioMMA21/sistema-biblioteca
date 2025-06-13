from database.database import Database

class Livro:
    def __init__(self):
        self.db = Database()
        
    def adicionar(self, titulo, autor, isbn, quantidade):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                """
                INSERT INTO livros (titulo, autor, isbn, quantidade, disponivel)
                VALUES (?, ?, ?, ?, ?)
                """,
                (titulo, autor, isbn, quantidade, quantidade)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
            
    def listar_todos(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM livros ORDER BY titulo")
        livros = cursor.fetchall()
        
        conn.close()
        return livros
        
    def buscar(self, termo):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """
            SELECT * FROM livros 
            WHERE titulo LIKE ? OR autor LIKE ? OR isbn LIKE ?
            ORDER BY titulo
            """,
            (f"%{termo}%", f"%{termo}%", f"%{termo}%")
        )
        livros = cursor.fetchall()
        
        conn.close()
        return livros
        
    def atualizar(self, id, titulo, autor, isbn, quantidade):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                """
                UPDATE livros 
                SET titulo = ?, autor = ?, isbn = ?, quantidade = ?
                WHERE id = ?
                """,
                (titulo, autor, isbn, quantidade, id)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
            
    def excluir(self, id):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM livros WHERE id = ?", (id,))
        conn.commit()
        
        conn.close()
        return True
        
    def verificar_disponibilidade(self, id):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT disponivel FROM livros WHERE id = ?", (id,))
        resultado = cursor.fetchone()
        
        conn.close()
        return resultado[0] > 0 if resultado else False
        
    def atualizar_disponibilidade(self, id, quantidade):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "UPDATE livros SET disponivel = disponivel + ? WHERE id = ?",
            (quantidade, id)
        )
        conn.commit()
        
        conn.close()
        return True 