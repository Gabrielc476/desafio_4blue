import { useState, useEffect } from 'react';
import { v4 as uuidv4 } from 'uuid';
import { ChatService } from '../services/api';
import type { InteracaoChat } from '../types/ChatTypes';

export const useChat = (usuarioAtivo: string) => {
  const [mensagens, setMensagens] = useState<InteracaoChat[]>([]);
  const [carregando, setCarregando] = useState(false);

  // 1. Carregar histórico ao trocar de usuário
  useEffect(() => {
    const carregarHistorico = async () => {
      setCarregando(true);
      try {
        const historico = await ChatService.obterHistorico(usuarioAtivo);
        setMensagens(historico);
      } catch (error) {
        console.error("Erro ao carregar histórico", error);
        setMensagens([]); 
      } finally {
        setCarregando(false);
      }
    };

    carregarHistorico();
  }, [usuarioAtivo]);

  // 2. Envio Otimista
  const enviarMensagem = async (texto: string) => {
    if (!texto.trim()) return;

    // Cria mensagem temporária
    const idTemporario = uuidv4();
    const mensagemTemporaria: InteracaoChat = {
      id: idTemporario,
      usuario: { identificador: usuarioAtivo },
      mensagem_usuario: texto,
      resposta_bot: "", 
      criado_em: new Date().toISOString(),
      enviando: true,
    };

    // Atualiza a tela imediatamente
    setMensagens((prev) => [...prev, mensagemTemporaria]);

    try {
      const respostaReal = await ChatService.enviarMensagem({
        identificador_usuario: usuarioAtivo,
        mensagem_usuario: texto,
      });

      // Substitui a fake pela real
      setMensagens((prev) =>
        prev.map((msg) => (msg.id === idTemporario ? respostaReal : msg))
      );
    } catch (error) {
      console.error("Erro ao enviar", error);
      // Marca como erro
      setMensagens((prev) =>
        prev.map((msg) =>
          msg.id === idTemporario ? { ...msg, enviando: false, erro: true } : msg
        )
      );
    }
  };

  return { mensagens, carregando, enviarMensagem };
};