from urllib.request import urlopen
import pandas as pd
from bs4 import BeautifulSoup
from caixa.web_scrapping.extracao_dados_crud import gerar_csv, armazenar_no_db

URL = "https://pedrovncs.github.io/lindosprecos/produtos.html#"

def acessar_url():
    try:
        html = urlopen(URL)
    except Exception as ex:
        print(ex)
        exit()
    return html

def obter_tabela(bs):
    tabela = bs.find_all("div", class_="product-item")
    if not tabela:
        print("Erro: tabela não encontrada")
        exit()
    return tabela

def extrair_dados(produto):
    nome = produto.find("h5", class_="card-title")["data-nome"]
    preco = limpar_preco(produto.find("p", class_="card-price")["data-preco"])
    quantidade = produto.find("p", {"data-qtd": True})["data-qtd"]
    return {"Nome": nome, "Preço": preco, "Quantidade": quantidade}

def limpar_preco(valor_str):
    valor_limpo = valor_str.replace("R$", "").replace("\xa0", "").replace(",", ".").strip()
    return float(valor_limpo)

def criar_dataframe(produtos):
    lista_dados = []
    for produto in produtos:
        dados_produtos = extrair_dados(produto)
        lista_dados.append(dados_produtos)
    df = pd.DataFrame(lista_dados)
    return df

def inicializar_extracao_dados():
    html = acessar_url()
    bs = BeautifulSoup(html, "html.parser")
    produtos = obter_tabela(bs)
    df = criar_dataframe(produtos)
    gerar_csv(df, "commons/data/produtos.csv")
    armazenar_no_db()