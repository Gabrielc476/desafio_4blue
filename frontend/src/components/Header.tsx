import { Link, useLocation } from 'react-router-dom'; // Adicionei useLocation para destacar o ativo
import { useAuth } from '../contexts/AuthContext';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Button } from "@/components/ui/button";

export function Header() {
  const { usuarioAtivo, setUsuarioAtivo } = useAuth();
  const location = useLocation(); // Para saber em qual página estamos

  // Função auxiliar para destacar o botão da página atual
  const getVariant = (path: string) => {
    return location.pathname === path ? "secondary" : "ghost";
  };

  return (
    <header className="flex items-center justify-between p-4 border-b bg-white shadow-sm h-16">
      <div className="flex items-center gap-2">
        {/* Título ou Logo (opcional, mas fica bonito) */}
        <div className="font-bold text-xl mr-4 text-blue-600">4Blue Chat</div>

        {/* Botões corrigidos: variant="ghost" remove o fundo preto */}
        <Link to="/">
          <Button variant={getVariant('/')} className="font-medium">
            Chat
          </Button>
        </Link>
        <Link to="/historico">
          <Button variant={getVariant('/historico')} className="font-medium">
            Histórico
          </Button>
        </Link>
      </div>
      
      <div className="flex items-center gap-3">
        <span className="text-sm text-muted-foreground hidden sm:inline">
          Atendendo como:
        </span>
        <Select value={usuarioAtivo} onValueChange={setUsuarioAtivo}>
          <SelectTrigger className="w-[180px] bg-white">
            <SelectValue placeholder="Selecione o usuário" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="UsuarioA">Usuário A</SelectItem>
            <SelectItem value="UsuarioB">Usuário B</SelectItem>
          </SelectContent>
        </Select>
      </div>
    </header>
  );
}