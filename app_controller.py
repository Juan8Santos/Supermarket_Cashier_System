from caixa.web_scrapping.extracao_dados import inicializar_extracao_dados
from caixa.crud_caixa.crud_caixa import carregar_mocki_clientes
from sig.data_extraction.data_extraction import inicializar_extracao_dados_sheets
from commons.menu.menu import menu_inicial_aplicacao
from commons.utils.util import entrar_int_personalizado
from caixa.caixa import inicializar_sistema_caixa
from sig.sig import inicializar_sistema_sig

class AppController:
    def start(self):
        inicializar_extracao_dados()
        carregar_mocki_clientes()
        inicializar_extracao_dados_sheets()
        self.loop_main()
            
    def restart_loop(self):
        self.loop_main()

    def loop_main(self):
        while True:
            menu_inicial_aplicacao()
            entrada = entrar_int_personalizado(">> Escolha uma opção: ", 1, 3)
            try:
                match entrada:
                    case 1:
                        print("")
                        inicializar_sistema_caixa()
                    case 2:
                        print("")
                        inicializar_sistema_sig()
                    case 3:
                        print("")
                        print("Encerrando do sistema...")
                        exit()
                    case _:
                        raise ValueError("Opção inválida. Tente novamente.")
            except Exception as e:
                print(f"Erro inesperado ao iniciar o sistema: {e}")