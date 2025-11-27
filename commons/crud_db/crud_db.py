from commons.models.models import Produto, Cliente
from commons.conn.conexao import session   

# ====== Queries para Produtos ======

def obter_todos_produtos_db():
    try:
        with session:
            produtos = session.query(Produto).all()
        return produtos
    except Exception as e:
        print("Erro ao obter produtos:", e)

def reduzir_estoque_db(id_produto, quantidade):
    try:
        with session:
            produto = session.query(Produto).filter_by(id=id_produto).first()    
            produto.quantidade -= quantidade
            session.commit()
    except Exception as e:
        print("Erro ao reduzir estoque:", e)

def buscar_por_id_db(id_produto):
    try:
        with session:
            produto_procurado = session.query(Produto).filter_by(id=id_produto).first()
        return produto_procurado
    except Exception as e:
        print("Erro ao buscar produto por ID:", e)

def buscar_quantidade_por_id_db(id_produto):
    try:
        with session:
            produto_procurado = session.query(Produto).filter_by(id=id_produto).first()
        return produto_procurado.quantidade
    except Exception as e:
        print("Erro ao buscar produto por ID:", e)

def verificar_sem_estoque_db():
    try:
        with session:
            sem_estoque = session.query(Produto).filter(Produto.quantidade == 0).all()
        return sem_estoque
    except Exception as e:
        print("Erro ao verificar produtos sem estoque:", e)

# ====== Queries para Clientes ======

def contar_clientes_db():
    try:
        with session:
            qtd_clientes = session.query(Cliente).count()
        return qtd_clientes
    except Exception as e:
        print("Erro ao contar clientes:", e)

def carregar_mocki_clientes_db(clientes_para_mocki):
    try:
        with session:
            for _, cliente in clientes_para_mocki.iterrows():
                objeto_cliente = Cliente(None, nome=cliente["nome"])
                session.add(objeto_cliente)
            session.commit()
    except Exception as e:
        print("Erro ao carregar clientes mocki:", e)

def procurar_cliente_db(id_cliente):
    try:
        with session:
            cliente = session.query(Cliente).filter_by(id_cliente=id_cliente).first()
        return cliente
    except Exception as e:
        print("Erro ao procurar cliente por ID:", e)
    
def armazenar_cliente_db(nome_cliente, id_cliente):
    try:
        with session:
            novo_cliente = Cliente(id_cliente=id_cliente, nome=nome_cliente)
            session.add(novo_cliente)
            session.commit()
            return novo_cliente.nome
    except Exception as e:
        print("Erro ao armazenar novo cliente:", e)

def obter_nome_cliente_db(id_cliente):
    try:
        with session:
            cliente = session.query(Cliente).filter_by(id_cliente=id_cliente).first()
        return cliente.nome
    except Exception as e:
        print("Erro ao obter nome do cliente por ID:", e) 

def procurar_nome_cliente_db(nome_cliente):
    try:
        with session:
            cliente = session.query(Cliente).filter_by(nome=nome_cliente).first()
        return cliente
    except Exception as e:
        print("Erro ao procurar cliente por nome:", e)        