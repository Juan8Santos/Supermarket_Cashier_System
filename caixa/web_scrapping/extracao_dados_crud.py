import pandas as pd
from commons.crud_db.crud_db import armazenar_produtos_no_db

def gerar_csv(df, nome_arquivo):
    df.to_csv(nome_arquivo, index=False)

def armazenar_no_db():
    produto_csv = pd.read_csv("commons/data/produtos.csv", encoding="utf-8")
    armazenar_produtos_no_db(produto_csv)