from module.documento.acusacao import Acusacao
from module.documento.defesa import Defesa
from module.documento.audiencia import Audiencia
from module.documento.sentenca import Sentenca
from module.usuario.juiz import Juiz
from module.usuario.advogado import Advogado
from view.telaDocumentos import TelaDocumentos

class ControladorDocumentos:
    def __init__(self):
        self.__tela_documentos = TelaDocumentos()

    def abrir_tela_documento(self, usuario_logado, processo, lista_usuarios):
        tipo = self.__tela_documentos.mostrar_menu_documentos()
        if not tipo:
            print(">>> Operação cancelada.")
            return

        dados_basicos = self.__tela_documentos.solicitar_dados_basicos()
        if not dados_basicos:
            print(">>> Falha ao obter dados básicos.")
            return

        dados_extra = self.__tela_documentos.solicitar_dados_extra(tipo, processo, processo.advogados)

        if dados_extra is None:
            print(">>> Falha ao obter dados específicos.")
            return

        dados_doc = {**dados_basicos, **dados_extra}

        try:
            documento = self.criar_documento(tipo, dados_doc, usuario_logado, processo)
            processo.adicionar_documento(documento)
            self.__controlador_processos.get_processo_dao().update(processo.numero, processo)
            print(f">>> {tipo.capitalize()} adicionada ao processo.")
        except (PermissionError, ValueError) as e:
            print(f">>> Erro: {str(e)}")

    def criar_documento(self, tipo, dados_doc, usuario_logado, processo):
        doc = None

        if tipo == "sentenca":
            if not isinstance(usuario_logado, Juiz):
                raise PermissionError("Apenas juízes podem emitir sentenças.")
            if "reu" not in dados_doc or "vitima" not in dados_doc:
                raise ValueError("Sentenças exigem réu e vítima.")
            doc = Sentenca(
                id=dados_doc["id"],
                titulo=dados_doc["titulo"],
                descricao=dados_doc["descricao"],
                data_envio=dados_doc["data_envio"],
                autor=usuario_logado,
                reu=dados_doc["reu"],
                vitima=dados_doc["vitima"]
            )

        elif tipo == "acusacao":
            if not isinstance(usuario_logado, Advogado):
                raise PermissionError("Apenas advogados podem criar acusações.")
            if "vitima" not in dados_doc:
                raise ValueError("Acusações exigem uma vítima.")
            doc = Acusacao(
                id=dados_doc["id"],
                titulo=dados_doc["titulo"],
                descricao=dados_doc["descricao"],
                data_envio=dados_doc["data_envio"],
                autor=usuario_logado,
                vitima=dados_doc["vitima"]
            )

        elif tipo == "defesa":
            if not isinstance(usuario_logado, Advogado):
                raise PermissionError("Apenas advogados podem criar defesas.")
            if "reu" not in dados_doc:
                raise ValueError("Defesas exigem um réu.")
            doc = Defesa(
                id=dados_doc["id"],
                titulo=dados_doc["titulo"],
                descricao=dados_doc["descricao"],
                data_envio=dados_doc["data_envio"],
                autor=usuario_logado,
                reu=dados_doc["reu"]
            )

        elif tipo == "audiencia":
            if not isinstance(usuario_logado, Juiz):
                raise PermissionError("Apenas juízes podem agendar audiências.")
            if "data_audiencia" not in dados_doc or "advogado" not in dados_doc:
                raise ValueError("Audiências exigem data e advogado responsável.")
            doc = Audiencia(
                id=dados_doc["id"],
                titulo=dados_doc["titulo"],
                descricao=dados_doc["descricao"],
                data_envio=dados_doc["data_envio"],
                autor=dados_doc["advogado"],
                juiz_responsavel=usuario_logado,
                data=dados_doc["data_audiencia"]
            )

        elif tipo == "arquivamento":
            raise PermissionError("Arquivamento é criado automaticamente ao encerrar o processo.")

        else:
            raise ValueError("Tipo de documento inválido.")

        return doc

    def get_proximo_id(self, processo):
        if not processo.documentos:
            return 1
        return max(doc.id for doc in processo.documentos) + 1