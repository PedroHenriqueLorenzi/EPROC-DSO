class TelaUsuarios:
    def mostrar_menu(self) -> int:
        print("\n=== MENU DE USUÁRIOS ===")
        print("1 - Cadastrar novo usuário")
        print("2 - Listar todos os usuários")
        print("3 - Listar por tipo")
        print("4 - Remover usuário")
        print("0 - Voltar")
        try:
            return int(input("Escolha uma opção: "))
        except ValueError:
            return -1

    def mostrar_mensagem(self, mensagem: str):
        print(f">>> {mensagem}")

    def ler_dados_usuario(self, usuarios: list, tribunais: list) -> dict:
        print("\n--- Cadastro de Usuário ---")

        while True:
            try:
                id_usuario = int(input("ID (número inteiro): "))
                if any(u.id == id_usuario for u in usuarios):
                    print(">>> ID já cadastrado. Tente novamente.")
                    continue
                break
            except ValueError:
                print(">>> ID inválido. Digite um número inteiro.")

        while True:
            cpf = input("CPF (apenas números): ").strip()
            if not cpf.isdigit():
                print(">>> CPF deve conter apenas números.")
                continue
            if any(u.cpf == int(cpf) for u in usuarios):
                print(">>> CPF já cadastrado. Tente novamente.")
                continue
            break

        nome = input("Nome: ")

        while True:
            data = input("Data de nascimento (AAAA-MM-DD): ").strip()
            try:
                from datetime import datetime
                datetime.strptime(data, "%Y-%m-%d")
                break
            except ValueError:
                print(">>> Data inválida. Use o formato correto: AAAA-MM-DD.")

        tipo = input("Tipo (juiz/advogado/vitima/reu): ").strip().lower()

        return {
            "id": id_usuario,
            "nome": nome,
            "cpf": int(cpf),
            "data_nascimento": data,
            "tipo": tipo
        }

    def exibir_usuarios(self, lista: list):
        print("\n--- Lista de Usuários ---")
        if not lista:
            print("Nenhum usuário encontrado.")
        for item in lista:
            print(item)

    def solicitar_tipo(self) -> str:
        return input("Digite o tipo de usuário (juiz/advogado/vitima/reu): ")

    def solicitar_id(self) -> int:
        try:
            return int(input("Digite o ID do usuário: "))
        except ValueError:
            return -1
    def selecionar_tribunal(self, tribunais: list):
        print("\nTribunais disponíveis:")
        for t in tribunais:
            print(f"{t.id} - {t.nome} ({t.localidade})")
        try:
            id_tribunal = int(input("Escolha o ID do tribunal atribuído ao juiz: "))
            for t in tribunais:
                if t.id == id_tribunal:
                    return t
        except ValueError:
            pass
        return None
