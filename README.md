# Sistema de Gerenciamento de Biblioteca

Um sistema completo de gerenciamento de biblioteca desenvolvido em Python com interface gráfica moderna e banco de dados SQLite.

## Funcionalidades

- Sistema de autenticação de usuários (admin e bibliotecário)
- Cadastro e gerenciamento de livros
- Cadastro e gerenciamento de usuários
- Interface gráfica moderna e intuitiva
- Banco de dados SQLite para persistência
- Sistema de busca avançada
- Geração de multas por atraso

## Requisitos

- Python 3.8 ou superior
- Tkinter (incluído na instalação padrão do Python)
- CustomTkinter
- Pillow
- bcrypt
- python-dotenv

## Instalação

1. Clone este repositório:
```bash
git clone https://github.com/seu-usuario/sistema-biblioteca.git
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure o arquivo `.env` com as credenciais iniciais:
```
ADMIN_EMAIL=admin@admin.com
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
```

## Como usar

Execute o arquivo principal:
```bash
python main.py
```

## Estrutura do Projeto

- `main.py`: Arquivo principal do aplicativo
- `database/`: Diretório com arquivos relacionados ao banco de dados
- `models/`: Classes e modelos do sistema
- `views/`: Interfaces gráficas
- `controllers/`: Lógica de negócios
- `utils/`: Funções utilitárias
- `assets/`: Recursos gráficos e ícones

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests. 