from typing import Optional
from uuid import UUID

from src.dominio.entidades.usuario_mock import UsuarioMock
from src.dominio.repositorios.interface_repositorio_usuario_mock import InterfaceRepositorioUsuarioMock
from src.infraestrutura.persistencia.django.models.usuario import MockUser


class RepositorioUsuarioMockDjango(InterfaceRepositorioUsuarioMock):

    def salvar(self, usuario: UsuarioMock) -> UsuarioMock:
        # Converte Entidade -> Model Django
        usuario_django, created = MockUser.objects.update_or_create(
            id=usuario.id,
            defaults={
                'identifier': usuario.identificador
            }
        )
        # Retorna a Entidade (garantindo que estamos devolvendo o objeto de domínio)
        return self._para_entidade(usuario_django)

    def buscar_por_identificador(self, identificador: str) -> Optional[UsuarioMock]:
        try:
            usuario_django = MockUser.objects.get(identifier=identificador)
            return self._para_entidade(usuario_django)
        except MockUser.DoesNotExist:
            return None

    def buscar_por_id(self, id: UUID) -> Optional[UsuarioMock]:
        try:
            usuario_django = MockUser.objects.get(id=id)
            return self._para_entidade(usuario_django)
        except MockUser.DoesNotExist:
            return None

    def _para_entidade(self, usuario_django: MockUser) -> UsuarioMock:
        """Helper para converter Model Django -> Entidade de Domínio"""
        return UsuarioMock(
            identificador=usuario_django.identifier,
            id=usuario_django.id,
            criado_em=usuario_django.created_at
        )