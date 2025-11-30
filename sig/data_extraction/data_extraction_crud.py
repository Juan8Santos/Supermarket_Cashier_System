import pandas as pd

def gerar_df_fornecedores(url):
    df = pd.read_csv(url)
    return df