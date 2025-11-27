from caixa.caixa import inicializar_sistema_caixa
from sig.sig import inicializar_sistema_sig
from commons.utils.util import entrar_int_personalizado
from commons.menu.menu import menu_inicial_aplicacao

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
                break
            case _:
                raise ValueError("Opção inválida. Tente novamente.")
    except Exception as e:
        print(f"Erro inesperado ao iniciar o sistema: {e}")