from commons.models.models import Produto, Cliente, Fornecedor, ProdutosFornecedores, Compra, Item
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
        return session.query(Cliente).filter_by(id_cliente=id_cliente).first()
    except Exception as e:
        print("Erro ao procurar cliente por ID:", e)
    
def armazenar_cliente_db(nome_cliente, id_cliente):
    try:
        with session:
            novo_cliente = Cliente(id_cliente=id_cliente, nome=nome_cliente)
            session.add(novo_cliente)
            session.commit()
    except Exception as e:
        print("Erro ao armazenar novo cliente:", e)

def obter_cliente_db(id_cliente):
    try:
        cliente = session.query(Cliente).filter_by(id_cliente=id_cliente).first()
        return cliente
    except Exception as e:
        print("Erro ao obter nome do cliente por ID:", e)

def procurar_nome_cliente_db(nome_cliente):
    try:
        with session:
            cliente = session.query(Cliente).filter_by(nome=nome_cliente).first()
        return cliente
    except Exception as e:
        print("Erro ao procurar cliente por nome:", e)

# ====== Queries para insert de base de dados no BD ======  

def armazenar_produtos_no_db(dataframe_produtos):
    try:
        with session:
            session.query(Produto).delete()
            session.commit()
            for _, linha in dataframe_produtos.iterrows():
                produto = Produto(
                    nome=linha['Nome'],
                    quantidade=int(linha['Quantidade']),
                    preco=float(linha['Preço'])
                )
                session.add(produto)
            session.commit()
    except Exception as e:
        print("Erro ao armazenar produtos no banco de dados:", e)

def armazenar_fornecedores_no_db(dataframe_fornecedores):
    try:
        with session:
            session.query(Fornecedor).delete()
            session.commit()
            for _, linha in dataframe_fornecedores.iterrows():
                fornecedor = Fornecedor(
                    nome=linha['nome']
                )
                session.add(fornecedor)
            session.commit()
    except Exception as e:
        print("Erro ao armazenar fornecedores no banco de dados:", e)

def armazenar_produtos_fornecedores_no_db(dataframe_produtos_fornecedores):
    try:
        with session:
            session.query(ProdutosFornecedores).delete()
            session.commit()
            for _, linha in dataframe_produtos_fornecedores.iterrows():
                produto_id = int(linha['id_produto'])
                fornecedor_id = int(linha['id_fornecedor'])
                produtos_fornecedores = ProdutosFornecedores(
                    produto_id=produto_id,
                    fornecedor_id=fornecedor_id
                )
                session.add(produtos_fornecedores)
            session.commit()
    except Exception as e:
        print("Erro ao armazenar produtos e fornecedores no banco de dados:", e)

# ====== Queries para Produtos ======

def armazenar_compras_no_db(id_cliente):
    try:
        with session:
            nova_compra = Compra(
                id_cliente=id_cliente
            )
            session.add(nova_compra)
            session.commit()
            return nova_compra.id
    except Exception as e:
        print("Erro ao armazenar nova compra no banco de dados:", e)

# ====== Queries para Itens ======

def armazenar_itens_compra_no_db(id_compra, sacola):
    try:
        with session:
            for produto, quantidade in sacola:
                novo_item = Item(
                    compra_id=id_compra,
                    produto_id=produto.id,
                    quantidade=quantidade,
                    preco_unitario=produto.preco
                )
                session.add(novo_item)
            session.commit()
    except Exception as e:
        print("Erro ao armazenar itens da compra no banco de dados:", e)