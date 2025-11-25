import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import { Header } from './components/Header';
import { ChatPage } from './pages/ChatPage';
import { HistoryPage } from './pages/HistoryPage';

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        {/* Container Principal: ocupa toda a tela, fundo cinza claro */}
        <div className="min-h-screen w-full bg-gray-50 text-foreground font-sans">
          <Header />
          <Routes>
            <Route path="/" element={<ChatPage />} />
            <Route path="/historico" element={<HistoryPage />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </div>
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;