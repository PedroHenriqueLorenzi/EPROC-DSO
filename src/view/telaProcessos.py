from datetime import datetime

class TelaProcessos:
    def mostrar_menu(self) -> int:
        print("\n=== MENU DE PROCESSOS ===")
        print("1 - Criar novo processo")
        print("2 - Listar processos")
        print("3 - Adicionar documento")
        print("4 - Encerrar processo")
        print("5 - Gerar relatório")
        print("0 - Voltar")
        try:
            return int(input("Escolha uma opção: "))
        except ValueError:
            return -1

    def mostrar_mensagem(self, mensagem: str):
        print(f">>> {mensagem}")

    def solicitar_numero_processo(self) -> int:
        while True:
            try:
                numero = int(input("Número do processo (inteiro): "))
                if numero >= 0:
                    return numero
                raise ValueError
            except ValueError:
                print("Número inválido. Digite um número inteiro positivo.")

    def solicitar_data_processo(self) -> str:
        while True:
            data = input("Data de abertura (AAAA-MM-DD): ").strip()
            try:
                datetime.strptime(data, "%Y-%m-%d")
                return data
            except ValueError:
                print("Data inválida. Use o formato correto: AAAA-MM-DD.")

    def solicitar_juiz(self, usuarios: list):
        juizes = [u for u in usuarios if u.__class__.__name__.lower() == "juiz"]
        if not juizes:
            self.mostrar_mensagem("Nenhum juiz cadastrado.")
            return None

        print("\n--- Selecionar Juiz Responsável ---")
        for j in juizes:
            print(f"{j.id} - {j.nome}")
        try:
            id_juiz = int(input("Digite o ID do juiz responsável: "))
            for j in juizes:
                if j.id == id_juiz:
                    return j
        except ValueError:
            pass
        return None

    def selecionar_tribunal(self, tribunais: list):
        print("\n--- Selecionar Tribunal ---")
        for t in tribunais:
            print(f"{t.id} - {t.nome} ({t.localidade})")
        try:
            id_escolhido = int(input("Digite o ID do tribunal: "))
            for t in tribunais:
                if t.id == id_escolhido:
                    return t
        except ValueError:
            pass
        return None

    def exibir_lista_processos(self, lista: list):
        print("\n--- Lista de Processos ---")
        if not lista:
            print("Nenhum processo encontrado.")
        for item in lista:
            print(item)

    def selecionar_numero_processo(self) -> int:
        try:
            return int(input("Digite o número do processo: "))
        except ValueError:
            return -1

    def confirmar(self, mensagem: str) -> bool:
        resposta = input(mensagem).strip().lower()
        return resposta == "s"

    def selecionar_usuarios_por_id(self, lista_usuarios, tipo):
        print(f"--- Seleção de {tipo.capitalize()}s ---")
        if not lista_usuarios:
            self.mostrar_mensagem(f"Nenhum {tipo} disponível.")
            return []

        for u in lista_usuarios:
            print(f"{u.id} - {u.nome} ({u.__class__.__name__})")

        try:
            ids = input("Digite os IDs separados por vírgula: ").split(",")
            ids = [int(i.strip()) for i in ids]
            return [u for u in lista_usuarios if u.id in ids]
        except ValueError:
            self.mostrar_mensagem("Entrada inválida.")
            return []

    def ler_dados_documento(self):
        print("\n--- Adicionar Documento ---")
        tipo = input("Tipo de documento (acusacao/defesa/audiencia/sentenca): ").strip().lower()

        try:
            id_doc = int(input("ID do documento: "))
        except ValueError:
            self.mostrar_mensagem("ID inválido.")
            return tipo, {}

        titulo = input("Título: ")
        descricao = input("Descrição: ")
        data_envio = input("Data de envio (AAAA-MM-DD): ")

        dados = {
            "id": id_doc,
            "titulo": titulo,
            "descricao": descricao,
            "data_envio": data_envio,
        }

        if tipo == "audiencia":
            data_audiencia = input("Data da audiência (AAAA-MM-DD): ")
            dados["data"] = data_audiencia

        return tipo, dados

    def mostrar_menu_relatorio(self) -> int:
        print("\n--- Relatórios Disponíveis ---")
        print("1 - Por status")
        print("2 - Por juiz")
        print("3 - Sem audiência")
        print("4 - Com sentença")
        print("0 - Voltar")
        try:
            return int(input("Escolha uma opção: "))
        except ValueError:
            return -1

    def solicitar_status(self) -> str:
        return input("Digite o status (Ativo/Encerrado): ")

    def solicitar_nome_juiz(self) -> str:
        return input("Digite o nome do juiz: ")

    def exibir_relatorio(self, linhas: list):
        print("\n--- RELATÓRIO ---")
        if not linhas:
            print("Nenhum dado encontrado.")
        for linha in linhas:
            print(linha)
    def solicitar_data(self, mensagem="Digite a data (AAAA-MM-DD): "):
        while True:
            data = input(mensagem).strip()
            try:
                from datetime import datetime
                datetime.strptime(data, "%Y-%m-%d")
                return data
            except ValueError:  
                print(">>> Data inválida. Use o formato correto: AAAA-MM-DD.")