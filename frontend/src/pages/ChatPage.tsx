import { useRef, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useChat } from '../hooks/useChat';
import { ChatInput } from '../components/ChatInput';
import { MessageBubble } from '../components/MessageBubble';
import { ScrollArea } from "@/components/ui/scroll-area";
import { Card } from "@/components/ui/card";

export function ChatPage() {
  const { usuarioAtivo } = useAuth();
  const { mensagens, enviarMensagem } = useChat(usuarioAtivo);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [mensagens]);

  return (
    <div className="flex flex-col h-[calc(100vh-64px)] w-full p-4">
      <Card className="flex flex-col h-full overflow-hidden shadow-lg border-t-4 border-t-blue-600">
        <div className="bg-white p-4 border-b flex justify-between items-center">
          <div>
            <h2 className="font-semibold text-lg">Chat Suporte</h2>
            <p className="text-xs text-gray-500">Conectado como <span className="font-medium text-blue-600">{usuarioAtivo}</span></p>
          </div>
          <div className="h-2 w-2 rounded-full bg-green-500 animate-pulse" title="Online"></div>
        </div>

        <ScrollArea className="flex-1 p-6 bg-slate-50/50">
          {mensagens.length === 0 && (
            <div className="flex flex-col items-center justify-center h-full text-gray-400 space-y-2 opacity-50 mt-20">
              <div className="w-16 h-16 bg-gray-200 rounded-full flex items-center justify-center">
                💬
              </div>
              <p>Nenhuma mensagem ainda.</p>
              <p className="text-sm">Comece a conversa enviando um "Olá"!</p>
            </div>
          )}

          <div className="space-y-4">
            {mensagens.map((msg) => (
              <div key={msg.id} className="flex flex-col gap-1">
                <MessageBubble 
                  texto={msg.mensagem_usuario} 
                  isUser={true} 
                  timestamp={msg.criado_em}
                  enviando={msg.enviando}
                  erro={msg.erro}
                />
                
                {msg.resposta_bot && (
                  <MessageBubble 
                    texto={msg.resposta_bot} 
                    isUser={false} 
                    timestamp={msg.criado_em} 
                  />
                )}
              </div>
            ))}
          </div>
          <div ref={scrollRef} className="pb-4" />
        </ScrollArea>

        <ChatInput onSend={enviarMensagem} />
      </Card>
    </div>
  );
}