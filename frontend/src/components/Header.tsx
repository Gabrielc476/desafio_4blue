import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { Button } from "@/components/ui/button";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Check, ChevronDown, User, Briefcase, MessageSquare } from "lucide-react";

export function Header() {
  const { usuarioAtivo, setUsuarioAtivo } = useAuth();
  const location = useLocation();

  const getVariant = (path: string) => {
    return location.pathname === path ? "default" : "ghost";
  };

  const getUserData = (id: string) => {
    if (id === 'UsuarioA') return { 
        initial: 'UA', 
        name: 'Usuário A', 
        role: 'Comércio',
        color: 'bg-blue-600',
        icon: User
    };
    return { 
        initial: 'UB', 
        name: 'Usuário B', 
        role: 'Serviços',
        color: 'bg-emerald-600',
        icon: Briefcase
    };
  };

  const currentUser = getUserData(usuarioAtivo);

  return (
    // Adicionado z-50 para garantir que o header fique acima de outros elementos
    <header className="sticky top-0 z-50 w-full border-b bg-white/95 backdrop-blur supports-[backdrop-filter]:bg-white/60">
      <div className="flex h-16 items-center justify-between px-4 w-full">
        
        {/* Lado Esquerdo: Marca e Navegação */}
        <div className="flex items-center gap-6">
          <div className="flex items-center gap-2">
            <div className="bg-primary/10 p-2 rounded-lg">
              <MessageSquare className="h-5 w-5 text-primary" />
            </div>
            <span className="font-bold text-lg tracking-tight hidden md:inline-block">4Blue Chat</span>
          </div>

          <nav className="flex items-center gap-1 bg-slate-100/50 p-1 rounded-lg border border-slate-200/50">
            <Link to="/">
              <Button 
                variant={getVariant('/')} 
                size="sm" 
                className="h-8 text-xs font-medium rounded-md px-4 transition-all"
              >
                Chat
              </Button>
            </Link>
            <Link to="/historico">
              <Button 
                variant={getVariant('/historico')} 
                size="sm" 
                className="h-8 text-xs font-medium rounded-md px-4 transition-all"
              >
                Histórico
              </Button>
            </Link>
          </nav>
        </div>
        
        {/* Lado Direito: Seletor de Perfil */}
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="outline" className="h-10 pl-2 pr-4 gap-3 rounded-full border-slate-200 hover:bg-slate-50 hover:text-slate-900 data-[state=open]:bg-slate-50 transition-all bg-white">
              <Avatar className="h-7 w-7">
                <AvatarFallback className={`${currentUser.color} text-white text-[10px] font-bold`}>
                  {currentUser.initial}
                </AvatarFallback>
              </Avatar>
              <div className="flex flex-col items-start hidden sm:flex">
                <span className="text-xs font-semibold leading-none">{currentUser.name}</span>
                <span className="text-[10px] text-muted-foreground">{currentUser.role}</span>
              </div>
              <ChevronDown className="h-3 w-3 text-muted-foreground opacity-50" />
            </Button>
          </DropdownMenuTrigger>
          
          {/* CORREÇÃO AQUI: 
             - bg-white: Garante fundo sólido (não transparente)
             - z-50: Garante que fique no topo da pilha (acima do chat)
             - shadow-xl: Sombra forte para destacar do fundo
             - border: Borda sutil
          */}
          <DropdownMenuContent className="w-64 p-2 bg-white z-50 shadow-xl border border-slate-200 rounded-xl" align="end" sideOffset={5}>
            <DropdownMenuLabel className="font-normal px-2 py-2">
              <div className="flex flex-col space-y-1">
                <p className="text-sm font-semibold leading-none text-slate-900">Alterar Perfil</p>
                <p className="text-xs leading-none text-muted-foreground font-normal">
                  Simulação de login para testes
                </p>
              </div>
            </DropdownMenuLabel>
            <DropdownMenuSeparator className="bg-slate-100" />
            
            <div className="p-1 space-y-1">
                <DropdownMenuItem 
                onClick={() => setUsuarioAtivo('UsuarioA')}
                className="p-2 cursor-pointer rounded-lg focus:bg-blue-50 focus:text-blue-900 data-[state=checked]:bg-blue-50"
                >
                <div className="flex items-center gap-3 w-full">
                    <div className="flex items-center justify-center h-9 w-9 rounded-full bg-blue-100 text-blue-600 shrink-0">
                    <User className="h-4 w-4" />
                    </div>
                    <div className="flex flex-col flex-1 gap-0.5 min-w-0">
                    <span className="text-sm font-medium truncate">Usuário A</span>
                    <span className="text-[10px] text-muted-foreground truncate">Comércio & Varejo</span>
                    </div>
                    {usuarioAtivo === 'UsuarioA' && <Check className="h-4 w-4 text-blue-600 shrink-0" />}
                </div>
                </DropdownMenuItem>

                <DropdownMenuItem 
                onClick={() => setUsuarioAtivo('UsuarioB')}
                className="p-2 cursor-pointer rounded-lg focus:bg-emerald-50 focus:text-emerald-900 data-[state=checked]:bg-emerald-50"
                >
                <div className="flex items-center gap-3 w-full">
                    <div className="flex items-center justify-center h-9 w-9 rounded-full bg-emerald-100 text-emerald-600 shrink-0">
                    <Briefcase className="h-4 w-4" />
                    </div>
                    <div className="flex flex-col flex-1 gap-0.5 min-w-0">
                    <span className="text-sm font-medium truncate">Usuário B</span>
                    <span className="text-[10px] text-muted-foreground truncate">Serviços & Consultoria</span>
                    </div>
                    {usuarioAtivo === 'UsuarioB' && <Check className="h-4 w-4 text-emerald-600 shrink-0" />}
                </div>
                </DropdownMenuItem>
            </div>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>
    </header>
  );
}