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

    def ler_dados_usuario(self, tribunais=None) -> dict:
        print("\n--- Cadastro de Usuário ---")
        try:
            id_usuario = int(input("ID: "))
        except ValueError:
            id_usuario = -1
        nome = input("Nome: ")
        cpf = input("CPF: ")
        data_nascimento = input("Data de nascimento (AAAA-MM-DD): ")
        tipo = input("Tipo (juiz/advogado/vitima/reu): ").lower()

        dados = {
            "id": id_usuario,
            "nome": nome,
            "cpf": cpf,
            "data_nascimento": data_nascimento,
            "tipo": tipo
        }

        if tipo == "juiz" and tribunais:
            print("\nTribunais disponíveis:")
            for t in tribunais:
                print(f"{t.id} - {t.nome} ({t.localidade})")
            try:
                id_tribunal = int(input("Escolha o ID do tribunal atribuído ao juiz: "))
                for t in tribunais:
                    if t.id == id_tribunal:
                        dados["tribunal_atribuido"] = t
                        break
                else:
                    print("Tribunal não encontrado. Juiz não será cadastrado.")
                    return {}
            except ValueError:
                print("Entrada inválida.")
                return {}

        return dados

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