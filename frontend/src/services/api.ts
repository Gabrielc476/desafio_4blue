import axios from 'axios';
// CORREÇÃO: Adicionado 'type' na importação
import type { InteracaoChat, NovaMensagemPayload } from '../types/ChatTypes';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/chat',
});

export const ChatService = {
  obterHistorico: async (usuarioId: string): Promise<InteracaoChat[]> => {
    const response = await api.get<InteracaoChat[]>(`/historico/${usuarioId}/`);
    return response.data;
  },

  enviarMensagem: async (payload: NovaMensagemPayload): Promise<InteracaoChat> => {
    const response = await api.post<InteracaoChat>('/mensagem/', payload);
    return response.data;
  },
};