from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Importações dos Casos de Uso
from src.aplicacao.casos_de_uso.criar_interacao_chat import CriarInteracaoChatCasoDeUso
from src.aplicacao.casos_de_uso.obter_historico_chat_usuario import ObterHistoricoChatUsuarioCasoDeUso

# Importações dos Repositórios Concretos (Django)
from src.infraestrutura.persistencia.django.repositorios.repositorio_usuario_django import RepositorioUsuarioMockDjango
from src.infraestrutura.persistencia.django.repositorios.repositorio_interacao_django import \
    RepositorioInteracaoChatDjango

# Importação do Serviço de IA
from src.infraestrutura.ia.gemini_service import GeminiService

# Importações dos Mapeadores
from .mapeadores import NovaInteracaoInputMapper, InteracaoOutputMapper


class CriarInteracaoChatView(APIView):
    """
    Controlador para receber mensagens do chat.
    POST /api/chat/mensagem/
    """

    def post(self, request):
        # 1. Validar entrada com o Mapeador
        mapper_entrada = NovaInteracaoInputMapper(data=request.data)
        if not mapper_entrada.is_valid():
            return Response(mapper_entrada.errors, status=status.HTTP_400_BAD_REQUEST)

        dados = mapper_entrada.validated_data

        # 2. Injeção de Dependência
        repo_usuario = RepositorioUsuarioMockDjango()
        repo_interacao = RepositorioInteracaoChatDjango()

        # Instanciamos o Serviço de IA Real
        servico_ia = GeminiService()

        caso_de_uso = CriarInteracaoChatCasoDeUso(
            repositorio_usuario=repo_usuario,
            repositorio_interacao=repo_interacao,
            servico_ia=servico_ia
        )

        # 3. Execução da Lógica de Negócio
        try:
            interacao_criada = caso_de_uso.executar(
                identificador_usuario=dados['identificador_usuario'],
                mensagem_usuario=dados['mensagem_usuario']
            )

            # 4. Converter resultado para JSON
            mapper_saida = InteracaoOutputMapper(interacao_criada)
            return Response(mapper_saida.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            # Captura erros gerais (ex: falha na API da IA) para não quebrar o frontend
            print(f"Erro no processamento: {e}")
            return Response(
                {"erro": "Ocorreu um erro ao processar sua mensagem."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class HistoricoChatView(APIView):
    """
    Controlador para obter histórico.
    GET /api/chat/historico/<identificador_usuario>/
    """

    def get(self, request, identificador_usuario):
        # 1. Injeção de Dependência
        repo_usuario = RepositorioUsuarioMockDjango()
        repo_interacao = RepositorioInteracaoChatDjango()

        caso_de_uso = ObterHistoricoChatUsuarioCasoDeUso(
            repositorio_usuario=repo_usuario,
            repositorio_interacao=repo_interacao,
        )

        # 2. Execução
        historico = caso_de_uso.executar(identificador_usuario=identificador_usuario)

        # 3. Tratamento de Erro (Usuário não encontrado)
        if historico is None:
            return Response(
                {"erro": f"Usuário '{identificador_usuario}' não encontrado ou sem histórico."},
                status=status.HTTP_404_NOT_FOUND
            )

        # 4. Resposta
        mapper_saida = InteracaoOutputMapper(historico, many=True)
        return Response(mapper_saida.data, status=status.HTTP_200_OK)