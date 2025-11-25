import unittest
import uuid
from datetime import datetime

from src.dominio.entidades.usuario_mock import UsuarioMock

class TestUsuarioMock(unittest.TestCase):
    """
    Testes para a entidade UsuarioMock.
    """

    def test_criacao_usuario_mock(self):
        """
        Testa a criação de uma instância de UsuarioMock com valores padrão.
        """
        identificador = "UsuarioA"
        usuario = UsuarioMock(identificador=identificador)

        self.assertEqual(usuario.identificador, identificador)
        self.assertIsInstance(usuario.id, uuid.UUID)
        self.assertIsInstance(usuario.criado_em, datetime)

    def test_str_representation(self):
        """
        Testa a representação em string da entidade UsuarioMock.
        """
        identificador = "UsuarioB"
        usuario = UsuarioMock(identificador=identificador)
        
        self.assertEqual(str(usuario), identificador)

if __name__ == '__main__':
    unittest.main()
