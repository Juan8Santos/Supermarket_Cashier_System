from commons.models.models import Produto, Cliente, Fornecedor, ProdutosFornecedores, Compra, Item
from commons.conn.conexao import session
from sqlalchemy import *
from sqlalchemy.orm import joinedload

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

def armazenar_produto_db(nome_produto, quantidade_produto, preco_produto):
    try:
        novo_produto = Produto(
            nome=nome_produto,
            quantidade=quantidade_produto,
            preco=preco_produto
        )
        session.add(novo_produto)
        session.commit()
        return novo_produto
    except Exception as e:
        print("Erro ao armazenar novo produto:", e)

def buscar_produto_por_nome_db(nome_produto):
    try:
        produto_procurado = session.query(Produto).filter_by(nome=nome_produto).first()
        return produto_procurado
    except Exception as e:
        print("Erro ao buscar produto por nome:", e)

def atualizar_produto_db(id_produto, novo_nome, nova_quantidade, novo_preco):
    try:
        produto = session.query(Produto).filter_by(id=id_produto).first()
        produto.nome = novo_nome
        produto.quantidade = nova_quantidade
        produto.preco = novo_preco
        session.commit()
        return True
    except Exception as e:
        print(f"Erro ao atualizar produto: {e}")

def remover_produto_db(produto):
    try:
        session.delete(produto)
        session.commit()
    except Exception as e:
        print(f"Erro ao remover produto: {e}")  

def produtos_mais_vendidos_db():
    try:
        resultados = (
        session.query(
            Produto.nome,
            func.sum(Item.quantidade).label("total_vendido")
        )
        .join(Item, Produto.id == Item.produto_id)
        .group_by(Produto.id)
        .order_by(func.sum(Item.quantidade).desc())
        .limit(3)
        .all()
        )
        return resultados
    except Exception as e:
        print("Erro ao consultar produtos mais vendidos:", e)

def produtos_menos_vendidos_db():
    try:
        resultados = (
            session.query(
                Produto,
                func.sum(Item.quantidade).label("total_vendido")
            )
            .join(Item, Produto.id == Item.produto_id)
            .group_by(Produto.id)
            .order_by(func.sum(Item.quantidade).asc())
            .limit(3)
            .all()
        )
        return resultados
    except Exception as e:
        print("Erro ao consultar produtos menos vendidos:", e)

def produtos_com_pouco_estoque_db(limite):
    try:
        produtos = (
            session.query(Produto)
            .filter(Produto.quantidade <= limite)
            .order_by(Produto.quantidade.asc())
            .all()
        )
        return produtos
    except Exception as e:
        print("Erro ao consultar produtos com pouco estoque:", e)

# ====== Queries para Clientes ======

def listar_todos_clientes_com_contagem_de_compras_db():
    try:
        clientes = session.query(Cliente)\
            .outerjoin(Compra, Cliente.id_cliente == Compra.id_cliente)\
            .options(joinedload(Cliente.compras))\
            .all()
        return clientes
    except Exception as e:
        print("Erro ao listar clientes com contagem de compras:", e)

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
                objeto_cliente = Cliente(id_cliente=None, nome=cliente["nome"])
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

def compras_do_cliente_db(id_cliente):
    try:
        compras_cliente = (
            session.query(Compra)
            .options(joinedload(Compra.itens).joinedload(Item.produto))
            .filter(Compra.id_cliente == id_cliente)
            .all()
        )
        return compras_cliente
    except Exception as e:
        print("Erro ao obter compras do cliente:", e)

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

# ====== Queries para Itens ======

def armazenar_itens_compra_no_db(id_compra, grupos):
    try:       
        with session:
            for item in grupos.values():
                produto = item["produto"]
                quantidade = item["quantidade"]
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

# ====== Queries para compras ======

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

def consultar_compra_filtrado_por_cliente_e_compra__db(id_compra, id_cliente):
    try:
        with session:
            compra = session.query(Compra)\
                .options(
                    joinedload(Compra.itens).joinedload(Item.produto),
                    joinedload(Compra.cliente)
                )\
                .filter_by(id=id_compra, id_cliente=id_cliente)\
                .first()
            return compra
    except Exception as e:
        print("Erro ao consultar itens da compra:", e)

def consultar_clientes_com_mais_compras_db():
    try:
        with session:
            resultados = session.query(
                Cliente.nome,
                func.count(Compra.id).label("total_compras")
            ).join(Compra)\
             .group_by(Cliente.id_cliente)\
             .order_by(func.count(Compra.id).desc())\
             .limit(3)\
             .all()
            return resultados
    except Exception as e:
        print("Erro ao consultar clientes que mais compram:", e)

def clientes_que_mais_gastam_db():
    try:
        with session:
            resultados = session.query(
                Cliente.nome,
                func.sum(Item.quantidade * Item.preco_unitario).label("total_gasto")
            ).select_from(Cliente)\
             .join(Compra, Compra.id_cliente == Cliente.id_cliente)\
             .join(Item, Item.compra_id == Compra.id)\
             .group_by(Cliente.id_cliente)\
             .order_by(func.sum(Item.quantidade * Item.preco_unitario).desc())\
             .limit(3)\
             .all()
            return resultados
    except Exception as e:
        print("Erro ao consultar clientes que mais gastam:", e)

def consultar_clientes_sem_compras_db():
    try:
        with session:
            resultados = session.query(Cliente)\
                .outerjoin(Compra, Compra.id_cliente == Cliente.id_cliente)\
                .filter(Compra.id == None)\
                .all()
            return resultados
    except Exception as e:
        print("Erro ao consultar clientes sem compras:", e)

# ====== Queries para Fornecedores ======

def consultar_todos_fornecedores_db():
    try:
        with session:
            fornecedores = session.query(Fornecedor).all()
        return fornecedores
    except Exception as e:
        print("Erro ao obter fornecedores:", e)

def procurar_fornecedor_db(id_fornecedor):
    try:
        return session.query(Fornecedor).filter_by(id=id_fornecedor).first()
    except Exception as e:
        print("Erro ao procurar fornecedor por ID:", e)

def obter_fornecedores_do_produto_db(id_produto):
    try:
        produto = session.query(Produto)\
            .options(joinedload(Produto.fornecedores))\
            .filter_by(id=id_produto)\
            .first()
        return produto.fornecedores
    except Exception as e:
        print("Erro ao obter fornecedores do produto:", e)

def armazenar_relacionamento_produto_fornecedor_db(id_produto, id_fornecedor):
    try:
        with session:
            relacionamento = ProdutosFornecedores(
                produto_id=id_produto,
                fornecedor_id=id_fornecedor
            )
            session.add(relacionamento)
            session.commit()
    except Exception as e:
        print("Erro ao armazenar relacionamento produto-fornecedor:", e)

def verificar_relacionamento_produto_fornecedor_db(id_produto, id_fornecedor):
    try:
        with session:
            relacionamento_existente = session.query(ProdutosFornecedores)\
                .filter_by(produto_id=id_produto, fornecedor_id=id_fornecedor)\
                .first()
            return relacionamento_existente
    except Exception as e:
        print("Erro ao verificar relacionamento produto-fornecedor:", e)