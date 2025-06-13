import customtkinter as ctk
from tkinter import messagebox
import os
from dotenv import load_dotenv
from database.database import Database

class SistemaBiblioteca:
    def __init__(self):
        self.janela = ctk.CTk()
        self.janela.title("Sistema de Gerenciamento de Biblioteca")
        self.janela.geometry("800x600")
        
        # Configuração do tema
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Carrega variáveis de ambiente
        load_dotenv()
        
        # Inicializa o banco de dados
        self.db = Database()
        self.db.criar_usuario_admin(
            os.getenv("ADMIN_USERNAME", "admin"),
            os.getenv("ADMIN_PASSWORD", "admin123")
        )
        
        # Interface
        self.criar_interface_login()
        
    def criar_interface_login(self):
        # Frame principal
        self.frame_login = ctk.CTkFrame(self.janela)
        self.frame_login.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Título
        titulo = ctk.CTkLabel(
            self.frame_login,
            text="Sistema de Gerenciamento de Biblioteca",
            font=("Arial", 24, "bold")
        )
        titulo.pack(pady=20)
        
        # Campos de login
        frame_campos = ctk.CTkFrame(self.frame_login)
        frame_campos.pack(pady=20, padx=40, fill="x")
        
        # Email
        label_email = ctk.CTkLabel(frame_campos, text="Email:")
        label_email.pack(anchor="w", pady=(10, 0))
        
        self.entrada_email = ctk.CTkEntry(frame_campos, placeholder_text="Digite seu email")
        self.entrada_email.pack(fill="x", pady=(0, 10))
        
        # Senha
        label_senha = ctk.CTkLabel(frame_campos, text="Senha:")
        label_senha.pack(anchor="w", pady=(10, 0))
        
        self.entrada_senha = ctk.CTkEntry(frame_campos, placeholder_text="Digite sua senha", show="*")
        self.entrada_senha.pack(fill="x", pady=(0, 10))
        
        # Botão de login
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
        # Frame principal
        self.frame_principal = ctk.CTkFrame(self.janela)
        self.frame_principal.pack(fill="both", expand=True)
        
        # Barra superior
        frame_superior = ctk.CTkFrame(self.frame_principal)
        frame_superior.pack(fill="x", padx=20, pady=10)
        
        # Informações do usuário
        label_usuario = ctk.CTkLabel(
            frame_superior,
            text=f"Bem-vindo, {usuario[1]}!",
            font=("Arial", 16)
        )
        label_usuario.pack(side="left", padx=10)
        
        # Botão de logout
        botao_logout = ctk.CTkButton(
            frame_superior,
            text="Sair",
            command=self.fazer_logout
        )
        botao_logout.pack(side="right", padx=10)
        
        # Menu lateral
        frame_menu = ctk.CTkFrame(self.frame_principal, width=200)
        frame_menu.pack(side="left", fill="y", padx=20, pady=20)
        
        # Botões do menu
        botoes_menu = [
            ("Livros", self.mostrar_livros),
            ("Usuários", self.mostrar_usuarios),
            ("Clientes", self.mostrar_clientes),
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
            
        # Área de conteúdo
        self.frame_conteudo = ctk.CTkFrame(self.frame_principal)
        self.frame_conteudo.pack(side="right", fill="both", expand=True, padx=20, pady=20)
        
        # Mostra a tela de livros por padrão
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
        label = ctk.CTkLabel(self.frame_conteudo, text="Gerenciamento de Usuários")
        label.pack(pady=20)
        
    def mostrar_emprestimos(self):
        self.limpar_conteudo()
        label = ctk.CTkLabel(self.frame_conteudo, text="Gerenciamento de Empréstimos")
        label.pack(pady=20)
        
    def mostrar_relatorios(self):
        self.limpar_conteudo()
        label = ctk.CTkLabel(self.frame_conteudo, text="Relatórios e Estatísticas")
        label.pack(pady=20)
        
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

        frame_principal = ctk.CTkFrame(self.frame_conteudo)
        frame_principal.pack(pady=10, padx=20, fill="both", expand=True)

        # Formulário de cadastro de usuário
        frame_usuario = ctk.CTkFrame(frame_principal)
        frame_usuario.grid(row=0, column=0, padx=20, pady=10, sticky="n")
        label_usuario = ctk.CTkLabel(frame_usuario, text="Cadastro de Usuário", font=("Arial", 14, "bold"))
        label_usuario.pack(pady=10)
        label_nome = ctk.CTkLabel(frame_usuario, text="Nome:")
        label_nome.pack(anchor="w")
        self.entrada_nome_cadastro = ctk.CTkEntry(frame_usuario, width=250)
        self.entrada_nome_cadastro.pack(pady=2)
        label_email = ctk.CTkLabel(frame_usuario, text="Email:")
        label_email.pack(anchor="w")
        self.entrada_email_cadastro = ctk.CTkEntry(frame_usuario, width=250)
        self.entrada_email_cadastro.pack(pady=2)
        label_senha = ctk.CTkLabel(frame_usuario, text="Senha:")
        label_senha.pack(anchor="w")
        self.entrada_senha_cadastro = ctk.CTkEntry(frame_usuario, show="*", width=250)
        self.entrada_senha_cadastro.pack(pady=2)
        botao_cadastrar_usuario = ctk.CTkButton(frame_usuario, text="Cadastrar Usuário", command=self.cadastrar_usuario)
        botao_cadastrar_usuario.pack(pady=10)

        # Formulário de cadastro de livro
        frame_livro = ctk.CTkFrame(frame_principal)
        frame_livro.grid(row=0, column=1, padx=20, pady=10, sticky="n")
        label_livro = ctk.CTkLabel(frame_livro, text="Cadastro de Livro", font=("Arial", 14, "bold"))
        label_livro.pack(pady=10)
        label_titulo = ctk.CTkLabel(frame_livro, text="Título:")
        label_titulo.pack(anchor="w")
        self.entrada_titulo_livro = ctk.CTkEntry(frame_livro, width=250)
        self.entrada_titulo_livro.pack(pady=2)
        label_autor = ctk.CTkLabel(frame_livro, text="Autor:")
        label_autor.pack(anchor="w")
        self.entrada_autor_livro = ctk.CTkEntry(frame_livro, width=250)
        self.entrada_autor_livro.pack(pady=2)
        label_isbn = ctk.CTkLabel(frame_livro, text="ISBN:")
        label_isbn.pack(anchor="w")
        self.entrada_isbn_livro = ctk.CTkEntry(frame_livro, width=250)
        self.entrada_isbn_livro.pack(pady=2)
        label_quantidade = ctk.CTkLabel(frame_livro, text="Quantidade:")
        label_quantidade.pack(anchor="w")
        self.entrada_quantidade_livro = ctk.CTkEntry(frame_livro, width=100)
        self.entrada_quantidade_livro.pack(pady=2)
        botao_cadastrar_livro = ctk.CTkButton(frame_livro, text="Cadastrar Livro", command=self.cadastrar_livro)
        botao_cadastrar_livro.pack(pady=10)

        # Formulário de cadastro de cliente
        frame_cliente = ctk.CTkFrame(frame_principal)
        frame_cliente.grid(row=0, column=2, padx=20, pady=10, sticky="n")
        label_cliente = ctk.CTkLabel(frame_cliente, text="Cadastro de Cliente", font=("Arial", 14, "bold"))
        label_cliente.pack(pady=10)
        label_nome_cli = ctk.CTkLabel(frame_cliente, text="Nome:")
        label_nome_cli.pack(anchor="w")
        self.entrada_nome_cliente = ctk.CTkEntry(frame_cliente, width=200)
        self.entrada_nome_cliente.pack(pady=2)
        label_numero_cli = ctk.CTkLabel(frame_cliente, text="Número:")
        label_numero_cli.pack(anchor="w")
        self.entrada_numero_cliente = ctk.CTkEntry(frame_cliente, width=200)
        self.entrada_numero_cliente.pack(pady=2)
        label_email_cli = ctk.CTkLabel(frame_cliente, text="Email:")
        label_email_cli.pack(anchor="w")
        self.entrada_email_cliente = ctk.CTkEntry(frame_cliente, width=200)
        self.entrada_email_cliente.pack(pady=2)
        botao_cadastrar_cliente = ctk.CTkButton(frame_cliente, text="Cadastrar Cliente", command=self.cadastrar_cliente)
        botao_cadastrar_cliente.pack(pady=10)

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