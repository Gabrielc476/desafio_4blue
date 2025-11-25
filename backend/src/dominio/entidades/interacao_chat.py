import uuid
from dataclasses import dataclass, field
from datetime import datetime
from .usuario_mock import UsuarioMock

@dataclass
class InteracaoChat:
    """
    Entidade de negócio que representa uma interação de chat completa,
    incluindo a mensagem do usuário e a resposta do bot.
    """
    usuario: UsuarioMock
    mensagem_usuario: str
    resposta_bot: str
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    criado_em: datetime = field(default_factory=datetime.now)

    def __str__(self) -> str:
        """
        Retorna uma representação em string da interação de chat.
        Ex: "Usuário A - 2025-11-23 15:45:00"
        """
        hora_formatada = self.criado_em.strftime('%Y-%m-%d %H:%M:%S')
        return f"{self.usuario.identificador} - {hora_formatada}"
