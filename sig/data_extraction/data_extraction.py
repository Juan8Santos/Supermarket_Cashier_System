from commons.crud_db.crud_db import armazenar_fornecedores_no_db, armazenar_produtos_fornecedores_no_db
from sig.data_extraction.data_extraction_crud import gerar_df_fornecedores

def inicializar_extracao_dados_sheets():
    url_fornecedores = "https://docs.google.com/spreadsheets/d/1wEPglDR5EYFLmM206ZHffsjBC9L9K5hz_qiA8NSgzCw/export?format=csv"
    url_produtos_fornecedores = "https://docs.google.com/spreadsheets/d/1wEPglDR5EYFLmM206ZHffsjBC9L9K5hz_qiA8NSgzCw/export?format=csv&gid=493927295"

    df_fornecedores = gerar_df_fornecedores(url_fornecedores)
    df_produtos_fornecedores = gerar_df_fornecedores(url_produtos_fornecedores)
    armazenar_fornecedores_no_db(df_fornecedores)
    armazenar_produtos_fornecedores_no_db(df_produtos_fornecedores)
