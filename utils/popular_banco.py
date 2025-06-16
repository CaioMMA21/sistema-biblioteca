import sqlite3
import random
from faker import Faker

fake = Faker('pt_BR')

db_path = "database/biblioteca.db"

TITULOS = [
    "O Senhor dos Anéis", "Dom Quixote", "O Pequeno Príncipe", "Harry Potter e a Pedra Filosofal",
    "Cem Anos de Solidão", "Orgulho e Preconceito", "A Menina que Roubava Livros", "O Hobbit",
    "1984", "O Código Da Vinci", "O Alquimista", "A Culpa é das Estrelas", "O Nome do Vento",
    "O Diário de Anne Frank", "O Caçador de Pipas", "A Revolução dos Bichos", "O Morro dos Ventos Uivantes",
    "O Silmarillion", "O Retrato de Dorian Gray", "O Apanhador no Campo de Centeio", "O Lobo da Estepe",
    "O Médico e o Monstro", "O Processo", "O Velho e o Mar", "O Grande Gatsby", "O Iluminado",
    "O Sol é para Todos", "O Padrão Bitcoin", "O Homem Invisível", "O Guia do Mochileiro das Galáxias"
]
AUTORES = [
    "J.R.R. Tolkien", "Miguel de Cervantes", "Antoine de Saint-Exupéry", "J.K. Rowling",
    "Gabriel García Márquez", "Jane Austen", "Markus Zusak", "George Orwell",
    "Dan Brown", "Paulo Coelho", "John Green", "Patrick Rothfuss", "Anne Frank",
    "Khaled Hosseini", "Emily Brontë", "Oscar Wilde", "J.D. Salinger", "Hermann Hesse",
    "Robert Louis Stevenson", "Franz Kafka", "Ernest Hemingway", "F. Scott Fitzgerald",
    "Stephen King", "Harper Lee", "Saifedean Ammous", "H.G. Wells", "Douglas Adams"
]

def popular_livros(cursor, quantidade=30):
    for i in range(quantidade):
        titulo = TITULOS[i % len(TITULOS)] + f" Vol. {random.randint(1,3)}"
        autor = random.choice(AUTORES)
        isbn = fake.isbn13()
        quantidade = random.randint(1, 10)
        try:
            cursor.execute(
                "INSERT INTO livros (titulo, autor, isbn, quantidade, disponivel) VALUES (?, ?, ?, ?, ?)",
                (titulo, autor, isbn, quantidade, quantidade)
            )
        except Exception:
            pass

def popular_clientes(cursor, quantidade=10):
    for _ in range(quantidade):
        nome = fake.name()
        numero = fake.phone_number()
        email = fake.email()
        try:
            cursor.execute(
                "INSERT INTO clientes (nome, numero, email) VALUES (?, ?, ?)",
                (nome, numero, email)
            )
        except Exception:
            pass

def main():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    popular_livros(cursor, 30)
    popular_clientes(cursor, 10)
    conn.commit()
    conn.close()
    print("Banco populado com 30 livros e 10 clientes!")

if __name__ == "__main__":
    main() 