import uuid
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class UsuarioMock:
    """
    Entidade de negócio que representa um usuário simulado no sistema.
    """
    identificador: str
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    criado_em: datetime = field(default_factory=datetime.now)

    def __str__(self) -> str:
        """
        Retorna a representação em string da entidade, que é o seu identificador.
        """
        return self.identificador
