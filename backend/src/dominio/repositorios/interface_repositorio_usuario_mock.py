from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from src.dominio.entidades.usuario_mock import UsuarioMock

class InterfaceRepositorioUsuarioMock(ABC):
    """
    Interface que define o contrato para repositórios de UsuarioMock.
    """

    @abstractmethod
    def salvar(self, usuario: UsuarioMock) -> UsuarioMock:
        """
        Salva uma instância de UsuarioMock no repositório.

        :param usuario: A instância de UsuarioMock a ser salva.
        :return: A instância de UsuarioMock salva.
        """
        raise NotImplementedError

    @abstractmethod
    def buscar_por_identificador(self, identificador: str) -> Optional[UsuarioMock]:
        """
        Busca um UsuarioMock pelo seu identificador único.

        :param identificador: O identificador do usuário a ser buscado.
        :return: Uma instância de UsuarioMock se encontrado, senão None.
        """
        raise NotImplementedError

    @abstractmethod
    def buscar_por_id(self, id: UUID) -> Optional[UsuarioMock]:
        """
        Busca um UsuarioMock pelo seu ID.

        :param id: O ID do usuário a ser buscado.
        :return: Uma instância de UsuarioMock se encontrado, senão None.
        """
        raise NotImplementedError
