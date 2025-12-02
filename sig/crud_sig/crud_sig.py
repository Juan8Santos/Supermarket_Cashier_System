from sig.menu_sig.menu_sig import exibir_menu_sig, menu_modulo_clientes_sig, menu_modulo_produtos_sig, menu_clientes_com_compras
from commons.utils.util import entrar_int_personalizado, entrar_int, entrar_float
from commons.crud_db.crud_db import *
from tabulate import tabulate

# ====== Funções para senha inicial sistema SIG ======

def exigir_senha_inicial_sig():
    senha_encriptada = "Vlj456"
    tentativas = 3
    while tentativas > 0:
        entrada = input(">> Digite a senha para acessar o sistema SIG: ")
        if entrada == desencriptografar(senha_encriptada):
            print("\nAcesso concedido.\n")
            dashboard_principal_sig()
            return
        else:
            tentativas -= 1
            print(f"\nSenha incorreta. Você tem {tentativas} tentativas restantes!\n")
    print("Número máximo de tentativas excedido! Retornando ao menu principal.\n")
    from app_controller import AppController
    app = AppController()
    app.restart_loop()

def desencriptografar(senha_criptografada):
    return ''.join(chr(ord(caracter) - 3) for caracter in senha_criptografada)

# ====== Função de navegação sistema SIG ======

def dashboard_principal_sig():
    while True:
        exibir_menu_sig()
        entrada = entrar_int_personalizado(">> Escolha uma opção: ", 1, 3)
        try:
            match entrada:
                case 1:
                    print("")
                    modulo_clientes_sig()
                case 2:
                    print("")
                    modulo_produtos_sig()
                case 3:
                    from app_controller import AppController
                    print("")
                    app = AppController()
                    app.restart_loop()
                    break
                case _:
                    raise ValueError("Opção inválida. Tente novamente.")
        except Exception as e:
            print(f"Erro inesperado ao iniciar o sistema: {e}")

def modulo_clientes_sig():
    while True:
        menu_modulo_clientes_sig()
        entrada = entrar_int_personalizado(">> Escolha uma opção: ", 1, 3)
        try:
            match entrada:
                case 1:
                    print("")
                    decidir_opcao_no_clientes_com_compras()
                case 2:
                    print("")
                    listar_clientes_sem_compras()
                case 3:
                    print("")
                    dashboard_principal_sig()
                case _:
                    raise ValueError("Opção inválida. Tente novamente.")
        except Exception as e:
            print(f"Erro inesperado no módulo de clientes: {e}")

def modulo_produtos_sig():
    while True:
        menu_modulo_produtos_sig()
        entrada = entrar_int_personalizado(">> Escolha uma opção: ", 1, 8)
        try:
            match entrada:
                case 1:
                    cadastrar_novo_produto()
                case 2:
                    atualizar_produto()
                case 3:
                    remover_produto()
                case 4:
                    consultar_fornecedores_produto()
                case 5:
                    produtos_mais_vendidos()
                case 6:
                    produtos_menos_vendidos()
                case 7:
                    produtos_com_pouco_estoque()
                case 8:
                    print("")
                    dashboard_principal_sig()
                case _:
                    raise ValueError("Opção inválida. Tente novamente.")
        except Exception as e:
            print(f"Erro inesperado no módulo de produtos: {e}")

# ====== Função para o modulo clientes ======

def decidir_opcao_no_clientes_com_compras():
    while True:
        menu_clientes_com_compras()
        entrada = entrar_int_personalizado("\n>> Digite a opção desejada: ", 1, 4)
        match entrada:
            case 1:
                print("")
                consultar_cliente_com_compras()
            case 2:
                print("")
                clientes_com_mais_compras()
            case 3:
                print("")
                clientes_que_mais_gastam()
            case 4:
                break
        
def consultar_cliente_com_compras():
    while True:
        formatar_clientes_mais_compras()
        entrada = entrar_int(">> Digite o id do cliente que deseja encontrar o histórico: ")
        cliente = procurar_cliente_db(entrada)
        if cliente is None:
            print("\nCliente não encontrado. Tente novamente.")
        elif compras_do_cliente_db(cliente.id_cliente) is None or len(compras_do_cliente_db(cliente.id_cliente)) == 0:
            print("\nCliente não possui compras registradas.")
        else:
            compras = compras_do_cliente_db(cliente.id_cliente)
            formatar_historico_compras_cliente(cliente, compras)
            decidir_consultar_compra_do_cliente(cliente, compras)
            break

def formatar_clientes_mais_compras():
    produtos = listar_todos_clientes_com_contagem_de_compras_db()
    print("\nClientes e quantidades compras:\n")
    for cliente in produtos:
        total_compras = len(cliente.compras) if cliente.compras else 0
        print(f"- Id {cliente.id_cliente} | {cliente.nome} | Total de compras: {total_compras}")
    print("")

def formatar_historico_compras_cliente(cliente, compras):
    print(f"\nHistórico de compras do cliente {cliente.nome}:\n")
    for compra in compras:
        total = sum(item.quantidade * item.preco_unitario for item in compra.itens)
        print(f"- Compra ID: {compra.id}, Data e Hora: {compra.data_hora}, total: R$ {total:.2f}")
    print("")

def decidir_consultar_compra_do_cliente(cliente, compras):
    while True:
        entrada = entrar_int_personalizado(">> Deseja consultar alguma compra? [1 - Sim / 2 - Não]: ", 1, 2)
        match entrada:
            case 1:
                consultar_compra_do_cliente(cliente, compras)
            case 2:
                break
            case _:
                print("Opção inválida. Tente novamente.")

def consultar_compra_do_cliente(cliente, compras):
    while True:
        entrada = entrar_int("\n>> Digite o id da compra que deseja consultar: ")
        compra_encontrada = next((compra for compra in compras if compra.id == entrada), None)     
        if compra_encontrada:
            compra = consultar_compra_filtrado_por_cliente_e_compra__db(compra_encontrada.id, cliente.id_cliente)
            formatar_detalhes_compra_cliente(compra)
            break
        else:
            print("Compra não encontrada. Tente novamente.")

def formatar_detalhes_compra_cliente(compra):
    print(f"\nDetalhes da compra ID {compra.id} - Cliente: {compra.cliente.nome}")
    print(f"Data e Hora: {compra.data_hora}\n")
    gerar_tabela_boleto_de_compra(compra)


def gerar_tabela_boleto_de_compra(compra):
    tabela = []
    valor_total = 0
    for item in compra.itens:
        subtotal = item.quantidade * item.preco_unitario
        valor_total += subtotal
        tabela.append({
            "produto": item.produto.nome,
            "quantidade": item.quantidade,
            "preco_unitario": item.preco_unitario,
            "subtotal": subtotal
        })
    print(tabulate(tabela, headers="keys"))
    print(f"\nValor Total da Compra: R$ {valor_total:.2f}\n")

def clientes_com_mais_compras():
    print("Clientes que mais compram:")
    tabela_compras = consultar_clientes_com_mais_compras_db()
    for nome, compras in tabela_compras:
        print(f"- {nome} | {compras} compras")
    print("")

def clientes_que_mais_gastam():
    print("Clientes que mais gastam:")
    tabela_gastos = clientes_que_mais_gastam_db()
    for nome, total in tabela_gastos:
        print(f"- {nome} | R$ {total:.2f}")
    print("")

def listar_clientes_sem_compras():
    clientes = consultar_clientes_sem_compras_db()
    if not clientes:
        print("\nTodos os clientes possuem compras registradas.")
    else:
        print("\nClientes que não possuem compras:\n")
        for cliente in clientes:
            print(f"- Id {cliente.id_cliente} | {cliente.nome}")
    modulo_clientes_sig()

# ====== Funções para o modulo produtos ======

def cadastrar_novo_produto():
        while True:
            nome = input("\n>> Digite o nome do produto: ")
            preco = entrar_float("\n>> Digite o preço do produto: ")
            quantidade_estoque = entrar_int("\n>> Digite a quantidade em estoque do produto: ")
            produto_existente = buscar_produto_por_nome_db(nome)
            if produto_existente is None:
                produto = armazenar_produto_db(nome, quantidade_estoque, preco)
                print(f"\nProduto {produto.nome} cadastrado com sucesso.")
                relacionar_produto_fornecedor(produto.id)
                break
            else:
                print(f"\nProduto {nome} já existe. Tente outro nome.")

def relacionar_produto_fornecedor(id_produto):
    while True:
        listar_fornecedores_db()
        entrada = entrar_int("\n>> Digite o [ID] do fornecedor para relacionar um fornecedor a um produto: ",)
        fornecedor = procurar_fornecedor_db(entrada)
        if fornecedor is None:
            print("\nFornecedor não encontrado. Tente novamente.")
            continue
        if verificar_relacionamento_produto_fornecedor_db(id_produto, fornecedor.id) is None:
            armazenar_relacionamento_produto_fornecedor_db(id_produto, fornecedor.id)
            print(f"\nProduto relacionado ao fornecedor {fornecedor.nome} com sucesso.\n")
            decidir_adicionar_outro_fornecedor(id_produto)
        else:
            print("\nEsse fornecedor já está relacionado a esse produto. Tente novamente.")

def decidir_adicionar_outro_fornecedor(id_produto):
    while True:
        entrada = entrar_int_personalizado(">> Deseja adicionar outro fornecedor? [1 - Sim / 2 - Não]: ", 1, 2)
        match entrada:
            case 1:
                relacionar_produto_fornecedor(id_produto)
            case 2:
                modulo_produtos_sig()
            case _:
                print("Opção inválida. Tente novamente.")

def listar_fornecedores_db():
    fornecedores = consultar_todos_fornecedores_db()
    print("\nFornecedores disponíveis:\n")
    for fornecedor in fornecedores:
        print(f"- Id {fornecedor.id}: {fornecedor.nome}")

def atualizar_produto():
    while True:
        produtos = obter_todos_produtos_db()
        if not produtos:
            print("\nNenhum produto cadastrado.")
            return
        exibir_produtos()
        id_produto = entrar_int("\n>> Digite o ID do produto que deseja atualizar: ")
        produto = buscar_por_id_db(id_produto)
        if produto is None:
            print("\nProduto não encontrado. Tente novamente.")
        else:
            print(f"\nAtualizando produto: {produto.nome} | Preço: R$ {produto.preco:.2f} | Estoque: {produto.quantidade}")
            atualizar_nome_preco_estoque_produto(produto)
            return

def atualizar_nome_preco_estoque_produto(produto):
    novo_nome = input(f"\n>> Digite o novo nome: ")
    if not novo_nome.strip():
        print("\nEspaço em branco! Mantendo o nome anterior.\n")
        novo_nome = produto.nome
    novo_preco = entrar_float(f">> Digite o novo preço: ")
    nova_quantidade = entrar_int(f">> Nova quantidade em estoque: ")
    atualizar_produto_db(produto.id, novo_nome, nova_quantidade, novo_preco)
    print(f"\nProduto {novo_nome} atualizado com sucesso!\n")

def remover_produto():
    produtos = obter_todos_produtos_db()
    if not produtos:
        print("\nNenhum produto cadastrado.")
        return
    exibir_produtos()
    id_produto = entrar_int(">> Digite o ID do produto que deseja remover: ")
    produto = buscar_por_id_db(id_produto)
    if produto is None:
        print("\nProduto não encontrado. Tente novamente.\n")
        return
    if produto.itens and len(produto.itens) > 0:
        print("\nNão é possível remover este produto, pois ele já foi vendido em uma compra.")
        return
    confirmar_remocao_produto(produto)

def confirmar_remocao_produto(produto):
    confirmar = entrar_int_personalizado(f"\n>> Tem certeza que deseja remover o produto {produto.nome}? [1 - Sim / 2 - Não]: ", 1, 2)
    if confirmar == 1:
        remover_produto_db(produto)
        print(f"\nProduto {produto.nome} removido com sucesso.\n")
    else:
        print("\nRemoção de produto cancelada.\n")

def consultar_fornecedores_produto():
    produtos = obter_todos_produtos_db()
    if not produtos:
        print("\nNenhum produto cadastrado.")
        return
    produto = obter_produtos_valido()
    if produto is None:
        print("\nProduto não encontrado.\n")
        return
    fornecedores = obter_fornecedores_do_produto_db(produto.id)
    if not fornecedores:
        print(f"\nO produto {produto.nome} não possui fornecedores relacionados.\n")
        return
    exibir_fornecedores_produto(fornecedores, produto) 

def obter_produtos_valido():
    exibir_produtos()
    id_produto = entrar_int(">> Digite o ID do produto que deseja Consultar: ")
    produto = buscar_por_id_db(id_produto)
    return produto

def exibir_fornecedores_produto(fornecedores, produto):
    print(f"\nFornecedores do produto {produto.nome}:\n")
    for fornecedor in fornecedores:
        print(f"- {fornecedor.nome}")
    print("")

def produtos_mais_vendidos():
    top_produtos = produtos_mais_vendidos_db()
    if not top_produtos:
        print("\nNenhum produto vendido até o momento.\n")
        return
    exibir_produtos_mais_vendidos(top_produtos)

def exibir_produtos_mais_vendidos(produtos):
    print("\nProdutos mais vendidos:\n")
    for produto, total_vendido in produtos:
        print(f"- {produto.nome} | {total_vendido} unidades vendidas")
    print("")

def produtos_menos_vendidos():
    top_produtos = produtos_menos_vendidos_db()
    if not top_produtos:
        print("\nNenhum produto vendido até o momento.\n")
        return
    exibir_produtos_menos_vendidos(top_produtos)

def exibir_produtos_menos_vendidos(produtos):
    print("\nProdutos menos vendidos:\n")
    for produto, total_vendido in produtos:
        print(f"- {produto.nome} | {total_vendido} unidades vendidas")
    print("")

def produtos_com_pouco_estoque():
    limite = entrar_int("\n>> Digite um parâmetro para verificar produto com pouco estoque: ")
    produtos_acabando = produtos_com_pouco_estoque_db(limite)
    if not produtos_acabando:
        print("\nNenhum produto encontrado com pouco estoque.\n")
        return
    exibir_produtos_com_pouco_estoque(produtos_acabando)

def exibir_produtos_com_pouco_estoque(produtos):
    print("\nProdutos com pouco estoque:\n")
    for produto in produtos:
        print(f"- {produto.nome} | Estoque: {produto.quantidade}")
    print("")

def exibir_produtos():
    produtos = obter_todos_produtos_db()
    if produtos is None or len(produtos) == 0:
        print("\nNenhum produto cadastrado.")
        return
    print("\nProdutos cadastrados:\n")
    for produto in produtos:
        print(f"- ID {produto.id}: {produto.nome} | Preço: R${produto.preco:.2f} | Estoque: {produto.quantidade}")
    print("")