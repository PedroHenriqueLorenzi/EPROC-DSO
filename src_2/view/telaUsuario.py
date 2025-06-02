
""" 
TelaUsuarios
------------
Responsável por:
- Interface com o usuário para entrada e saída de dados relacionados a usuários
- Nunca manipula diretamente objetos de domínio
"""

class TelaUsuarios:
    def mostrar_menu(self) -> int:
        print("\n--- MENU USUÁRIOS ---")
        print("1 - Incluir Usuário")
        print("2 - Remover Usuário")
        print("3 - Alterar Usuário")
        print("4 - Listar Todos os Usuários")
        print("5 - Listar Usuários por Tipo")
        print("0 - Voltar ao Menu Principal")
        try:
            return int(input("Escolha uma opção: "))
        except ValueError:
            return -1

    def mostrar_mensagem(self, mensagem: str):
        print(f">>> {mensagem}")

    def ler_dados_usuario(self) -> dict:
        print("\n--- Cadastro de Usuário ---")
        tipo = input("Tipo de usuário (advogado / juiz / reu / vitima): ").strip().lower()
        nome = input("Nome: ").strip()
        cpf = input("CPF: ").strip()
        data_nascimento = input("Data de nascimento (AAAA-MM-DD): ").strip()
        id = input("ID numérico: ").strip()

        dados = {
            "id": int(id),
            "nome": nome,
            "cpf": cpf,
            "data_nascimento": data_nascimento,
            "tipo": tipo
        }

        # Campos adicionais por tipo
        if tipo == "advogado":
            dados["oab"] = input("Número da OAB: ").strip()
        elif tipo == "juiz":
            dados["numero_funcional"] = input("Número funcional: ").strip()
            dados["tribunal_atribuido"] = input("Tribunal atribuído: ").strip()

        return dados

    def selecionar_usuario(self, lista_usuarios: list) -> int:
        print("\n--- Usuários Disponíveis ---")
        for usuario in lista_usuarios:
            print(f"{usuario.id()} - {usuario.nome()} ({type(usuario).__name__})")
        try:
            return int(input("Digite o ID do usuário: "))
        except ValueError:
            return -1

    def exibir_lista_usuarios(self, lista: list[str]):
        print("\n--- Lista de Usuários ---")
        if not lista:
            print("Nenhum usuário encontrado.")
        else:
            for item in lista:
                print(item)

    def selecionar_tipo_usuario(self) -> str:
        return input("Digite o tipo de usuário (advogado / juiz / reu / vitima): ").strip().lower()
