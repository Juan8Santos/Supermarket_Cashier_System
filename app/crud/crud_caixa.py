from app.utils.util import entrar_int_personalizado, entrar_int
from tabulate import tabulate
from datetime import datetime
from app.crud.crud_db import *
import pandas as pd

# ====== Funções para o Caixa ======

def decidir_abrir_caixa():
    vendas_do_dia = []
    entrada = entrar_int_personalizado("Digite uma das operações: ", 1, 2)
    if entrada == 1:
        cliente = solicitar_id_cliente()
        atender_cliente(vendas_do_dia, cliente)
    else:
        fechar_caixa(vendas_do_dia)

def atender_cliente(vendas_do_dia, cliente):
    sacola = []
    print(f"\n{cliente}")
    while True:
        print("\n* Digite o id do produto e a quantidade desejada.\n")
        id_produto = entrar_int("Digite o id do produto: ")
        quantidade = entrar_int("Digite a quantidade desejada: ")
        executar_operacao_caixa(sacola, id_produto, quantidade)
        continuar = entrar_int_personalizado("\nDeseja adicionar outro produto? [1] - Sim / [2] - Não: ", 1, 2)
        if continuar == 2:
            break
    finalizar_venda(sacola, cliente, vendas_do_dia)
    
def executar_operacao_caixa(sacola, id_produto, quantidade):
    try:
        produto = buscar_produto_por_id(id_produto)
        quantidade_produto = validar_quantidade_suficiente(id_produto, quantidade, sacola)
        sacola.append((produto, quantidade_produto))
        print(f"Produto {produto.nome} adicionado à sacola.")
    except ValueError as e:
        print(e)

def finalizar_venda(sacola, cliente, vendas_do_dia):
    if len(sacola) > 0:
        reduzir_estoque(sacola)
        total = sum([produto.preco * quantidade for produto, quantidade in sacola])
        vendas_do_dia.append({"cliente": cliente, "total": total})
        gerar_boleto(sacola, cliente)
        decidir_fechar_caixa(vendas_do_dia)
    else:
        print("Nenhum produto na sacola. Venda cancelada.")
        decidir_fechar_caixa(vendas_do_dia)

def decidir_fechar_caixa(vendas_do_dia):
    entrada = entrar_int_personalizado("\nDeseja atender o próximo cliente? [1] - Atender Cliente / [2] - Fechar Caixa: ", 1, 2)
    if entrada == 1:
        cliente = solicitar_id_cliente()
        atender_cliente(vendas_do_dia, cliente)
    else:
        fechar_caixa(vendas_do_dia)

def gerar_df_boleto(sacola):
    dados = [{"produto": produto.nome, "quantidade": quantidade, "preco": produto.preco} for produto, quantidade in sacola]
    df = pd.DataFrame(dados)
    df["total"] = df["quantidade"] * df["preco"]
    df_group = df.groupby(["produto", "preco"], as_index=False).agg({"quantidade": "sum", "total": "sum" })
    return df_group

def gerar_boleto(sacola, cliente):
    df_group = gerar_df_boleto(sacola)
    print(f"\nCliente {cliente}")
    print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")    
    print(tabulate(df_group, headers=["Item", "Produto", "Preço", "Quant.", "Total"]))
    print(f"\nItens diferentes: {len(df_group)}")
    print(f"Total geral: R${df_group['total'].sum():.2f}")

def fechar_caixa(vendas_do_dia):
    tabela = [[vendas['cliente'], f"R${vendas['total']:.2f}"] for vendas in vendas_do_dia]
    print("\nFechamento do caixa")
    print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
    print(tabulate(tabela, headers=["Cliente", "Total"]))
    print(f"\nTotal de vendas: R${sum(vendas['total'] for vendas in vendas_do_dia):.2f}\n")
    verificar_sem_estoque()
    exit()

# ====== Funções para Produtos ======

def reduzir_estoque(sacola):
    for produto, quantidade in sacola:
        reduzir_estoque_db(produto.id, quantidade)

def buscar_produto_por_id(id_produto):
    produto = buscar_por_id_db(id_produto)
    if not produto:
        raise ValueError("Produto não encontrado.")
    else:
        return produto

def validar_quantidade_suficiente(id_produto, quantidade, sacola):
    verificacao_quantidade_total = 0
    quantidade_estoque = buscar_quantidade_por_id_db(id_produto)
    for produto_sacola, quantidade_sacola in sacola:
        if produto_sacola.id == id_produto:
            verificacao_quantidade_total += quantidade_sacola
    if (verificacao_quantidade_total + quantidade) > quantidade_estoque:
        raise ValueError("Quantidade indisponível no estoque.")
    else:
        return quantidade

def verificar_sem_estoque():
    sem_estoque = verificar_sem_estoque_db()
    if not sem_estoque:
        print("* Nenhum produto sem estoque.")
    else:
        print("* Produtos sem estoque:")
        for produto in sem_estoque:
            print(f"- {produto.nome}")

# ====== Funções para Clientes ======

def procurar_cliente(id_cliente):
    cliente = procurar_cliente_db(id_cliente)
    if cliente is not None:
        return True
    else:
        return False
    
def armazenar_cliente(nome_cliente, id):
    novo_cliente = armazenar_cliente_db(nome_cliente, id)
    if novo_cliente:
        print(f"Cliente {nome_cliente} registrado com sucesso.")
    return novo_cliente

def registrar_cliente():
    print("\nCliente não encontrado. Registrando novo cliente.\n")
    while True:
        nome_cliente = input("Digite o nome do cliente [Cliente ID]: ")
        if procurar_nome_cliente_db(nome_cliente) is not None:
            print("\nErro! Cliente já registrado. Tente novamente.\n")
        elif verificar_formatacao_nome_cliente(nome_cliente):
            break
        else:
            print("\nErro! Nome inválido. Tente novamente.\n")
    id = extrair_id_cliente(nome_cliente)
    cliente = armazenar_cliente(nome_cliente.capitalize(), id)
    return cliente

def solicitar_id_cliente():
    id_cliente = entrar_int("\nDigite o ID do cliente: ")
    cliente_existe = procurar_cliente(id_cliente)
    if cliente_existe:
        cliente = obter_nome_cliente_db(id_cliente)
    else:
        cliente = registrar_cliente()
    return cliente

def extrair_id_cliente(nome_cliente):
    id_cliente = ""
    for char in nome_cliente:
        if char.isdigit():
            id_cliente += char
    return int(id_cliente)

def verificar_formatacao_nome_cliente(nome_cliente):
    partes = nome_cliente.strip().split()   
    if len(partes) == 2 and partes[0] == "Cliente" and partes[1].isdigit():
        return True
    else:
        return False

def carregar_mocki_clientes():
    clientes_para_mocki = pd.read_json("app/data/clientes.json")
    qtd_clientes = contar_clientes_db()
    if qtd_clientes == 0:
        carregar_mocki_clientes_db(clientes_para_mocki)