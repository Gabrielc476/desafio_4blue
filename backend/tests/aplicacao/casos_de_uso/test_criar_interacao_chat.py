import unittest

from src.dominio.entidades.usuario_mock import UsuarioMock
from src.aplicacao.casos_de_uso.criar_interacao_chat import CriarInteracaoChatCasoDeUso
from tests.aplicacao.mocks.repositorio_usuario_mock_em_memoria import RepositorioUsuarioMockEmMemoria
from tests.aplicacao.mocks.repositorio_interacao_chat_em_memoria import RepositorioInteracaoChatEmMemoria


class TestCriarInteracaoChatCasoDeUso(unittest.TestCase):
    """
    Testes para o caso de uso CriarInteracaoChat.
    """

    def setUp(self):
        """
        Configura os repositórios em memória antes de cada teste.
        """
        self.repositorio_usuario = RepositorioUsuarioMockEmMemoria()
        self.repositorio_interacao = RepositorioInteracaoChatEmMemoria()
        self.caso_de_uso = CriarInteracaoChatCasoDeUso(
            repositorio_usuario=self.repositorio_usuario,
            repositorio_interacao=self.repositorio_interacao,
        )

    def test_cria_interacao_para_novo_usuario(self):
        """
        Testa se o caso de uso cria um novo usuário se ele não existir
        e salva a interação corretamente.
        """
        identificador = "UsuarioC"
        mensagem = "Primeira mensagem"

        # Antes, não deve haver nenhum usuário
        self.assertEqual(len(self.repositorio_usuario.listar_todos()), 0)

        interacao_criada = self.caso_de_uso.executar(
            identificador_usuario=identificador,
            mensagem_usuario=mensagem
        )

        # Agora, deve haver um usuário e uma interação
        self.assertEqual(len(self.repositorio_usuario.listar_todos()), 1)
        self.assertEqual(len(self.repositorio_interacao.listar_todas()), 1)

        usuario_salvo = self.repositorio_usuario.buscar_por_identificador(identificador)
        self.assertIsNotNone(usuario_salvo)
        self.assertEqual(usuario_salvo.identificador, identificador)

        self.assertEqual(interacao_criada.usuario, usuario_salvo)
        self.assertEqual(interacao_criada.mensagem_usuario, mensagem)
        self.assertIn("Obrigado por seu contato", interacao_criada.resposta_bot)

    def test_cria_interacao_para_usuario_existente(self):
        """
        Testa se o caso de uso utiliza um usuário existente para criar
        uma nova interação.
        """
        # Pré-popula o repositório com um usuário
        usuario_existente = UsuarioMock(identificador="UsuarioA")
        self.repositorio_usuario.salvar(usuario_existente)

        mensagem = "Segunda mensagem"

        # Antes, deve haver um usuário e nenhuma interação
        self.assertEqual(len(self.repositorio_usuario.listar_todos()), 1)
        self.assertEqual(len(self.repositorio_interacao.listar_todas()), 0)

        interacao_criada = self.caso_de_uso.executar(
            identificador_usuario="UsuarioA",
            mensagem_usuario=mensagem
        )

        # Não deve criar um novo usuário
        self.assertEqual(len(self.repositorio_usuario.listar_todos()), 1)
        self.assertEqual(len(self.repositorio_interacao.listar_todas()), 1)

        self.assertEqual(interacao_criada.usuario.id, usuario_existente.id)
        self.assertEqual(interacao_criada.mensagem_usuario, mensagem)
        self.assertEqual(interacao_criada.resposta_bot, "Obrigado por seu contato, Usuário A. Em breve responderemos.")

if __name__ == '__main__':
    unittest.main()
