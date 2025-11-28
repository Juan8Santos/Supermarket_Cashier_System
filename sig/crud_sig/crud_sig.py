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
    while True:
        menu_modulo_clientes_sig()
        entrada = entrar_int_personalizado(">> Escolha uma opção: ", 1, 3)
        try:
            match entrada:
                case 1:
                    print("")
                    print("Função de adicionar cliente ainda não implementada.")
                case 2:
                    print("")
                    print("Função de listar clientes ainda não implementada.")
                case 3:
                    print("")
                    dashboard_principal_sig()
                case _:
                    raise ValueError("Opção inválida. Tente novamente.")
        except Exception as e:
            print(f"Erro inesperado no módulo de clientes: {e}")

def modulo_produtos_sig():
    while True:
        menu_modulo_produtos_sig()
        entrada = entrar_int_personalizado(">> Escolha uma opção: ", 1, 8)
        try:
            match entrada:
                case 1:
                    print("")
                    print("Função de adicionar produto ainda não implementada.")
                case 2:
                    print("")
                    print("Função de listar produtos ainda não implementada.")
                case 3:
                    print("")
                    print("Função de atualizar produto ainda não implementada.")
                case 4:
                    print("")
                    print("Função de deletar produto ainda não implementada.")
                case 5:
                    print("")
                    print("Função de buscar produto por ID ainda não implementada.")
                case 6:
                    print("")
                    print("Função de verificar produtos sem estoque ainda não implementada.")
                case 7:
                    print("")
                    print("Função de reduzir estoque ainda não implementada.")
                case 8:
                    print("")
                    dashboard_principal_sig()
                case _:
                    raise ValueError("Opção inválida. Tente novamente.")
        except Exception as e:
            print(f"Erro inesperado no módulo de produtos: {e}")