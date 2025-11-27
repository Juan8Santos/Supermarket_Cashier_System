# ====== Menus caixa ======

def exibir_dashboard_abrir_caixa():
    print("\n====== Caixa SuperMercado ======")
    print("[1] - Abrir Caixa")
    print("[2] - Fechar Caixa")

# ====== Menus SIG ======

def exibir_dashboard_sig():
    print("="*40)
    print(" "*2 + "Sistema de Informação Gerencial (SIG)")
    print("="*40)

    print("\033[92m[1]\033[0m Clientes")
    print("\033[92m[2]\033[0m Produtos")
    print("\033[92m[3]\033[0m Caixa")
    print("\033[92m[4]\033[0m Estoque")
    print("\033[92m[5]\033[0m Relatórios")
    print("\033[92m[6]\033[0m Sair")

    print("-"*40)
    return input("Escolha uma opção: ")