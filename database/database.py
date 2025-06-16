import sqlite3
import os
from datetime import datetime
import bcrypt

class Database:
    def __init__(self):
        self.db_file = "database/biblioteca.db"
        self.create_tables()
        
    def get_connection(self):
        return sqlite3.connect(self.db_file)
        
    def create_tables(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Tabela de usuários
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL,
            tipo TEXT NOT NULL,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Tabela de livros
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS livros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            isbn TEXT UNIQUE,
            quantidade INTEGER NOT NULL,
            disponivel INTEGER NOT NULL,
            data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Tabela de clientes
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            numero TEXT NOT NULL,
            email TEXT NOT NULL
        )
        ''')
        
        # Tabela de empréstimos
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS emprestimos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER NOT NULL,
            livro_id INTEGER NOT NULL,
            data_emprestimo TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            data_devolucao_prevista TIMESTAMP NOT NULL,
            data_devolucao_real TIMESTAMP,
            status TEXT NOT NULL DEFAULT 'ativo',
            FOREIGN KEY (cliente_id) REFERENCES clientes (id),
            FOREIGN KEY (livro_id) REFERENCES livros (id)
        )
        ''')
        
        conn.commit()
        conn.close()
        
    def criar_usuario_admin(self, username, password):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Verifica se já existe um admin
        cursor.execute("SELECT * FROM usuarios WHERE tipo = 'admin'")
        if cursor.fetchone() is None:
            senha_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            cursor.execute(
                "INSERT INTO usuarios (nome, email, senha, tipo) VALUES (?, ?, ?, ?)",
                (username, f"{username}@admin.com", senha_hash.decode('utf-8'), "admin")
            )
            conn.commit()
        conn.close()
        
    def verificar_login(self, email, senha):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT * FROM usuarios WHERE email = ? AND senha = ?",
            (email, senha)
        )
        usuario = cursor.fetchone()
        
        conn.close()
        return usuario 