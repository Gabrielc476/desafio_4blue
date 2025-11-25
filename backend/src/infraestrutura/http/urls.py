from django.urls import path
from src.infraestrutura.http.controladores.views import CriarInteracaoChatView, HistoricoChatView

urlpatterns = [
    # Rota para enviar mensagem (POST)
    path('mensagem/', CriarInteracaoChatView.as_view(), name='enviar_mensagem'),

    # Rota para pegar histórico (GET), ex: /api/chat/historico/A/
    path('historico/<str:identificador_usuario>/', HistoricoChatView.as_view(), name='historico_usuario'),
]