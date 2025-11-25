import { createContext, useState, useContext } from 'react';
import type { ReactNode } from 'react';

interface AuthContextType {
  usuarioAtivo: string;
  setUsuarioAtivo: (usuario: string) => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  // Começamos com o UsuarioA por padrão
  const [usuarioAtivo, setUsuarioAtivo] = useState<string>('UsuarioA');

  return (
    <AuthContext.Provider value={{ usuarioAtivo, setUsuarioAtivo }}>
      {children}
    </AuthContext.Provider>
  );
};

// eslint-disable-next-line react-refresh/only-export-components
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth deve ser usado dentro de um AuthProvider');
  }
  return context;
};