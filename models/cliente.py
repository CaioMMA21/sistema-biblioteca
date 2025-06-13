from database.database import Database

class Cliente:
    def __init__(self):
        self.db = Database()

    def adicionar(self, nome, numero, email):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO clientes (nome, numero, email) VALUES (?, ?, ?)",
                (nome, numero, email)
            )
            conn.commit()
            return True
        except Exception:
            return False
        finally:
            conn.close()

    def listar_todos(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clientes ORDER BY nome")
        clientes = cursor.fetchall()
        conn.close()
        return clientes

    def buscar(self, termo):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM clientes WHERE nome LIKE ? OR email LIKE ? ORDER BY nome",
            (f"%{termo}%", f"%{termo}%")
        )
        clientes = cursor.fetchall()
        conn.close()
        return clientes 