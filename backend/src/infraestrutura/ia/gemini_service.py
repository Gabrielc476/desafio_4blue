import os
import google.generativeai as genai
from typing import List, Dict
from dotenv import load_dotenv
from src.dominio.servicos.interface_servico_ia import InterfaceServicoIA

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

class GeminiService(InterfaceServicoIA):
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("AVISO CRÍTICO: GEMINI_API_KEY não encontrada no arquivo .env ou variáveis de ambiente.")
        else:
            genai.configure(api_key=api_key)

        # Configurações de geração para o Gemini Pro
        self.generation_config = {
            "temperature": 0.4, # Baixa temperatura para o Analista ser preciso
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 2048,
        }

    def gerar_resposta_agente(self, mensagem_usuario: str, historico_chat: List[Dict[str, str]], prompt_sistema: str) -> str:
        if not os.getenv("GEMINI_API_KEY"):
            return "Erro de Configuração: Chave de API da IA não encontrada. Por favor, configure o backend."

        try:
            # Instancia o modelo
            # OBS: Use "gemini-1.5-pro" para maior inteligência de raciocínio
            model = genai.GenerativeModel(
                model_name="gemini-2.5-flash",
                generation_config=self.generation_config,
                system_instruction=prompt_sistema
            )

            # Inicia o chat com o histórico fornecido
            chat = model.start_chat(history=historico_chat)

            # Envia a mensagem
            response = chat.send_message(mensagem_usuario)
            return response.text

        except Exception as e:
            print(f"Erro ao chamar API Gemini: {e}")
            return "Desculpe, estou tendo dificuldades técnicas para consultar minha base de conhecimento agora. Tente novamente em instantes."