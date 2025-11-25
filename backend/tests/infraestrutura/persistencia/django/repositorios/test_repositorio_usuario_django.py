from django.test import TestCase
from src.dominio.entidades.usuario_mock import UsuarioMock
from src.infraestrutura.persistencia.django.repositorios.repositorio_usuario_django import RepositorioUsuarioMockDjango
from src.infraestrutura.persistencia.django.models.usuario import MockUser


class TestRepositorioUsuarioMockDjango(TestCase):

    def setUp(self):
        self.repo = RepositorioUsuarioMockDjango()

    def test_salvar_usuario_novo(self):
        """Testa se salva uma entidade UsuarioMock corretamente no banco."""
        usuario_entidade = UsuarioMock(identificador="NovoUsuario")

        # Executa o método do repositório
        salvo = self.repo.salvar(usuario_entidade)

        # Verifica retorno
        self.assertIsInstance(salvo, UsuarioMock)
        self.assertEqual(salvo.identificador, "NovoUsuario")

        # Verifica se realmente persistiu no banco Django
        self.assertTrue(MockUser.objects.filter(identifier="NovoUsuario").exists())

    def test_buscar_por_identificador_existente(self):
        """Testa a busca de um usuário que existe no banco."""
        # Cria direto no banco para simular dado existente
        MockUser.objects.create(identifier="BuscaTeste")

        # Busca pelo repositório
        usuario = self.repo.buscar_por_identificador("BuscaTeste")

        self.assertIsNotNone(usuario)
        self.assertIsInstance(usuario, UsuarioMock)
        self.assertEqual(usuario.identificador, "BuscaTeste")

    def test_buscar_por_identificador_inexistente(self):
        """Testa a busca de um usuário que não existe."""
        usuario = self.repo.buscar_por_identificador("NaoExiste")
        self.assertIsNone(usuario)