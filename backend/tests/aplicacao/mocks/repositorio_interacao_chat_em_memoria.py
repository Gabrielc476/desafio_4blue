from typing import Dict, List
from uuid import UUID

from src.dominio.entidades.interacao_chat import InteracaoChat
from src.dominio.repositorios.interface_repositorio_interacao_chat import InterfaceRepositorioInteracaoChat


class RepositorioInteracaoChatEmMemoria(InterfaceRepositorioInteracaoChat):
    """
    Implementação em memória do repositório de interações de chat para testes.
    """

    def __init__(self):
        self._interacoes: Dict[UUID, InteracaoChat] = {}

    def salvar(self, interacao: InteracaoChat) -> InteracaoChat:
        self._interacoes[interacao.id] = interacao
        return interacao

    def listar_por_id_usuario(self, usuario_id: UUID) -> List[InteracaoChat]:
        interacoes_usuario = [
            interacao
            for interacao in self._interacoes.values()
            if interacao.usuario.id == usuario_id
        ]
        return sorted(interacoes_usuario, key=lambda i: i.criado_em)

    def listar_todas(self) -> List[InteracaoChat]:
        return list(self._interacoes.values())
