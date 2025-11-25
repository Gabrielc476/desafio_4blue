import { cn } from "@/lib/utils";
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

interface MessageBubbleProps {
  texto: string;
  isUser: boolean;
  timestamp?: string;
  enviando?: boolean;
  erro?: boolean;
}

export function MessageBubble({ texto, isUser, timestamp, enviando, erro }: MessageBubbleProps) {
  return (
    <div className={cn("flex w-full mt-2 mb-2", isUser ? "justify-end" : "justify-start")}>
      <div
        className={cn(
          "relative max-w-[85%] px-4 py-3 rounded-lg text-sm shadow-sm overflow-hidden", // Aumentei um pouco o padding e max-w
          isUser 
            ? "bg-blue-600 text-white rounded-br-none" 
            : "bg-white text-gray-800 rounded-bl-none border border-gray-100",
          enviando && "opacity-70",
          erro && "bg-red-50 text-red-600 border border-red-200"
        )}
      >
        {/* Renderização de Markdown */}
        <div className={cn(
          "prose prose-sm max-w-none break-words leading-relaxed", // Classes base de tipografia
          
          // Estilos específicos para quando é o BOT (fundo claro)
          !isUser && "prose-slate prose-p:text-gray-700 prose-strong:text-gray-900 prose-headings:text-gray-900",
          
          // Estilos específicos para quando é o USUÁRIO (fundo escuro - inverte as cores)
          isUser && "prose-invert prose-p:text-blue-50 prose-strong:text-white prose-headings:text-white"
        )}>
          <ReactMarkdown 
            remarkPlugins={[remarkGfm]}
            components={{
              // Removemos a margem extra do primeiro e último elemento para caber melhor no balão
              p: ({children}) => <p className="mb-2 last:mb-0">{children}</p>,
              ul: ({children}) => <ul className="list-disc pl-4 mb-2 last:mb-0 space-y-1">{children}</ul>,
              ol: ({children}) => <ol className="list-decimal pl-4 mb-2 last:mb-0 space-y-1">{children}</ol>,
              li: ({children}) => <li className="marker:text-current">{children}</li>,
              a: ({href, children}) => (
                <a 
                  href={href} 
                  target="_blank" 
                  rel="noopener noreferrer" 
                  className={isUser ? "text-blue-200 hover:text-white underline" : "text-blue-600 hover:text-blue-800 underline"}
                >
                  {children}
                </a>
              )
            }}
          >
            {texto}
          </ReactMarkdown>
        </div>
        
        <div className={cn(
          "text-[10px] mt-1 text-right select-none", 
          isUser ? "text-blue-200" : "text-gray-400"
        )}>
           {enviando ? "Enviando..." : timestamp ? new Date(timestamp).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}) : ""}
        </div>
      </div>
    </div>
  );
}