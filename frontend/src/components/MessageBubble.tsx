import { cn } from "@/lib/utils";

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
          "relative max-w-[80%] px-4 py-2 rounded-lg text-sm shadow-sm",
          isUser 
            ? "bg-blue-600 text-white rounded-br-none" 
            : "bg-gray-100 text-gray-800 rounded-bl-none",
          enviando && "opacity-70",
          erro && "bg-red-100 text-red-600 border border-red-300"
        )}
      >
        <p>{texto}</p>
        
        <div className={cn("text-[10px] mt-1 text-right", isUser ? "text-blue-100" : "text-gray-400")}>
           {enviando ? "Enviando..." : timestamp ? new Date(timestamp).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}) : ""}
        </div>
      </div>
    </div>
  );
}