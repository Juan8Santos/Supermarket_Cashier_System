from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, func
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    quantidade = Column(Integer, nullable=False, default=0)
    preco = Column(Float, nullable=False)

    itens = relationship("Item", back_populates="produto")
    fornecedores = relationship(
        "Fornecedor",
        secondary="produtos_fornecedores",
        back_populates="produtos"
    )

    def __init__(self, nome, quantidade, preco):
        self.nome = nome
        self.quantidade = quantidade
        self.preco = preco

    def __str__(self):
        return f"{self.nome} {self.quantidade} {self.preco:.2f}"


class Fornecedor(Base):
    __tablename__ = "fornecedores"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)

    produtos = relationship(
        "Produto",
        secondary="produtos_fornecedores",
        back_populates="fornecedores"
    )

    def __init__(self, nome):
        self.nome = nome

    def __str__(self):
        return f"{self.nome}"


class Cliente(Base):
    __tablename__ = "clientes"

    id_cliente = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)

    compras = relationship("Compra", back_populates="cliente")

    def __init__(self, id_cliente, nome):
        self.id_cliente = id_cliente
        self.nome = nome

    def __str__(self):
        return f"{self.nome}"


class Compra(Base):
    __tablename__ = "compras"

    id = Column(Integer, primary_key=True, autoincrement=True)
    data_hora = Column(DateTime, nullable=False, server_default=func.now())
    id_cliente = Column(Integer, ForeignKey("clientes.id_cliente"), nullable=False)

    cliente = relationship("Cliente", back_populates="compras")
    itens = relationship("Item", back_populates="compra")

    def __init__(self, id_cliente):
        self.id_cliente = id_cliente


    def __str__(self):
        return f"{self.id_cliente}"


class Item(Base):
    __tablename__ = "itens"

    id = Column(Integer, primary_key=True, autoincrement=True)
    compra_id = Column(Integer, ForeignKey("compras.id"), nullable=False)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    quantidade = Column(Integer, nullable=False)
    preco_unitario = Column(Float, nullable=False)

    compra = relationship("Compra", back_populates="itens")
    produto = relationship("Produto", back_populates="itens")

    def __init__(self, compra_id, produto_id, quantidade, preco_unitario):
        self.compra_id = compra_id
        self.produto_id = produto_id
        self.quantidade = quantidade
        self.preco_unitario = preco_unitario

    def __str__(self):
        return f"{self.compra_id} {self.produto_id} {self.quantidade} {self.preco:.2f}"


class ProdutosFornecedores(Base):
    __tablename__ = "produtos_fornecedores"

    produto_id = Column(Integer, ForeignKey("produtos.id"), primary_key=True)
    fornecedor_id = Column(Integer, ForeignKey("fornecedores.id"), primary_key=True)

    def __init__(self, produto_id, fornecedor_id):
        self.produto_id = produto_id
        self.fornecedor_id = fornecedor_id

    def __str__(self):
        return f"{self.produto_id} {self.fornecedor_id}"
