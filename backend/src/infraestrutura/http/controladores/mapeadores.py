from rest_framework import serializers

class NovaInteracaoInputMapper(serializers.Serializer):
    """
    Mapeia os dados de entrada para criar uma nova mensagem.
    Esperado: {"identificador_usuario": "A", "mensagem_usuario": "Texto"}
    """
    identificador_usuario = serializers.CharField(max_length=50)
    mensagem_usuario = serializers.CharField()

class UsuarioOutputMapper(serializers.Serializer):
    """Mapeia os dados do usuário para resposta."""
    identificador = serializers.CharField()

class InteracaoOutputMapper(serializers.Serializer):
    """
    Mapeia a entidade InteracaoChat para JSON de resposta.
    """
    id = serializers.UUIDField()
    usuario = UsuarioOutputMapper()
    mensagem_usuario = serializers.CharField()
    resposta_bot = serializers.CharField()
    criado_em = serializers.DateTimeField()