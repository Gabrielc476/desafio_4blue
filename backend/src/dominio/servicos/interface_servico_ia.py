from abc import ABC, abstractmethod
from typing import List, Dict

class InterfaceServicoIA(ABC):
    @abstractmethod
    def gerar_resposta_agente(self, mensagem_usuario: str, historico_chat: List[Dict[str, str]], prompt_sistema: str) -> str:
        """
        Gera uma resposta usando um modelo de IA com contexto e instrução específica.

        :param mensagem_usuario: A mensagem atual ou instrução combinada.
        :param historico_chat: Lista de dicionários [{'role': 'user', 'parts': ['...']}, ...].
        :param prompt_sistema: A instrução (persona) do agente.
        :return: O texto gerado pela IA.
        """
        raise NotImplementedError