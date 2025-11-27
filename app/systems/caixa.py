from app.crud.crud_caixa import decidir_abrir_caixa, carregar_mocki_clientes
from app.menu.menu import exibir_dashboard_abrir_caixa
from app.web_scrapping.extracao_dados import inicializar_extracao_dados

def inicializar_sistema_caixa():
    inicializar_extracao_dados()
    carregar_mocki_clientes()

    exibir_dashboard_abrir_caixa()
    decidir_abrir_caixa()