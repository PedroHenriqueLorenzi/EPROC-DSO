from abc import ABC,abstractmethod
from system.module.usuario.abstractUsuario import Usuario
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
    def ide(self, ide: int):
        if isinstance(ide, int): self.__ide = ide

    @property
    def titulo(self):
        return self.__titulo
    
    @titulo.setter
    def titulo(self, titulo: int):
        self.__titulo = titulo

    @property
    def descricao(self):
        return self.__descricao
    
    @descricao.setter
    def descricao(self, descricao: int):
        self.__descricao = descricao

    @property
    def data_envio(self):
        return self.__data_envio
    
    @data_envio.setter
    def data_envio(self, data_envio: int):
        self.__data_envio = data_envio

    @property
    def autor(self):
        return self.__autor
    
