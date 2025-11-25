import unittest

from src.dominio.entidades.usuario_mock import UsuarioMock
from src.dominio.entidades.interacao_chat import InteracaoChat
from src.aplicacao.casos_de_uso.obter_historico_chat_usuario import ObterHistoricoChatUsuarioCasoDeUso
from tests.aplicacao.mocks.repositorio_usuario_mock_em_memoria import RepositorioUsuarioMockEmMemoria
from tests.aplicacao.mocks.repositorio_interacao_chat_em_memoria import RepositorioInteracaoChatEmMemoria


class TestObterHistoricoChatUsuarioCasoDeUso(unittest.TestCase):
    """
    Testes para o caso de uso ObterHistoricoChatUsuario.
    """

    def setUp(self):
        """
        Configura os repositórios em memória e o caso de uso.
        """
        self.repositorio_usuario = RepositorioUsuarioMockEmMemoria()
        self.repositorio_interacao = RepositorioInteracaoChatEmMemoria()
        self.caso_de_uso = ObterHistoricoChatUsuarioCasoDeUso(
            repositorio_usuario=self.repositorio_usuario,
            repositorio_interacao=self.repositorio_interacao,
        )

        # Pré-popula os repositórios com dados de teste
        self.usuario_a = UsuarioMock(identificador="UsuarioA")
        self.usuario_b = UsuarioMock(identificador="UsuarioB")
        self.repositorio_usuario.salvar(self.usuario_a)
        self.repositorio_usuario.salvar(self.usuario_b)

        self.interacao1_a = InteracaoChat(usuario=self.usuario_a, mensagem_usuario="Oi", resposta_bot="Olá A")
        self.interacao2_a = InteracaoChat(usuario=self.usuario_a, mensagem_usuario="Tudo bem?", resposta_bot="Tudo sim.")
        self.interacao1_b = InteracaoChat(usuario=self.usuario_b, mensagem_usuario="E aí?", resposta_bot="E aí B!")
        
        self.repositorio_interacao.salvar(self.interacao1_a)
        self.repositorio_interacao.salvar(self.interacao2_a)
        self.repositorio_interacao.salvar(self.interacao1_b)

    def test_retorna_historico_para_usuario_existente(self):
        """
        Testa se o caso de uso retorna a lista correta de interações
        para um usuário que possui histórico.
        """
        historico = self.caso_de_uso.executar(identificador_usuario="UsuarioA")
        
        self.assertIsNotNone(historico)
        self.assertEqual(len(historico), 2)
        self.assertIn(self.interacao1_a, historico)
        self.assertIn(self.interacao2_a, historico)
        self.assertNotIn(self.interacao1_b, historico)

    def test_retorna_lista_vazia_para_usuario_sem_historico(self):
        """
        Testa se o caso de uso retorna uma lista vazia para um usuário
        que existe mas não possui interações.
        """
        usuario_c = UsuarioMock(identificador="UsuarioC")
        self.repositorio_usuario.salvar(usuario_c)

        historico = self.caso_de_uso.executar(identificador_usuario="UsuarioC")
        
        self.assertIsNotNone(historico)
        self.assertEqual(len(historico), 0)

    def test_retorna_none_para_usuario_inexistente(self):
        """
        Testa se o caso de uso retorna None quando o identificador
        do usuário não corresponde a nenhum usuário no repositório.
        """
        historico = self.caso_de_uso.executar(identificador_usuario="UsuarioX")
        
        self.assertIsNone(historico)

if __name__ == '__main__':
    unittest.main()
