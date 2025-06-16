import customtkinter as ctk
from tkinter import messagebox
import os
from dotenv import load_dotenv
from database.database import Database

class SistemaBiblioteca:
    def __init__(self):
        self.janela = ctk.CTk()
        self.janela.title("Sistema de Gerenciamento de Biblioteca")
        self.janela.state('zoomed')
        self.janela.attributes('-fullscreen', True)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        load_dotenv()
        self.db = Database()
        self.db.criar_usuario_admin(
            os.getenv("ADMIN_USERNAME", "admin"),
            os.getenv("ADMIN_PASSWORD", "admin123")
        )
        self.criar_interface_login()

    def criar_interface_login(self):
        self.frame_login = ctk.CTkFrame(self.janela)
        self.frame_login.pack(pady=20, padx=20, fill="both", expand=True)
        titulo = ctk.CTkLabel(
            self.frame_login,
            text="Sistema de Gerenciamento de Biblioteca",
            font=("Arial", 24, "bold")
        )
        titulo.pack(pady=20)
        frame_campos = ctk.CTkFrame(self.frame_login)
        frame_campos.pack(pady=20, padx=40, fill="x")
        label_email = ctk.CTkLabel(frame_campos, text="Email:")
        label_email.pack(anchor="w", pady=(10, 0))
        self.entrada_email = ctk.CTkEntry(frame_campos, placeholder_text="Digite seu email")
        self.entrada_email.pack(fill="x", pady=(0, 10))
        label_senha = ctk.CTkLabel(frame_campos, text="Senha:")
        label_senha.pack(anchor="w", pady=(10, 0))
        self.entrada_senha = ctk.CTkEntry(frame_campos, placeholder_text="Digite sua senha", show="*")
        self.entrada_senha.pack(fill="x", pady=(0, 10))
        botao_login = ctk.CTkButton(
            frame_campos,
            text="Entrar",
            command=self.fazer_login
        )
        botao_login.pack(pady=20)

    def fazer_login(self):
        from models.usuario import Usuario
        email = self.entrada_email.get().strip()
        senha = self.entrada_senha.get().strip()
        if not email or not senha:
            messagebox.showwarning("Aviso", "Por favor, preencha todos os campos!")
            return
        usuario_model = Usuario()
        usuario = usuario_model.verificar_login(email, senha)
        if usuario:
            self.frame_login.destroy()
            self.criar_interface_principal(usuario)
        else:
            messagebox.showerror("Erro", "Email ou senha inválidos!")

    def criar_interface_principal(self, usuario):
        self.frame_principal = ctk.CTkFrame(self.janela)
        self.frame_principal.pack(fill="both", expand=True)
        frame_superior = ctk.CTkFrame(self.frame_principal)
        frame_superior.pack(fill="x", padx=20, pady=10)
        label_usuario = ctk.CTkLabel(
            frame_superior,
            text=f"Bem-vindo, {usuario[1]}!",
            font=("Arial", 16)
        )
        label_usuario.pack(side="left", padx=10)
        botao_logout = ctk.CTkButton(
            frame_superior,
            text="Sair",
            command=self.fazer_logout
        )
        botao_logout.pack(side="right", padx=10)
        frame_menu = ctk.CTkFrame(self.frame_principal, width=200)
        frame_menu.pack(side="left", fill="y", padx=20, pady=20)
        botoes_menu = [
            ("Livros", self.mostrar_livros),
            ("Usuários", self.mostrar_usuarios),
            ("Clientes", self.mostrar_clientes),
            ("Aluguel", self.mostrar_emprestimos),
            ("Busca Avançada", self.mostrar_busca_avancada),
            ("Multas", self.mostrar_multas),
            ("Relatórios", self.mostrar_relatorios),
            ("Cadastro", self.mostrar_cadastro)
        ]
        for texto, comando in botoes_menu:
            botao = ctk.CTkButton(
                frame_menu,
                text=texto,
                command=comando,
                width=180
            )
            botao.pack(pady=5, padx=10)
        self.frame_conteudo = ctk.CTkFrame(self.frame_principal)
        self.frame_conteudo.pack(side="right", fill="both", expand=True, padx=20, pady=20)
        self.mostrar_livros()

    def mostrar_livros(self):
        self.limpar_conteudo()
        label = ctk.CTkLabel(self.frame_conteudo, text="Livros Cadastrados", font=("Arial", 18, "bold"))
        label.pack(pady=20)

        from models.livro import Livro
        livro_model = Livro()
        livros = livro_model.listar_todos()

        # Cabeçalho
        frame_lista = ctk.CTkFrame(self.frame_conteudo)
        frame_lista.pack(padx=20, pady=10, fill="x")
        header = ["Título", "Autor", "ISBN", "Alugado?"]
        for i, h in enumerate(header):
            ctk.CTkLabel(frame_lista, text=h, font=("Arial", 12, "bold")).grid(row=0, column=i, padx=10, pady=5)

        # Linhas dos livros
        for idx, livro in enumerate(livros):
            titulo, autor, isbn, quantidade, disponivel = livro[1], livro[2], livro[3], livro[4], livro[5]
            alugado = "Sim" if disponivel < quantidade else "Não"
            ctk.CTkLabel(frame_lista, text=titulo).grid(row=idx+1, column=0, padx=10, pady=2)
            ctk.CTkLabel(frame_lista, text=autor).grid(row=idx+1, column=1, padx=10, pady=2)
            ctk.CTkLabel(frame_lista, text=isbn).grid(row=idx+1, column=2, padx=10, pady=2)
            ctk.CTkLabel(frame_lista, text=alugado).grid(row=idx+1, column=3, padx=10, pady=2)

    def mostrar_usuarios(self):
        self.limpar_conteudo()
        label = ctk.CTkLabel(self.frame_conteudo, text="Usuários Cadastrados", font=("Arial", 18, "bold"))
        label.pack(pady=20)

        from models.usuario import Usuario
        usuario_model = Usuario()
        usuarios = usuario_model.listar_todos()

        frame_lista = ctk.CTkFrame(self.frame_conteudo)
        frame_lista.pack(padx=20, pady=10, fill="x")
        header = ["Nome", "Email", "Tipo", "Data de Criação"]
        for i, h in enumerate(header):
            ctk.CTkLabel(frame_lista, text=h, font=("Arial", 12, "bold")).grid(row=0, column=i, padx=10, pady=5)
        for idx, usuario in enumerate(usuarios):
            nome, email, tipo, data_criacao = usuario[1], usuario[2], usuario[3], usuario[4]
            ctk.CTkLabel(frame_lista, text=nome).grid(row=idx+1, column=0, padx=10, pady=2)
            ctk.CTkLabel(frame_lista, text=email).grid(row=idx+1, column=1, padx=10, pady=2)
            ctk.CTkLabel(frame_lista, text=tipo).grid(row=idx+1, column=2, padx=10, pady=2)
            ctk.CTkLabel(frame_lista, text=data_criacao).grid(row=idx+1, column=3, padx=10, pady=2)

    def mostrar_emprestimos(self):
        self.limpar_conteudo()
        label = ctk.CTkLabel(self.frame_conteudo, text="Gerenciamento de Empréstimos", font=("Arial", 18, "bold"))
        label.pack(pady=20)

        # Frame principal para o formulário
        frame_principal = ctk.CTkFrame(self.frame_conteudo)
        frame_principal.pack(pady=10, padx=20, fill="both", expand=True)

        # Frame do formulário
        frame_formulario = ctk.CTkFrame(frame_principal)
        frame_formulario.pack(pady=20, padx=20, fill="both", expand=True)

        # Título do formulário
        label_titulo = ctk.CTkLabel(frame_formulario, text="Novo Empréstimo", font=("Arial", 14, "bold"))
        label_titulo.pack(pady=10)

        # Frame para os campos
        frame_campos = ctk.CTkFrame(frame_formulario)
        frame_campos.pack(pady=10, padx=20, fill="x")

        # Campos do cliente
        label_cliente = ctk.CTkLabel(frame_campos, text="Dados do Cliente", font=("Arial", 12, "bold"))
        label_cliente.grid(row=0, column=0, columnspan=2, pady=10, sticky="w")

        label_nome = ctk.CTkLabel(frame_campos, text="Nome do Cliente:")
        label_nome.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entrada_nome_emprestimo = ctk.CTkEntry(frame_campos, width=250)
        self.entrada_nome_emprestimo.grid(row=1, column=1, padx=5, pady=5)

        label_numero = ctk.CTkLabel(frame_campos, text="Número:")
        label_numero.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entrada_numero_emprestimo = ctk.CTkEntry(frame_campos, width=250)
        self.entrada_numero_emprestimo.grid(row=2, column=1, padx=5, pady=5)

        label_email = ctk.CTkLabel(frame_campos, text="Email:")
        label_email.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.entrada_email_emprestimo = ctk.CTkEntry(frame_campos, width=250)
        self.entrada_email_emprestimo.grid(row=3, column=1, padx=5, pady=5)

        # Campos do livro
        label_livro = ctk.CTkLabel(frame_campos, text="Dados do Livro", font=("Arial", 12, "bold"))
        label_livro.grid(row=4, column=0, columnspan=2, pady=10, sticky="w")

        label_titulo_livro = ctk.CTkLabel(frame_campos, text="Título do Livro:")
        label_titulo_livro.grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.entrada_titulo_emprestimo = ctk.CTkEntry(frame_campos, width=250)
        self.entrada_titulo_emprestimo.grid(row=5, column=1, padx=5, pady=5)

        # Campo para quantidade de dias
        label_dias = ctk.CTkLabel(frame_campos, text="Quantidade de Dias:")
        label_dias.grid(row=6, column=0, padx=5, pady=5, sticky="w")
        self.entrada_dias_emprestimo = ctk.CTkEntry(frame_campos, width=100)
        self.entrada_dias_emprestimo.grid(row=6, column=1, padx=5, pady=5, sticky="w")

        # Botão de busca de cliente
        botao_buscar_cliente = ctk.CTkButton(
            frame_campos,
            text="Buscar Cliente",
            command=self.buscar_cliente_emprestimo,
            width=120
        )
        botao_buscar_cliente.grid(row=7, column=0, padx=5, pady=10)

        # Botão de busca de livro
        botao_buscar_livro = ctk.CTkButton(
            frame_campos,
            text="Buscar Livro",
            command=self.buscar_livro_emprestimo,
            width=120
        )
        botao_buscar_livro.grid(row=7, column=1, padx=5, pady=10)

        # Botão de confirmar empréstimo
        botao_confirmar = ctk.CTkButton(
            frame_formulario,
            text="Confirmar Empréstimo",
            command=self.confirmar_emprestimo,
            width=200
        )
        botao_confirmar.pack(pady=20)

    def buscar_cliente_emprestimo(self):
        nome = self.entrada_nome_emprestimo.get().strip()
        if not nome:
            messagebox.showwarning("Aviso", "Digite o nome do cliente para buscar!")
            return

        from models.cliente import Cliente
        cliente_model = Cliente()
        clientes = cliente_model.buscar(nome)

        if not clientes:
            messagebox.showinfo("Informação", "Cliente não encontrado!")
            return

        # Se encontrou mais de um cliente, mostra uma lista para selecionar
        if len(clientes) > 1:
            # Criar uma janela de seleção
            janela_selecao = ctk.CTkToplevel(self.janela)
            janela_selecao.title("Selecionar Cliente")
            janela_selecao.geometry("400x300")

            label = ctk.CTkLabel(janela_selecao, text="Selecione o cliente:")
            label.pack(pady=10)

            frame_lista = ctk.CTkFrame(janela_selecao)
            frame_lista.pack(pady=10, padx=20, fill="both", expand=True)

            for cliente in clientes:
                frame_cliente = ctk.CTkFrame(frame_lista)
                frame_cliente.pack(fill="x", pady=2)
                
                texto = f"{cliente[1]} - {cliente[2]} - {cliente[3]}"
                botao = ctk.CTkButton(
                    frame_cliente,
                    text=texto,
                    command=lambda c=cliente: self.selecionar_cliente(c, janela_selecao)
                )
                botao.pack(fill="x", padx=5, pady=2)
        else:
            # Se encontrou apenas um cliente, seleciona automaticamente
            self.selecionar_cliente(clientes[0])

    def selecionar_cliente(self, cliente, janela_selecao=None):
        self.entrada_nome_emprestimo.delete(0, "end")
        self.entrada_numero_emprestimo.delete(0, "end")
        self.entrada_email_emprestimo.delete(0, "end")

        self.entrada_nome_emprestimo.insert(0, cliente[1])
        self.entrada_numero_emprestimo.insert(0, cliente[2])
        self.entrada_email_emprestimo.insert(0, cliente[3])

        if janela_selecao:
            janela_selecao.destroy()

    def buscar_livro_emprestimo(self):
        titulo = self.entrada_titulo_emprestimo.get().strip()
        if not titulo:
            messagebox.showwarning("Aviso", "Digite o título do livro para buscar!")
            return

        from models.livro import Livro
        livro_model = Livro()
        livros = livro_model.buscar(titulo)

        if not livros:
            messagebox.showinfo("Informação", "Livro não encontrado!")
            return

        # Se encontrou mais de um livro, mostra uma lista para selecionar
        if len(livros) > 1:
            # Criar uma janela de seleção
            janela_selecao = ctk.CTkToplevel(self.janela)
            janela_selecao.title("Selecionar Livro")
            janela_selecao.geometry("400x300")

            label = ctk.CTkLabel(janela_selecao, text="Selecione o livro:")
            label.pack(pady=10)

            frame_lista = ctk.CTkFrame(janela_selecao)
            frame_lista.pack(pady=10, padx=20, fill="both", expand=True)

            for livro in livros:
                frame_livro = ctk.CTkFrame(frame_lista)
                frame_livro.pack(fill="x", pady=2)
                
                texto = f"{livro[1]} - {livro[2]} - Disponível: {livro[5]}"
                botao = ctk.CTkButton(
                    frame_livro,
                    text=texto,
                    command=lambda l=livro: self.selecionar_livro(l, janela_selecao)
                )
                botao.pack(fill="x", padx=5, pady=2)
        else:
            # Se encontrou apenas um livro, seleciona automaticamente
            self.selecionar_livro(livros[0])

    def selecionar_livro(self, livro, janela_selecao=None):
        self.entrada_titulo_emprestimo.delete(0, "end")
        self.entrada_titulo_emprestimo.insert(0, livro[1])

        if janela_selecao:
            janela_selecao.destroy()

    def confirmar_emprestimo(self):
        nome = self.entrada_nome_emprestimo.get().strip()
        numero = self.entrada_numero_emprestimo.get().strip()
        email = self.entrada_email_emprestimo.get().strip()
        titulo = self.entrada_titulo_emprestimo.get().strip()
        dias = self.entrada_dias_emprestimo.get().strip()

        if not all([nome, numero, email, titulo, dias]):
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return

        try:
            dias = int(dias)
            if dias <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Aviso", "A quantidade de dias deve ser um número positivo!")
            return

        # Busca o cliente
        from models.cliente import Cliente
        cliente_model = Cliente()
        clientes = cliente_model.buscar(nome)
        
        if not clientes:
            messagebox.showerror("Erro", "Cliente não encontrado!")
            return
            
        cliente_id = clientes[0][0]  # Pega o ID do primeiro cliente encontrado

        # Busca o livro
        from models.livro import Livro
        livro_model = Livro()
        livros = livro_model.buscar(titulo)
        
        if not livros:
            messagebox.showerror("Erro", "Livro não encontrado!")
            return
            
        livro_id = livros[0][0]  # Pega o ID do primeiro livro encontrado

        # Registra o empréstimo
        from models.emprestimo import Emprestimo
        emprestimo_model = Emprestimo()
        sucesso, mensagem = emprestimo_model.adicionar(cliente_id, livro_id, dias)
        
        if sucesso:
            messagebox.showinfo("Sucesso", mensagem)
            # Limpar os campos após o registro
            self.entrada_nome_emprestimo.delete(0, "end")
            self.entrada_numero_emprestimo.delete(0, "end")
            self.entrada_email_emprestimo.delete(0, "end")
            self.entrada_titulo_emprestimo.delete(0, "end")
            self.entrada_dias_emprestimo.delete(0, "end")
        else:
            messagebox.showerror("Erro", mensagem)

    def mostrar_relatorios(self):
        self.limpar_conteudo()
        label = ctk.CTkLabel(self.frame_conteudo, text="Relatórios e Estatísticas", font=("Arial", 18, "bold"))
        label.pack(pady=20)

        import sqlite3
        from datetime import datetime
        conn = sqlite3.connect("database/biblioteca.db")
        cursor = conn.cursor()

        # 1. Empréstimos ativos
        frame_ativos = ctk.CTkFrame(self.frame_conteudo)
        frame_ativos.pack(padx=10, pady=10, fill="x")
        ctk.CTkLabel(frame_ativos, text="Empréstimos Ativos", font=("Arial", 14, "bold")).pack(anchor="w", pady=5)
        cursor.execute('''
            SELECT c.nome, c.email, c.numero, l.titulo, l.autor, l.isbn, e.data_emprestimo, e.data_devolucao_prevista
            FROM emprestimos e
            JOIN clientes c ON e.cliente_id = c.id
            JOIN livros l ON e.livro_id = l.id
            WHERE e.status = 'ativo'
            ORDER BY e.data_emprestimo DESC
        ''')
        header = ["Cliente", "Email", "Tel", "Livro", "Autor", "ISBN", "Empréstimo", "Prev. Devolução", "Dias Restantes"]
        for i, h in enumerate(header):
            ctk.CTkLabel(frame_ativos, text=h, font=("Arial", 10, "bold")).grid(row=1, column=i, padx=5, pady=2)
        for idx, row in enumerate(cursor.fetchall()):
            nome, email, numero, titulo, autor, isbn, data_emp, data_prev = row
            try:
                dias_restantes = (datetime.strptime(data_prev, "%Y-%m-%d %H:%M:%S") - datetime.now()).days
            except:
                dias_restantes = "-"
            for col, val in enumerate([nome, email, numero, titulo, autor, isbn, data_emp, data_prev, dias_restantes]):
                ctk.CTkLabel(frame_ativos, text=str(val)).grid(row=idx+2, column=col, padx=5, pady=2)

        # 2. Livros mais emprestados
        frame_livros = ctk.CTkFrame(self.frame_conteudo)
        frame_livros.pack(padx=10, pady=10, fill="x")
        ctk.CTkLabel(frame_livros, text="Livros Mais Emprestados", font=("Arial", 14, "bold")).pack(anchor="w", pady=5)
        cursor.execute('''
            SELECT l.titulo, l.autor, COUNT(e.id) as total
            FROM livros l
            LEFT JOIN emprestimos e ON l.id = e.livro_id
            GROUP BY l.id
            ORDER BY total DESC
            LIMIT 10
        ''')
        ctk.CTkLabel(frame_livros, text="Título", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5)
        ctk.CTkLabel(frame_livros, text="Autor", font=("Arial", 10, "bold")).grid(row=0, column=1, padx=5)
        ctk.CTkLabel(frame_livros, text="Empréstimos", font=("Arial", 10, "bold")).grid(row=0, column=2, padx=5)
        for idx, (titulo, autor, total) in enumerate(cursor.fetchall()):
            ctk.CTkLabel(frame_livros, text=titulo).grid(row=idx+1, column=0, padx=5)
            ctk.CTkLabel(frame_livros, text=autor).grid(row=idx+1, column=1, padx=5)
            ctk.CTkLabel(frame_livros, text=total).grid(row=idx+1, column=2, padx=5)

        # 3. Clientes com mais empréstimos
        frame_clientes = ctk.CTkFrame(self.frame_conteudo)
        frame_clientes.pack(padx=10, pady=10, fill="x")
        ctk.CTkLabel(frame_clientes, text="Clientes com Mais Empréstimos", font=("Arial", 14, "bold")).pack(anchor="w", pady=5)
        cursor.execute('''
            SELECT c.nome, c.email, COUNT(e.id) as total
            FROM clientes c
            LEFT JOIN emprestimos e ON c.id = e.cliente_id
            GROUP BY c.id
            ORDER BY total DESC
            LIMIT 10
        ''')
        ctk.CTkLabel(frame_clientes, text="Nome", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5)
        ctk.CTkLabel(frame_clientes, text="Email", font=("Arial", 10, "bold")).grid(row=0, column=1, padx=5)
        ctk.CTkLabel(frame_clientes, text="Empréstimos", font=("Arial", 10, "bold")).grid(row=0, column=2, padx=5)
        for idx, (nome, email, total) in enumerate(cursor.fetchall()):
            ctk.CTkLabel(frame_clientes, text=nome).grid(row=idx+1, column=0, padx=5)
            ctk.CTkLabel(frame_clientes, text=email).grid(row=idx+1, column=1, padx=5)
            ctk.CTkLabel(frame_clientes, text=total).grid(row=idx+1, column=2, padx=5)

        # 4. Multas em aberto (fictício)
        frame_multas = ctk.CTkFrame(self.frame_conteudo)
        frame_multas.pack(padx=10, pady=10, fill="x")
        ctk.CTkLabel(frame_multas, text="Multas em Aberto (Fictício)", font=("Arial", 14, "bold")).pack(anchor="w", pady=5)
        cursor.execute('''
            SELECT c.nome, l.titulo, e.data_devolucao_prevista, e.data_emprestimo
            FROM emprestimos e
            JOIN clientes c ON e.cliente_id = c.id
            JOIN livros l ON e.livro_id = l.id
            WHERE e.status = 'ativo'
        ''')
        ctk.CTkLabel(frame_multas, text="Cliente", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5)
        ctk.CTkLabel(frame_multas, text="Livro", font=("Arial", 10, "bold")).grid(row=0, column=1, padx=5)
        ctk.CTkLabel(frame_multas, text="Dias de atraso", font=("Arial", 10, "bold")).grid(row=0, column=2, padx=5)
        ctk.CTkLabel(frame_multas, text="Multa (R$)", font=("Arial", 10, "bold")).grid(row=0, column=3, padx=5)
        row_idx = 1
        for nome, titulo, data_prev, data_emp in cursor.fetchall():
            if data_prev:
                try:
                    dias_atraso = (datetime.now() - datetime.strptime(data_prev, "%Y-%m-%d %H:%M:%S")).days
                except:
                    dias_atraso = 0
                if dias_atraso > 0:
                    valor_multa = dias_atraso * 2.0
                    ctk.CTkLabel(frame_multas, text=nome).grid(row=row_idx, column=0, padx=5)
                    ctk.CTkLabel(frame_multas, text=titulo).grid(row=row_idx, column=1, padx=5)
                    ctk.CTkLabel(frame_multas, text=dias_atraso).grid(row=row_idx, column=2, padx=5)
                    ctk.CTkLabel(frame_multas, text=f"R$ {valor_multa:.2f}").grid(row=row_idx, column=3, padx=5)
                    row_idx += 1

        # 5. Livros em atraso
        frame_atraso = ctk.CTkFrame(self.frame_conteudo)
        frame_atraso.pack(padx=10, pady=10, fill="x")
        ctk.CTkLabel(frame_atraso, text="Livros em Atraso", font=("Arial", 14, "bold")).pack(anchor="w", pady=5)
        cursor.execute('''
            SELECT c.nome, l.titulo, e.data_devolucao_prevista
            FROM emprestimos e
            JOIN clientes c ON e.cliente_id = c.id
            JOIN livros l ON e.livro_id = l.id
            WHERE e.status = 'ativo'
        ''')
        ctk.CTkLabel(frame_atraso, text="Cliente", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5)
        ctk.CTkLabel(frame_atraso, text="Livro", font=("Arial", 10, "bold")).grid(row=0, column=1, padx=5)
        ctk.CTkLabel(frame_atraso, text="Dias de atraso", font=("Arial", 10, "bold")).grid(row=0, column=2, padx=5)
        row_idx = 1
        for nome, titulo, data_prev in cursor.fetchall():
            if data_prev:
                try:
                    dias_atraso = (datetime.now() - datetime.strptime(data_prev, "%Y-%m-%d %H:%M:%S")).days
                except:
                    dias_atraso = 0
                if dias_atraso > 0:
                    ctk.CTkLabel(frame_atraso, text=nome).grid(row=row_idx, column=0, padx=5)
                    ctk.CTkLabel(frame_atraso, text=titulo).grid(row=row_idx, column=1, padx=5)
                    ctk.CTkLabel(frame_atraso, text=dias_atraso).grid(row=row_idx, column=2, padx=5)
                    row_idx += 1

        conn.close()

    def mostrar_clientes(self):
        self.limpar_conteudo()
        label = ctk.CTkLabel(self.frame_conteudo, text="Clientes Cadastrados", font=("Arial", 18, "bold"))
        label.pack(pady=20)

        from models.cliente import Cliente
        cliente_model = Cliente()
        clientes = cliente_model.listar_todos()

        frame_lista = ctk.CTkFrame(self.frame_conteudo)
        frame_lista.pack(padx=20, pady=10, fill="x")
        header = ["Nome", "Número", "Email"]
        for i, h in enumerate(header):
            ctk.CTkLabel(frame_lista, text=h, font=("Arial", 12, "bold")).grid(row=0, column=i, padx=10, pady=5)
        for idx, cliente in enumerate(clientes):
            nome, numero, email = cliente[1], cliente[2], cliente[3]
            ctk.CTkLabel(frame_lista, text=nome).grid(row=idx+1, column=0, padx=10, pady=2)
            ctk.CTkLabel(frame_lista, text=numero).grid(row=idx+1, column=1, padx=10, pady=2)
            ctk.CTkLabel(frame_lista, text=email).grid(row=idx+1, column=2, padx=10, pady=2)

    def mostrar_cadastro(self):
        self.limpar_conteudo()
        label = ctk.CTkLabel(self.frame_conteudo, text="Painel de Cadastro", font=("Arial", 18, "bold"))
        label.pack(pady=20)

        # Frame principal centralizado
        frame_principal = ctk.CTkFrame(self.frame_conteudo)
        frame_principal.pack(pady=10, padx=20, fill="both", expand=True)

        # Container para os formulários
        frame_formularios = ctk.CTkFrame(frame_principal)
        frame_formularios.pack(pady=20, padx=20, fill="both", expand=True)

        # Formulário de cadastro de usuário
        frame_usuario = ctk.CTkFrame(frame_formularios)
        frame_usuario.pack(side="left", padx=20, pady=10, fill="both", expand=True)
        label_usuario = ctk.CTkLabel(frame_usuario, text="Cadastro de Usuário", font=("Arial", 14, "bold"))
        label_usuario.pack(pady=10)
        label_nome = ctk.CTkLabel(frame_usuario, text="Nome:")
        label_nome.pack(anchor="w", padx=20)
        self.entrada_nome_cadastro = ctk.CTkEntry(frame_usuario, width=250)
        self.entrada_nome_cadastro.pack(pady=2, padx=20)
        label_email = ctk.CTkLabel(frame_usuario, text="Email:")
        label_email.pack(anchor="w", padx=20)
        self.entrada_email_cadastro = ctk.CTkEntry(frame_usuario, width=250)
        self.entrada_email_cadastro.pack(pady=2, padx=20)
        label_senha = ctk.CTkLabel(frame_usuario, text="Senha:")
        label_senha.pack(anchor="w", padx=20)
        self.entrada_senha_cadastro = ctk.CTkEntry(frame_usuario, show="*", width=250)
        self.entrada_senha_cadastro.pack(pady=2, padx=20)
        botao_cadastrar_usuario = ctk.CTkButton(frame_usuario, text="Cadastrar Usuário", command=self.cadastrar_usuario)
        botao_cadastrar_usuario.pack(pady=10, padx=20)

        # Formulário de cadastro de livro
        frame_livro = ctk.CTkFrame(frame_formularios)
        frame_livro.pack(side="left", padx=20, pady=10, fill="both", expand=True)
        label_livro = ctk.CTkLabel(frame_livro, text="Cadastro de Livro", font=("Arial", 14, "bold"))
        label_livro.pack(pady=10)
        label_titulo = ctk.CTkLabel(frame_livro, text="Título:")
        label_titulo.pack(anchor="w", padx=20)
        self.entrada_titulo_livro = ctk.CTkEntry(frame_livro, width=250)
        self.entrada_titulo_livro.pack(pady=2, padx=20)
        label_autor = ctk.CTkLabel(frame_livro, text="Autor:")
        label_autor.pack(anchor="w", padx=20)
        self.entrada_autor_livro = ctk.CTkEntry(frame_livro, width=250)
        self.entrada_autor_livro.pack(pady=2, padx=20)
        label_isbn = ctk.CTkLabel(frame_livro, text="ISBN:")
        label_isbn.pack(anchor="w", padx=20)
        self.entrada_isbn_livro = ctk.CTkEntry(frame_livro, width=250)
        self.entrada_isbn_livro.pack(pady=2, padx=20)
        label_quantidade = ctk.CTkLabel(frame_livro, text="Quantidade:")
        label_quantidade.pack(anchor="w", padx=20)
        self.entrada_quantidade_livro = ctk.CTkEntry(frame_livro, width=100)
        self.entrada_quantidade_livro.pack(pady=2, padx=20)
        botao_cadastrar_livro = ctk.CTkButton(frame_livro, text="Cadastrar Livro", command=self.cadastrar_livro)
        botao_cadastrar_livro.pack(pady=10, padx=20)

        # Formulário de cadastro de cliente
        frame_cliente = ctk.CTkFrame(frame_formularios)
        frame_cliente.pack(side="left", padx=20, pady=10, fill="both", expand=True)
        label_cliente = ctk.CTkLabel(frame_cliente, text="Cadastro de Cliente", font=("Arial", 14, "bold"))
        label_cliente.pack(pady=10)
        label_nome_cli = ctk.CTkLabel(frame_cliente, text="Nome:")
        label_nome_cli.pack(anchor="w", padx=20)
        self.entrada_nome_cliente = ctk.CTkEntry(frame_cliente, width=250)
        self.entrada_nome_cliente.pack(pady=2, padx=20)
        label_numero_cli = ctk.CTkLabel(frame_cliente, text="Número:")
        label_numero_cli.pack(anchor="w", padx=20)
        self.entrada_numero_cliente = ctk.CTkEntry(frame_cliente, width=250)
        self.entrada_numero_cliente.pack(pady=2, padx=20)
        label_email_cli = ctk.CTkLabel(frame_cliente, text="Email:")
        label_email_cli.pack(anchor="w", padx=20)
        self.entrada_email_cliente = ctk.CTkEntry(frame_cliente, width=250)
        self.entrada_email_cliente.pack(pady=2, padx=20)
        botao_cadastrar_cliente = ctk.CTkButton(frame_cliente, text="Cadastrar Cliente", command=self.cadastrar_cliente)
        botao_cadastrar_cliente.pack(pady=10, padx=20)

    def cadastrar_usuario(self):
        from models.usuario import Usuario
        nome = self.entrada_nome_cadastro.get().strip()
        email = self.entrada_email_cadastro.get().strip()
        senha = self.entrada_senha_cadastro.get().strip()

        if not nome or not email or not senha:
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return

        usuario_model = Usuario()
        sucesso = usuario_model.adicionar(nome, email, senha)
        if sucesso:
            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
            self.entrada_nome_cadastro.delete(0, "end")
            self.entrada_email_cadastro.delete(0, "end")
            self.entrada_senha_cadastro.delete(0, "end")
        else:
            messagebox.showerror("Erro", "Erro ao cadastrar usuário. Email já cadastrado.")
        
    def limpar_conteudo(self):
        for widget in self.frame_conteudo.winfo_children():
            widget.destroy()
            
    def fazer_logout(self):
        self.frame_principal.destroy()
        self.criar_interface_login()
        
    def cadastrar_livro(self):
        from models.livro import Livro
        titulo = self.entrada_titulo_livro.get().strip()
        autor = self.entrada_autor_livro.get().strip()
        isbn = self.entrada_isbn_livro.get().strip()
        quantidade = self.entrada_quantidade_livro.get().strip()

        if not titulo or not autor or not quantidade:
            messagebox.showwarning("Aviso", "Preencha todos os campos obrigatórios!")
            return
        try:
            quantidade = int(quantidade)
        except ValueError:
            messagebox.showwarning("Aviso", "Quantidade deve ser um número inteiro!")
            return

        livro_model = Livro()
        sucesso = livro_model.adicionar(titulo, autor, isbn, quantidade)
        if sucesso:
            messagebox.showinfo("Sucesso", "Livro cadastrado com sucesso!")
            self.entrada_titulo_livro.delete(0, "end")
            self.entrada_autor_livro.delete(0, "end")
            self.entrada_isbn_livro.delete(0, "end")
            self.entrada_quantidade_livro.delete(0, "end")
        else:
            messagebox.showerror("Erro", "Erro ao cadastrar livro. ISBN já cadastrado.")
        
    def cadastrar_cliente(self):
        from models.cliente import Cliente
        nome = self.entrada_nome_cliente.get().strip()
        numero = self.entrada_numero_cliente.get().strip()
        email = self.entrada_email_cliente.get().strip()
        if not nome or not numero or not email:
            messagebox.showwarning("Aviso", "Preencha todos os campos do cliente!")
            return
        cliente_model = Cliente()
        sucesso = cliente_model.adicionar(nome, numero, email)
        if sucesso:
            messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")
            self.entrada_nome_cliente.delete(0, "end")
            self.entrada_numero_cliente.delete(0, "end")
            self.entrada_email_cliente.delete(0, "end")
        else:
            messagebox.showerror("Erro", "Erro ao cadastrar cliente.")
        
    def mostrar_busca_avancada(self):
        self.limpar_conteudo()
        label = ctk.CTkLabel(self.frame_conteudo, text="Busca Avançada", font=("Arial", 18, "bold"))
        label.pack(pady=20)

        frame_busca = ctk.CTkFrame(self.frame_conteudo)
        frame_busca.pack(pady=10, padx=20)

        label_campo = ctk.CTkLabel(frame_busca, text="Buscar por título, autor ou ISBN:")
        label_campo.grid(row=0, column=0, padx=5)
        self.entrada_busca = ctk.CTkEntry(frame_busca, width=250)
        self.entrada_busca.grid(row=0, column=1, padx=5)
        botao_buscar = ctk.CTkButton(frame_busca, text="Buscar", command=self.executar_busca_avancada)
        botao_buscar.grid(row=0, column=2, padx=5)

        self.frame_resultado_busca = ctk.CTkFrame(self.frame_conteudo)
        self.frame_resultado_busca.pack(padx=20, pady=10, fill="x")

    def executar_busca_avancada(self):
        from models.livro import Livro
        termo = self.entrada_busca.get().strip()
        livro_model = Livro()
        resultados = livro_model.buscar(termo)

        for widget in self.frame_resultado_busca.winfo_children():
            widget.destroy()

        header = ["Título", "Autor", "ISBN", "Quantidade", "Disponível"]
        for i, h in enumerate(header):
            ctk.CTkLabel(self.frame_resultado_busca, text=h, font=("Arial", 12, "bold")).grid(row=0, column=i, padx=10, pady=5)
        for idx, livro in enumerate(resultados):
            ctk.CTkLabel(self.frame_resultado_busca, text=livro[1]).grid(row=idx+1, column=0, padx=10, pady=2)
            ctk.CTkLabel(self.frame_resultado_busca, text=livro[2]).grid(row=idx+1, column=1, padx=10, pady=2)
            ctk.CTkLabel(self.frame_resultado_busca, text=livro[3]).grid(row=idx+1, column=2, padx=10, pady=2)
            ctk.CTkLabel(self.frame_resultado_busca, text=livro[4]).grid(row=idx+1, column=3, padx=10, pady=2)
            ctk.CTkLabel(self.frame_resultado_busca, text=livro[5]).grid(row=idx+1, column=4, padx=10, pady=2)

    def mostrar_multas(self):
        self.limpar_conteudo()
        label = ctk.CTkLabel(self.frame_conteudo, text="Geração de Multas por Atraso", font=("Arial", 18, "bold"))
        label.pack(pady=20)

        from models.cliente import Cliente
        import random
        cliente_model = Cliente()
        clientes = cliente_model.listar_todos()

        frame_lista = ctk.CTkFrame(self.frame_conteudo)
        frame_lista.pack(padx=20, pady=10, fill="x")
        header = ["Nome", "Número", "Email", "Multa (R$)"]
        for i, h in enumerate(header):
            ctk.CTkLabel(frame_lista, text=h, font=("Arial", 12, "bold")).grid(row=0, column=i, padx=10, pady=5)
        for idx, cliente in enumerate(clientes):
            nome, numero, email = cliente[1], cliente[2], cliente[3]
            multa = round(random.uniform(0, 50), 2)  # valor fictício
            ctk.CTkLabel(frame_lista, text=nome).grid(row=idx+1, column=0, padx=10, pady=2)
            ctk.CTkLabel(frame_lista, text=numero).grid(row=idx+1, column=1, padx=10, pady=2)
            ctk.CTkLabel(frame_lista, text=email).grid(row=idx+1, column=2, padx=10, pady=2)
            ctk.CTkLabel(frame_lista, text=f"R$ {multa:.2f}").grid(row=idx+1, column=3, padx=10, pady=2)

    def iniciar(self):
        self.janela.mainloop()

if __name__ == "__main__":
    app = SistemaBiblioteca()
    app.iniciar() 