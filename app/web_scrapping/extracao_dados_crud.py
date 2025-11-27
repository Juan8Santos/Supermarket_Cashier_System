from app.conexao import session
from app.models.models import Produto
import pandas as pd

def gerar_csv(df, nome_arquivo):
    df.to_csv(nome_arquivo, index=False)

def armazenar_no_db():
    produto_csv = pd.read_csv("app/data/produtos.csv", encoding="utf-8")
    with session:
        session.query(Produto).delete()
        session.commit()
        for _, linha in produto_csv.iterrows():
            produto = Produto(
                nome=linha['Nome'],
                quantidade=int(linha['Quantidade']),
                preco=float(linha['Preço'])
            )
            session.add(produto)
        session.commit()