from typing import List, Optional

from src.dominio.entidades.interacao_chat import InteracaoChat
from src.dominio.repositorios.interface_repositorio_usuario_mock import InterfaceRepositorioUsuarioMock
from src.dominio.repositorios.interface_repositorio_interacao_chat import InterfaceRepositorioInteracaoChat


class ObterHistoricoChatUsuarioCasoDeUso:
    """
    Caso de uso para obter o histórico de interações de chat de um usuário.
    """

    def __init__(
        self,
        repositorio_usuario: InterfaceRepositorioUsuarioMock,
        repositorio_interacao: InterfaceRepositorioInteracaoChat,
    ):
        self.repositorio_usuario = repositorio_usuario
        self.repositorio_interacao = repositorio_interacao

    def executar(self, identificador_usuario: str) -> Optional[List[InteracaoChat]]:
        """
        Executa o caso de uso.

        1. Busca o usuário pelo seu identificador.
        2. Se o usuário existir, busca todas as suas interações de chat.
        3. Retorna a lista de interações.

        :param identificador_usuario: O identificador do usuário (ex: "A" ou "B").
        :return: Uma lista de InteracaoChat ou None se o usuário não for encontrado.
        """
        usuario = self.repositorio_usuario.buscar_por_identificador(
            identificador_usuario
        )

        if not usuario:
            return None

        return self.repositorio_interacao.listar_por_id_usuario(usuario.id)
