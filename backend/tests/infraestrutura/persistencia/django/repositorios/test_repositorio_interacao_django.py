from django.test import TestCase
from src.dominio.entidades.usuario_mock import UsuarioMock
from src.dominio.entidades.interacao_chat import InteracaoChat
from src.infraestrutura.persistencia.django.repositorios.repositorio_interacao_django import \
    RepositorioInteracaoChatDjango
from src.infraestrutura.persistencia.django.models.usuario import MockUser
from src.infraestrutura.persistencia.django.models.interacao import ChatInteraction


class TestRepositorioInteracaoChatDjango(TestCase):

    def setUp(self):
        self.repo = RepositorioInteracaoChatDjango()
        # Cria um usuário base para os testes
        self.usuario = UsuarioMock(identificador="UsuarioInteracao")

    def test_salvar_interacao(self):
        """Testa se salva uma interação e cria o usuário se necessário."""
        interacao = InteracaoChat(
            usuario=self.usuario,
            mensagem_usuario="Teste Msg",
            resposta_bot="Teste Bot"
        )

        salvo = self.repo.salvar(interacao)

        # Verifica retorno
        self.assertIsInstance(salvo, InteracaoChat)
        self.assertEqual(salvo.mensagem_usuario, "Teste Msg")

        # Verifica persistência no banco
        self.assertTrue(ChatInteraction.objects.filter(user_message="Teste Msg").exists())
        # Verifica se o usuário também foi salvo (cascade/create logic)
        self.assertTrue(MockUser.objects.filter(identifier="UsuarioInteracao").exists())

    def test_listar_por_id_usuario(self):
        """Testa a recuperação do histórico ordenado."""
        # 1. Salva o usuário no banco primeiro
        user_model = MockUser.objects.create(id=self.usuario.id, identifier=self.usuario.identificador)

        # 2. Cria interações diretamente no banco para controlar a ordem/tempo
        ChatInteraction.objects.create(user=user_model, user_message="Primeira", bot_response="R1")
        ChatInteraction.objects.create(user=user_model, user_message="Segunda", bot_response="R2")

        # 3. Cria interação de OUTRO usuário (não deve aparecer na lista)
        outro_user = MockUser.objects.create(identifier="Outro")
        ChatInteraction.objects.create(user=outro_user, user_message="Intrusa", bot_response="R3")

        # Ação
        historico = self.repo.listar_por_id_usuario(self.usuario.id)

        # Asserções
        self.assertEqual(len(historico), 2)
        self.assertEqual(historico[0].mensagem_usuario, "Primeira")
        self.assertEqual(historico[1].mensagem_usuario, "Segunda")
        # Garante que a mensagem do outro usuário não veio
        mensagens = [i.mensagem_usuario for i in historico]
        self.assertNotIn("Intrusa", mensagens)