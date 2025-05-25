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

        while True:
            try:
                id_usuario = int(input("ID (número inteiro): "))
                if id_usuario < 0:
                    raise ValueError
                break
            except ValueError:
                print("ID inválido. Digite um número inteiro positivo.")

        while True:
            nome = input("Nome: ").strip()
            if nome.replace(" ", "").isalpha():
                break
            print("Nome deve conter apenas letras.")

        while True:
            cpf = input("CPF (apenas números): ").strip()
            if cpf.isdigit():
                break
            print("CPF deve conter apenas números.")

        while True:
            data_nascimento = input("Data de nascimento (AAAA-MM-DD): ").strip()
            try:
                from datetime import datetime
                datetime.strptime(data_nascimento, "%Y-%m-%d")
                break
            except ValueError:
                print("Data inválida. Use o formato correto: AAAA-MM-DD.")

        while True:
            tipo = input("Tipo (juiz/advogado/vitima/reu): ").lower()
            if tipo in ["juiz", "advogado", "vitima", "reu"]:
                break
            print("Tipo inválido. Escolha entre: juiz, advogado, vitima, reu.")

        dados = {
            "id": id_usuario,
            "nome": nome,
            "cpf": int(cpf),
            "data_nascimento": data_nascimento,
            "tipo": tipo
        }

        if tipo == "juiz" and tribunais:
            print("\nTribunais disponíveis:")
            for t in tribunais:
                print(f"{t.id} - {t.nome} ({t.localidade})")
            while True:
                try:
                    id_tribunal = int(input("Escolha o ID do tribunal atribuído ao juiz: "))
                    for t in tribunais:
                        if t.id == id_tribunal:
                            dados["tribunal_atribuido"] = t
                            return dados
                    print("Tribunal não encontrado.")
                except ValueError:
                    print("Entrada inválida. Digite um número.")
        if tipo == "advogado":
            while True:
                oab = input("Número da OAB: ").strip()
                if oab.isdigit():
                    dados["oab"] = int(oab)
                    break
                print("OAB deve conter apenas números.")

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