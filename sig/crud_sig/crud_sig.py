from sig.menu_sig.menu_sig import exibir_menu_sig, menu_modulo_clientes_sig, menu_modulo_produtos_sig, menu_clientes_com_compras
from commons.utils.util import entrar_int_personalizado, entrar_int
from commons.crud_db.crud_db import *
from tabulate import tabulate

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
                    print("")
                    print("Encerrando do sistema...")
                    exit()
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
                    print("")
                    print("Função de adicionar produto ainda não implementada.")
                case 2:
                    print("")
                    print("Função de listar produtos ainda não implementada.")
                case 3:
                    print("")
                    print("Função de atualizar produto ainda não implementada.")
                case 4:
                    print("")
                    print("Função de deletar produto ainda não implementada.")
                case 5:
                    print("")
                    print("Função de buscar produto por ID ainda não implementada.")
                case 6:
                    print("")
                    print("Função de verificar produtos sem estoque ainda não implementada.")
                case 7:
                    print("")
                    print("Função de reduzir estoque ainda não implementada.")
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

def formatar_historico_compras_cliente(cliente, compras):
    print(f"\nHistórico de compras do cliente {cliente.nome}:\n")
    for compra in compras:
        print(f"- Compra ID: {compra.id}, Data e Hora: {compra.data_hora}")
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
        compra_encontrada = next((caracter for caracter in compras if caracter.id == entrada), None)     
        if compra_encontrada:
            compra = consultar_compra_filtrado_por_cliente_e_compra__db(compra_encontrada.id, cliente.id_cliente)
            formatar_detalhes_compra_cliente(compra)
            break
        else:
            print("Compra não encontrada. Tente novamente.")

def formatar_detalhes_compra_cliente(compra):
    print(f"\nDetalhes da compra ID {compra.id} - Cliente: {compra.cliente.nome}")
    print(f"Data e Hora: {compra.data_hora}\n")
    tabela = []
    valor_total = 0
    for item in compra.itens:
        subtotal = item.quantidade * item.preco_unitario
        valor_total += subtotal
        tabela.append([
            item.produto.nome,
            item.quantidade,
            f"R${item.preco_unitario:.2f}",
            f"R${subtotal:.2f}"
        ])
    print(tabulate(tabela, headers=["Produto", "Quantidade", "Preço Unitário", "Subtotal"]))
    print(f"\nValor Total da Compra: R${valor_total:.2f}\n")

def clientes_com_mais_compras():
    print("Clientes que mais compram:")
    tabela_compras = consultar_clientes_com_mais_compras_db()
    for nome, compras in tabela_compras:
        print(f"- {nome}: {compras} compras")
    print("")

def clientes_que_mais_gastam():
    print("Clientes que mais gastam:")
    tabela_gastos = clientes_que_mais_gastam_db()
    for nome, total in tabela_gastos:
        print(f"- {nome}: R${total:.2f}")
    print("")

def listar_clientes_sem_compras():
    clientes = consultar_clientes_sem_compras_db()
    if not clientes:
        print("\nTodos os clientes possuem compras registradas.")
    else:
        print("\nClientes que não possuem compras:\n")
        for cliente in clientes:
            print(f"- Id {cliente.id_cliente}: {cliente.nome}")
    modulo_clientes_sig()

# ====== Funções 