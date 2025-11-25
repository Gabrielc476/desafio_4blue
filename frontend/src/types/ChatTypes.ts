export interface Usuario {
  identificador: string;
}

export interface InteracaoChat {
  id: string;
  usuario: Usuario;
  mensagem_usuario: string;
  resposta_bot: string;
  criado_em: string;
  
  // Controle de UI (Otimista)
  enviando?: boolean;
  erro?: boolean;
}

export interface NovaMensagemPayload {
  identificador_usuario: string;
  mensagem_usuario: string;
}