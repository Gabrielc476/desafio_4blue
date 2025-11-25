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

// 1. Componente Wrapper: Responsável apenas por pegar o usuário e passar a 'key'
export function HistoryPage() {
  const { usuarioAtivo } = useAuth();
  
  // O segredo está aqui: key={usuarioAtivo}.
  // Quando o usuário muda, o React "destrói" o componente antigo e cria um novo.
  // Isso reseta o estado automaticamente e evita o erro de cascade update.
  return <HistoryListContent key={usuarioAtivo} usuarioId={usuarioAtivo} />;
}

// 2. Componente de Conteúdo: Responsável pela lógica e exibição
function HistoryListContent({ usuarioId }: { usuarioId: string }) {
  const [historico, setHistorico] = useState<InteracaoChat[]>([]);
  
  // CORREÇÃO: Iniciamos como true. Não precisamos setar no useEffect.
  const [carregando, setCarregando] = useState(true); 

  useEffect(() => {
    // Apenas buscamos os dados. O estado de loading já começou verdadeiro.
    ChatService.obterHistorico(usuarioId)
      .then(setHistorico)
      .finally(() => setCarregando(false));
  }, [usuarioId]);

  return (
    <div className="max-w-4xl mx-auto p-6">
      <Card>
        <CardHeader>
          <CardTitle>Histórico de Interações - {usuarioId}</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="rounded-md border">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead className="w-[180px]">Data/Hora</TableHead>
                  <TableHead>Sua Mensagem</TableHead>
                  <TableHead>Resposta do Bot</TableHead>
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
                    <TableRow key={item.id}>
                      <TableCell className="font-medium text-xs text-gray-500">
                        {new Date(item.criado_em).toLocaleString([], {
                          day: '2-digit',
                          month: '2-digit',
                          hour: '2-digit',
                          minute: '2-digit'
                        })}
                      </TableCell>
                      <TableCell className="text-blue-700 font-medium">
                        {item.mensagem_usuario}
                      </TableCell>
                      <TableCell className="text-gray-600">
                        {item.resposta_bot}
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