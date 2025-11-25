from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Produto(Base):
    __tablename__ = 'produtos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    quantidade = Column(Integer, nullable=False)
    preco = Column(Float, nullable=False)

    def __init__(self, nome, quantidade, preco):
            self.nome = nome
            self.quantidade = quantidade
            self.preco = preco

    def __str__(self):
        return f"{self.nome} (ID: {self.id}) - Qnt: {self.quantidade} - R${self.preco:.2f}"

class Cliente(Base):
    __tablename__ = "clientes"

    id_cliente = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)

    def __init__(self, id_cliente, nome):
            self.id_cliente = id_cliente
            self.nome = nome

    def __str__(self):
        return f"{self.id_cliente} - {self.nome}"