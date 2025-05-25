from abc import ABC,abstractmethod
from src.module.usuario.abstractUsuario import Usuario
class Documento(ABC):
    @abstractmethod
    def __init__(self, ide: int, titulo: str, descricao: str, data_envio: str, autor: Usuario):
        self.__ide = ide
        self.__titulo = titulo
        self.__descricao = descricao
        self.__data_envio = data_envio
        self.__autor = autor

    @property
    def ide(self):
        return self.__ide
    @ide.setter
    def ide(self, nova_ide: int):
        if isinstance(nova_ide, int): self.__ide = nova_ide

    @property
    def titulo(self):
        return self.__titulo
    @titulo.setter
    def titulo(self, novo_titulo: str):
        if isinstance(novo_titulo, str): self.__titulo = novo_titulo

    @property
    def descricao(self):
        return self.__descricao
    @descricao.setter
    def descricao(self, nova_descricao: str):
        if isinstance(nova_descricao, str): self.__descricao = nova_descricao

    @property
    def data_envio(self):
        return self.__data_envio
    @data_envio.setter
    def data_envio(self, nova_data_envio: str):
        if isinstance(nova_data_envio, str): self.__data_envio = nova_data_envio

    @property
    def autor(self):
        return self.__autor
    @autor.setter
    def autor(self, novo_autor: Usuario):
        if isinstance(novo_autor, Usuario): self.__autor = novo_autor