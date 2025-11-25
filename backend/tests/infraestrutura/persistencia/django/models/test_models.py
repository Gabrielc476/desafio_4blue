from django.test import TestCase
from src.infraestrutura.persistencia.django.models.usuario import MockUser
from src.infraestrutura.persistencia.django.models.interacao import ChatInteraction


class TestDjangoModels(TestCase):
    def test_criacao_mock_user(self):
        """Testa a criação básica de um MockUser no banco."""
        user = MockUser.objects.create(identifier="UsuarioTeste")

        self.assertIsNotNone(user.id)  # UUID deve ser gerado automaticamente
        self.assertIsNotNone(user.created_at)  # Data deve ser gerada automaticamente
        self.assertEqual(str(user), "UsuarioTeste")

    def test_mock_user_identifier_unico(self):
        """Testa se o identificador é único."""
        MockUser.objects.create(identifier="Unico")
        with self.assertRaises(Exception):  # Deve falhar ao tentar criar duplicado
            MockUser.objects.create(identifier="Unico")

    def test_criacao_chat_interaction(self):
        """Testa a criação de uma interação vinculada a um usuário."""
        user = MockUser.objects.create(identifier="UsuarioChat")
        interaction = ChatInteraction.objects.create(
            user=user,
            user_message="Olá",
            bot_response="Oi!"
        )

        self.assertEqual(interaction.user, user)
        self.assertIsNotNone(interaction.id)
        self.assertIsNotNone(interaction.created_at)
        # Verifica se o __str__ contém o identificador e a data (aproximadamente)
        self.assertIn("UsuarioChat", str(interaction))