class TelaSistema:
    def mostrar_menu(self) -> int:
        print("\n=== SISTEMA MINI-EPROC ===")
        print("1 - Gerenciar Usuários")
        print("2 - Gerenciar Processos")
        print("0 - Sair")
        try:
            return int(input("Escolha uma opção: "))
        except ValueError:
            return -1

    def mostrar_mensagem(self, mensagem: str):
        print(f">>> {mensagem}")

    def solicitar_id_usuario(self) -> int:
        try:
            return int(input("Digite o ID do usuário que deseja utilizar no sistema: "))
        except ValueError:
            return -1
