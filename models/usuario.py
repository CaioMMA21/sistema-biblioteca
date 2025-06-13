from database.database import Database
import bcrypt

class Usuario:
    def __init__(self):
        self.db = Database()
        
    def adicionar(self, nome, email, senha, tipo="bibliotecario"):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        # Hash da senha
        senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
        
        try:
            cursor.execute(
                """
                INSERT INTO usuarios (nome, email, senha, tipo)
                VALUES (?, ?, ?, ?)
                """,
                (nome, email, senha_hash.decode('utf-8'), tipo)
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
        
        cursor.execute("SELECT id, nome, email, tipo, data_criacao FROM usuarios ORDER BY nome")
        usuarios = cursor.fetchall()
        
        conn.close()
        return usuarios
        
    def buscar(self, termo):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """
            SELECT id, nome, email, tipo, data_criacao 
            FROM usuarios 
            WHERE nome LIKE ? OR email LIKE ?
            ORDER BY nome
            """,
            (f"%{termo}%", f"%{termo}%")
        )
        usuarios = cursor.fetchall()
        
        conn.close()
        return usuarios
        
    def atualizar(self, id, nome, email, tipo):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                """
                UPDATE usuarios 
                SET nome = ?, email = ?, tipo = ?
                WHERE id = ?
                """,
                (nome, email, tipo, id)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
            
    def atualizar_senha(self, id, nova_senha):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        # Hash da nova senha
        senha_hash = bcrypt.hashpw(nova_senha.encode('utf-8'), bcrypt.gensalt())
        
        cursor.execute(
            "UPDATE usuarios SET senha = ? WHERE id = ?",
            (senha_hash.decode('utf-8'), id)
        )
        conn.commit()
        
        conn.close()
        return True
        
    def excluir(self, id):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM usuarios WHERE id = ?", (id,))
        conn.commit()
        
        conn.close()
        return True
        
    def verificar_login(self, email, senha):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
        usuario = cursor.fetchone()
        
        conn.close()
        
        if usuario and bcrypt.checkpw(senha.encode('utf-8'), usuario[3].encode('utf-8')):
            return usuario
        return None 