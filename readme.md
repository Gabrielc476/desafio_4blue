# Chatbot de Atendimento Inteligente - 4Blue (Versão IA)

Este projeto é uma evolução do desafio técnico da 4Blue, transformando um chatbot simulado em um Consultor Financeiro Inteligente real. Utilizando a API do Google Gemini 2.5-flash, o sistema implementa uma arquitetura de múltiplos agentes para fornecer diagnósticos financeiros precisos e personalizados para pequenas empresas.

## 🧠 Diferenciais da Versão IA

Diferente de chatbots tradicionais que apenas respondem a perguntas soltas, este sistema utiliza um Workflow Sequencial de Agentes para garantir profundidade e precisão nas respostas.

### O Workflow de Agentes ("The Brain & The Voice")

A cada mensagem enviada pelo usuário, o backend orquestra uma cadeia de pensamento:

-   **🕵️ Agente 1: O Analista (Silent Observer)**
    -   **Função:** Analisa o histórico da conversa e a nova mensagem.
    -   **Objetivo:** Diagnosticar a "dor oculta" (ex: mistura de contas PF/PJ, precificação errada) e determinar o estágio da conversa (Investigação ou Solução).
    -   **Saída:** Um relatório técnico interno (invisível para o usuário).

-   **👨‍💼 Agente 2: O Consultor (The Persona)**
    -   **Função:** Recebe a mensagem do usuário + o relatório técnico do Analista.
    -   **Objetivo:** Traduzir o diagnóstico em uma resposta empática, didática e alinhada com a metodologia da 4Blue.
    -   **Saída:** A resposta final no chat.
    -   **Resultado:** O usuário sente que está conversando com um consultor humano que entende o contexto do seu negócio, e não com um robô genérico.

## 📋 Funcionalidades

### Consultoria em Tempo Real:
-   Respostas geradas por IA (Gemini 2.5-flash) com contexto de todo o histórico da conversa.
-   Formatação rica (Markdown) para listas, negritos e passos práticos.

### Perfis de Usuário Distintos:
-   Usuário A (Comércio): O sistema adapta o contexto para dores de varejo/estoque.
-   Usuário B (Serviços): O sistema foca em precificação de hora/homem e contratos.
-   (A IA detecta e se adapta ao perfil automaticamente pelo contexto da conversa).

### Interface Otimista & Moderna:
-   Envio instantâneo de mensagens (Optimistic UI).
-   Renderização completa de Markdown (listas, links, ênfases).
-   Histórico persistido e filtrado por usuário.

## 🛠️ Arquitetura Técnica

O projeto segue a Clean Architecture, garantindo que a integração com a IA seja apenas um detalhe de implementação, sem poluir as regras de negócio.

### Backend (Python / Django)

-   **Camada de Domínio:** Define a interface `InterfaceServicoIA`. O domínio não sabe que usamos o Gemini, apenas que existe um "serviço de inteligência".
-   **Camada de Aplicação:**
    -   **Casos de Uso:** O `CriarInteracaoChat` atua como orquestrador. Ele recupera o histórico, chama o Agente Analista, injeta o resultado no Agente Consultor e salva a resposta.
    -   **Prompts:** Os arquivos de prompt (`prompts.py`) definem a "alma" e as regras de negócio dos agentes.
-   **Camada de Infraestrutura:**
    -   `GeminiService`: Implementação concreta que se comunica com a API do Google Generative AI.
    -   Persistência: Django ORM (SQLite).

### Frontend (React / TypeScript)

-   **Renderização de Markdown:** Uso de `react-markdown` e `@tailwindcss/typography` para exibir as respostas complexas da IA com beleza e legibilidade.
-   **Gerenciamento de Estado:** Context API para gerenciar a sessão do usuário e atualizar o histórico em tempo real.
-   **Estilização:** Tailwind CSS + shadcn/ui.

## 🚀 Como Rodar o Projeto

### Pré-requisitos
-   Chave de API do Gemini: Obtenha gratuitamente no [Google AI Studio](https://ai.google.dev/).
-   Python 3.10+ e Node.js 18+.

### 1. Configuração do Backend

Entre na pasta `backend`:

```bash
cd backend
```

Crie um arquivo `.env` na raiz do backend e adicione sua chave:

```
GEMINI_API_KEY=sua_chave_aqui
```

Instale as dependências (incluindo as libs de IA):

```bash
pip install -r requirements.txt
```

Rode as migrações e o servidor:

```bash
python manage.py migrate
python manage.py runserver
```

### 2. Configuração do Frontend

Entre na pasta `frontend`:

```bash
cd frontend
```

Instale as dependências e inicie:

```bash
npm install
npm run dev
```

Acesse `http://localhost:5173` e comece a conversar com seu Consultor 4Blue!

## 🧪 Exemplo de Uso (Prompt Engineering)

Experimente enviar esta mensagem como Usuário A:

"Estou vendendo muito mas não vejo a cor do dinheiro no final do mês. O que está acontecendo?"

O que acontece nos bastidores:

-   **Analista:** Identifica provável "falta de precificação correta" ou "mistura de contas pessoais". Estágio: Investigação.
-   **Consultor:** Recebe a dica e responde: "Isso é um clássico 'Vender, Vender e Morrer'. É provável que sua margem de contribuição esteja errada ou você esteja retirando mais do que a empresa aguenta. Você sabe exatamente quanto custa para abrir sua porta todo dia (Custos Fixos)?"

## 📧 Contato

Projeto desenvolvido como parte do processo seletivo da 4Blue.
