from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from src.dominio.entidades.interacao_chat import InteracaoChat

class InterfaceRepositorioInteracaoChat(ABC):
    """
    Interface que define o contrato para repositórios de InteracaoChat.
    """

    @abstractmethod
    def salvar(self, interacao: InteracaoChat) -> InteracaoChat:
        """
        Salva uma instância de InteracaoChat no repositório.

        :param interacao: A instância de InteracaoChat a ser salva.
        :return: A instância de InteracaoChat salva.
        """
        raise NotImplementedError

    @abstractmethod
    def listar_por_id_usuario(self, usuario_id: UUID) -> List[InteracaoChat]:
        """
        Lista todas as interações de chat para um determinado ID de usuário.

        :param usuario_id: O ID do usuário para o qual buscar as interações.
        :return: Uma lista de instâncias de InteracaoChat.
        """
        raise NotImplementedError
