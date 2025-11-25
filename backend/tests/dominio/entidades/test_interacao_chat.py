import unittest
import uuid
from datetime import datetime

from src.dominio.entidades.usuario_mock import UsuarioMock
from src.dominio.entidades.interacao_chat import InteracaoChat

class TestInteracaoChat(unittest.TestCase):
    """
    Testes para a entidade InteracaoChat.
    """

    def setUp(self):
        """
        Configura um usuário mock para ser usado nos testes de InteracaoChat.
        """
        self.usuario = UsuarioMock(identificador="UsuarioTeste")

    def test_criacao_interacao_chat(self):
        """
        Testa a criação de uma instância de InteracaoChat.
        """
        mensagem = "Olá, mundo!"
        resposta = "Olá! Como posso ajudar?"
        
        interacao = InteracaoChat(
            usuario=self.usuario,
            mensagem_usuario=mensagem,
            resposta_bot=resposta
        )

        self.assertEqual(interacao.usuario, self.usuario)
        self.assertEqual(interacao.mensagem_usuario, mensagem)
        self.assertEqual(interacao.resposta_bot, resposta)
        self.assertIsInstance(interacao.id, uuid.UUID)
        self.assertIsInstance(interacao.criado_em, datetime)

    def test_str_representation(self):
        """
        Testa a representação em string da entidade InteracaoChat.
        """
        interacao = InteracaoChat(
            usuario=self.usuario,
            mensagem_usuario="Teste",
            resposta_bot="Testado."
        )
        
        hora_formatada = interacao.criado_em.strftime('%Y-%m-%d %H:%M:%S')
        expected_str = f"{self.usuario.identificador} - {hora_formatada}"
        
        self.assertEqual(str(interacao), expected_str)

if __name__ == '__main__':
    unittest.main()
