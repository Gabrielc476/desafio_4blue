from typing import Dict, Optional, List
from uuid import UUID

from src.dominio.entidades.usuario_mock import UsuarioMock
from src.dominio.repositorios.interface_repositorio_usuario_mock import InterfaceRepositorioUsuarioMock


class RepositorioUsuarioMockEmMemoria(InterfaceRepositorioUsuarioMock):
    """
    Implementação em memória do repositório de usuários para testes.
    """

    def __init__(self):
        self._usuarios: Dict[UUID, UsuarioMock] = {}

    def salvar(self, usuario: UsuarioMock) -> UsuarioMock:
        self._usuarios[usuario.id] = usuario
        return usuario

    def buscar_por_identificador(self, identificador: str) -> Optional[UsuarioMock]:
        for usuario in self._usuarios.values():
            if usuario.identificador == identificador:
                return usuario
        return None

    def buscar_por_id(self, id: UUID) -> Optional[UsuarioMock]:
        return self._usuarios.get(id)

    def listar_todos(self) -> List[UsuarioMock]:
        return list(self._usuarios.values())
