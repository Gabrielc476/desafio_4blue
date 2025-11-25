from typing import List
from uuid import UUID

from src.dominio.entidades.interacao_chat import InteracaoChat
from src.dominio.repositorios.interface_repositorio_interacao_chat import InterfaceRepositorioInteracaoChat
from src.infraestrutura.persistencia.django.models.interacao import ChatInteraction
from src.infraestrutura.persistencia.django.models.usuario import MockUser
from src.infraestrutura.persistencia.django.repositorios.repositorio_usuario_django import RepositorioUsuarioMockDjango


class RepositorioInteracaoChatDjango(InterfaceRepositorioInteracaoChat):

    def salvar(self, interacao: InteracaoChat) -> InteracaoChat:
        # Precisamos garantir que o usuário existe no banco Django antes de salvar a interação
        # Como o ID é o mesmo, podemos buscar pelo ID.
        try:
            usuario_django = MockUser.objects.get(id=interacao.usuario.id)
        except MockUser.DoesNotExist:
            # Em teoria o caso de uso já salvou o usuário, mas por segurança:
            usuario_django = MockUser.objects.create(
                id=interacao.usuario.id,
                identifier=interacao.usuario.identificador
            )

        interacao_django = ChatInteraction.objects.create(
            id=interacao.id,
            user=usuario_django,
            user_message=interacao.mensagem_usuario,
            bot_response=interacao.resposta_bot,
            # criado_em é auto_now_add no Django, então deixamos o banco definir ou forçamos se necessário.
            # Se quisermos manter a consistência exata com a entidade:
            created_at=interacao.criado_em
        )

        return self._para_entidade(interacao_django)

    def listar_por_id_usuario(self, usuario_id: UUID) -> List[InteracaoChat]:
        interacoes_django = ChatInteraction.objects.filter(user__id=usuario_id).order_by('created_at')
        return [self._para_entidade(i) for i in interacoes_django]

    def _para_entidade(self, interacao_django: ChatInteraction) -> InteracaoChat:
        """Helper para converter Model Django -> Entidade de Domínio"""

        # Reutilizamos o helper do outro repositório para converter o usuário
        repo_usuario_helper = RepositorioUsuarioMockDjango()
        usuario_entidade = repo_usuario_helper._para_entidade(interacao_django.user)

        return InteracaoChat(
            usuario=usuario_entidade,
            mensagem_usuario=interacao_django.user_message,
            resposta_bot=interacao_django.bot_response,
            id=interacao_django.id,
            criado_em=interacao_django.created_at
        )