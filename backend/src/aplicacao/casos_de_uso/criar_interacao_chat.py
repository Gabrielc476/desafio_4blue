from typing import Dict, Any

from src.dominio.entidades.usuario_mock import UsuarioMock
from src.dominio.entidades.interacao_chat import InteracaoChat
from src.dominio.repositorios.interface_repositorio_usuario_mock import InterfaceRepositorioUsuarioMock
from src.dominio.repositorios.interface_repositorio_interacao_chat import InterfaceRepositorioInteracaoChat


class CriarInteracaoChatCasoDeUso:
    """
    Caso de uso para criar uma nova interação de chat.
    """

    def __init__(
        self,
        repositorio_usuario: InterfaceRepositorioUsuarioMock,
        repositorio_interacao: InterfaceRepositorioInteracaoChat,
    ):
        self.repositorio_usuario = repositorio_usuario
        self.repositorio_interacao = repositorio_interacao

    def executar(self, identificador_usuario: str, mensagem_usuario: str) -> InteracaoChat:
        """
        Executa o caso de uso.

        1. Busca o usuário pelo identificador. Se não existir, cria um novo.
        2. Gera uma resposta mockada para o bot.
        3. Cria a entidade InteracaoChat.
        4. Salva a interação no repositório.
        5. Retorna a interação criada.

        :param identificador_usuario: O identificador do usuário (ex: "A" ou "B").
        :param mensagem_usuario: A mensagem enviada pelo usuário.
        :return: A entidade InteracaoChat criada e salva.
        """
        usuario = self.repositorio_usuario.buscar_por_identificador(identificador_usuario)
        if not usuario:
            usuario = UsuarioMock(identificador=identificador_usuario)
            usuario = self.repositorio_usuario.salvar(usuario)

        resposta_bot = self._gerar_resposta_mockada(usuario)

        nova_interacao = InteracaoChat(
            usuario=usuario,
            mensagem_usuario=mensagem_usuario,
            resposta_bot=resposta_bot,
        )

        interacao_salva = self.repositorio_interacao.salvar(nova_interacao)

        return interacao_salva

    def _gerar_resposta_mockada(self, usuario: UsuarioMock) -> str:
        """
        Gera uma resposta simulada baseada no usuário.
        """
        respostas = {
            "UsuarioA": "Obrigado por seu contato, Usuário A. Em breve responderemos.",
            "UsuarioB": "Olá, Usuário B! Seu contato é muito importante para nós.",
        }
        # Retorna uma resposta padrão se o identificador não for A ou B
        return respostas.get(
            usuario.identificador, "Obrigado por seu contato. Em breve responderemos."
        )
