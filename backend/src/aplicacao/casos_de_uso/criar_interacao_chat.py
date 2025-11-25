from typing import List, Dict

from src.dominio.entidades.usuario_mock import UsuarioMock
from src.dominio.entidades.interacao_chat import InteracaoChat
from src.dominio.repositorios.interface_repositorio_usuario_mock import InterfaceRepositorioUsuarioMock
from src.dominio.repositorios.interface_repositorio_interacao_chat import InterfaceRepositorioInteracaoChat
from src.dominio.servicos.interface_servico_ia import InterfaceServicoIA
from src.aplicacao.agentes.prompts import PROMPT_ANALISTA, PROMPT_CONSULTOR


class CriarInteracaoChatCasoDeUso:
    def __init__(
            self,
            repositorio_usuario: InterfaceRepositorioUsuarioMock,
            repositorio_interacao: InterfaceRepositorioInteracaoChat,
            servico_ia: InterfaceServicoIA
    ):
        self.repositorio_usuario = repositorio_usuario
        self.repositorio_interacao = repositorio_interacao
        self.servico_ia = servico_ia

    def executar(self, identificador_usuario: str, mensagem_usuario: str) -> InteracaoChat:
        # 1. Busca ou cria usuário
        usuario = self.repositorio_usuario.buscar_por_identificador(identificador_usuario)
        if not usuario:
            usuario = UsuarioMock(identificador=identificador_usuario)
            usuario = self.repositorio_usuario.salvar(usuario)

        # 2. Prepara o histórico (contexto)
        # Pegamos as últimas 10 interações para dar contexto sem gastar muitos tokens
        # O repositório retorna do mais antigo para o mais novo
        interacoes_antigas = self.repositorio_interacao.listar_por_id_usuario(usuario.id)
        # Pega as últimas 10
        interacoes_recentes = interacoes_antigas[-10:] if interacoes_antigas else []

        historico_formatado = self._formatar_historico_para_gemini(interacoes_recentes)

        # --- WORKFLOW DE AGENTES (CHAIN) ---

        # AGENTE 1: O ANALISTA (Raciocínio)
        # Ele recebe o histórico e a mensagem, mas não responde ao usuário diretamente.
        input_analista = f"Nova mensagem do usuário: {mensagem_usuario}"

        analise_tecnica = self.servico_ia.gerar_resposta_agente(
            mensagem_usuario=input_analista,
            historico_chat=historico_formatado,
            prompt_sistema=PROMPT_ANALISTA
        )

        # Log para debug (opcional, ajuda a ver o que a IA está pensando)
        print(
            f"--- ANÁLISE DO AGENTE ({identificador_usuario}) ---\n{analise_tecnica}\n-------------------------------")

        # AGENTE 2: O CONSULTOR (Resposta)
        # Ele recebe a mensagem original + a análise técnica do Agente 1
        prompt_com_contexto = f"""
        {PROMPT_CONSULTOR}

        --- INFORMAÇÃO DO ANALISTA INTERNO ---
        {analise_tecnica}
        """

        resposta_bot = self.servico_ia.gerar_resposta_agente(
            mensagem_usuario=mensagem_usuario,
            historico_chat=historico_formatado,  # O Consultor também precisa saber o histórico
            prompt_sistema=prompt_com_contexto
        )

        # 3. Salva a interação no banco
        nova_interacao = InteracaoChat(
            usuario=usuario,
            mensagem_usuario=mensagem_usuario,
            resposta_bot=resposta_bot,
        )

        return self.repositorio_interacao.salvar(nova_interacao)

    def _formatar_historico_para_gemini(self, interacoes: List[InteracaoChat]) -> List[Dict[str, str]]:
        """
        Converte as entidades do domínio para o formato esperado pela API do Google Generative AI.
        Formato: [{'role': 'user', 'parts': ['texto']}, {'role': 'model', 'parts': ['texto']}]
        """
        historico = []
        for interacao in interacoes:
            # Turno do Usuário
            historico.append({
                "role": "user",
                "parts": [interacao.mensagem_usuario]
            })
            # Turno do Modelo (Bot)
            historico.append({
                "role": "model",
                "parts": [interacao.resposta_bot]
            })
        return historico