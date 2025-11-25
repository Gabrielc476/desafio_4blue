import { useEffect, useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { ChatService } from '../services/api';
import type { InteracaoChat } from '../types/ChatTypes';
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

// 1. Componente Wrapper
export function HistoryPage() {
  const { usuarioAtivo } = useAuth();
  return <HistoryListContent key={usuarioAtivo} usuarioId={usuarioAtivo} />;
}

// 2. Componente de Conteúdo
function HistoryListContent({ usuarioId }: { usuarioId: string }) {
  const [historico, setHistorico] = useState<InteracaoChat[]>([]);
  const [carregando, setCarregando] = useState(true);

  useEffect(() => {
    ChatService.obterHistorico(usuarioId)
      .then(setHistorico)
      .finally(() => setCarregando(false));
  }, [usuarioId]);

  // Configuração comum para renderização do Markdown nas células
  const markdownComponents = {
    p: ({children}: any) => <p className="mb-1 last:mb-0">{children}</p>,
    ul: ({children}: any) => <ul className="list-disc pl-4 mb-1 space-y-0.5">{children}</ul>,
    ol: ({children}: any) => <ol className="list-decimal pl-4 mb-1 space-y-0.5">{children}</ol>,
    li: ({children}: any) => <li className="marker:text-gray-400">{children}</li>,
    a: ({href, children}: any) => (
      <a href={href} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">
        {children}
      </a>
    )
  };

  return (
    <div className="max-w-6xl mx-auto p-4 md:p-6">
      <Card>
        <CardHeader>
          <CardTitle>Histórico de Interações - {usuarioId}</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="rounded-md border">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead className="w-[140px]">Data/Hora</TableHead>
                  <TableHead className="w-[30%]">Sua Mensagem</TableHead>
                  <TableHead>Resposta do Consultor</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {carregando ? (
                  <TableRow>
                    <TableCell colSpan={3} className="h-24 text-center">
                      <div className="flex justify-center items-center gap-2 text-muted-foreground">
                        <span className="animate-spin">⏳</span> Carregando histórico...
                      </div>
                    </TableCell>
                  </TableRow>
                ) : historico.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={3} className="h-24 text-center text-gray-500">
                      Nenhum histórico encontrado para este usuário.
                    </TableCell>
                  </TableRow>
                ) : (
                  historico.map((item) => (
                    <TableRow key={item.id} className="align-top">
                      {/* Coluna Data */}
                      <TableCell className="font-mono text-xs text-gray-500 py-4 align-top">
                        {new Date(item.criado_em).toLocaleString([], {
                          day: '2-digit',
                          month: '2-digit',
                          hour: '2-digit',
                          minute: '2-digit'
                        })}
                      </TableCell>
                      
                      {/* Coluna Usuário */}
                      <TableCell className="py-4 align-top">
                         <div className="prose prose-sm max-w-none prose-p:text-blue-700 prose-strong:text-blue-900 leading-snug">
                            <ReactMarkdown 
                              remarkPlugins={[remarkGfm]}
                              components={markdownComponents}
                            >
                              {item.mensagem_usuario}
                            </ReactMarkdown>
                         </div>
                      </TableCell>

                      {/* Coluna Bot */}
                      <TableCell className="py-4 align-top">
                        <div className="prose prose-sm max-w-none prose-slate prose-p:text-gray-600 prose-headings:text-gray-700 leading-snug">
                          <ReactMarkdown 
                            remarkPlugins={[remarkGfm]}
                            components={markdownComponents}
                          >
                            {item.resposta_bot}
                          </ReactMarkdown>
                        </div>
                      </TableCell>
                    </TableRow>
                  ))
                )}
              </TableBody>
            </Table>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}