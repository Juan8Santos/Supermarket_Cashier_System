from sig.menu_sig.menu_sig import exibir_menu_sig, menu_modulo_clientes_sig, menu_modulo_produtos_sig
from commons.utils.util import entrar_int_personalizado

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
    menu_modulo_clientes_sig()
    entrada = entrar_int_personalizado(">> Escolha uma opção: ", 1, 3)

def modulo_produtos_sig():
    menu_modulo_produtos_sig()
    entrada = entrar_int_personalizado(">> Escolha uma opção: ", 1, 8)