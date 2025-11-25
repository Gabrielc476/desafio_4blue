# Chatbot de Atendimento Simulado - Desafio Técnico 4Blue

Este projeto é um protótipo Fullstack desenvolvido para atender aos requisitos do teste técnico da 4Blue. O objetivo é simular um ambiente de chat corporativo onde é possível alternar entre perfis de usuários e visualizar históricos de conversa, com persistência de dados real, mas respostas simuladas (mock).

## 📋 Funcionalidades (Conforme Requisitos)

### Login Mockado (Simulação de Perfil):
- Não há sistema de autenticação complexo (JWT/Session).
- Um seletor no frontend permite alternar instantaneamente entre "Usuário A" e "Usuário B".
- O estado do usuário ativo é gerenciado via React Context API, garantindo que a troca de perfil atualize toda a aplicação.

### Interface de Chat:
- Envio de mensagens persistidas no banco de dados.
- Respostas automáticas simuladas pelo Backend (ex: "Obrigado pelo contato...").
- Interface otimista: a mensagem aparece instantaneamente na tela enquanto é salva em segundo plano.

### Histórico de Mensagens:
- Página dedicada para consulta de conversas anteriores.
- Filtragem de Dados: O histórico exibe apenas as mensagens do perfil atualmente selecionado, demonstrando a capacidade de segregação de dados no backend.

## 🛠️ Arquitetura e Detalhes Técnicos

A principal decisão técnica deste projeto foi não seguir o padrão convencional "MVT" (Model-View-Template) do Django, optando por uma variação da Clean Architecture (Arquitetura Limpa). O objetivo foi desacoplar as regras de negócio do framework web.

### 1. Backend (Python / Django)

O código está organizado em camadas concêntricas, respeitando a Regra de Dependência (as camadas internas não conhecem as externas).

#### Estrutura de Camadas (`src/`)

-   **🟡 Camada de Domínio (`src/dominio`)**
    -   É o núcleo do sistema. Contém as Entidades (`UsuarioMock`, `InteracaoChat`) e as Interfaces de Repositórios.
    -   Característica: Python puro. Não possui importações do Django ou bibliotecas externas. Define "o que" o sistema faz, não "como".

-   **🟢 Camada de Aplicação (`src/aplicacao`)**
    -   Contém os Casos de Uso (`CriarInteracaoChat`, `ObterHistorico`).
    -   Orquestra o fluxo de dados: recebe uma requisição, valida regras de negócio e chama os repositórios (através das interfaces) para salvar/buscar dados.
    -   Característica: Depende apenas do Domínio.

-   **🔵 Camada de Infraestrutura (`src/infraestrutura`)**
    -   Onde o mundo real acontece. Aqui residem os detalhes de implementação.
    -   Persistência: Implementação concreta dos repositórios usando o Django ORM.
    -   Web/HTTP: Django REST Framework (DRF) atua como um adaptador de entrada, convertendo requisições HTTP em chamadas para os Casos de Uso.
    -   Injeção de Dependência: As Views instanciam as implementações concretas (ex: `RepositorioUsuarioDjango`) e as injetam nos Casos de Uso.

#### Padrões Utilizados
-   **Repository Pattern:** Abstrai a camada de dados. O Caso de Uso não sabe se os dados vêm do SQLite ou de uma API externa.
-   **Dependency Inversion (SOLID):** Os módulos de alto nível (Aplicação) não dependem de módulos de baixo nível (Infraestrutura), ambos dependem de abstrações (Interfaces do Domínio).

### 2. Frontend (React / TypeScript)

A arquitetura do frontend foca em separação de responsabilidades (UI vs Lógica) e UX.

#### Estrutura e Padrões

-   **Gerenciamento de Estado (Context API):**
    -   O `AuthContext` mantém o estado global do usuário ativo (`UsuarioA` ou `UsuarioB`). Isso evita o "prop drilling" (passar props por muitos níveis) e garante que o Header e as Páginas estejam sempre sincronizados.

-   **Custom Hooks (`useChat`):**
    -   Toda a lógica de envio de mensagens e comunicação com a API foi extraída para um hook personalizado.
    -   Isso deixa o componente visual (`ChatPage.tsx`) limpo, lidando apenas com renderização.

-   **Optimistic UI (Interface Otimista):**
    -   Para dar sensação de instantaneidade, a mensagem do usuário é adicionada à lista visual antes da resposta do servidor (marcada como "enviando").
    -   Quando a API responde, a mensagem temporária é substituída pela oficial.

-   **Componentização (shadcn/ui):**
    -   Uso de componentes reutilizáveis e acessíveis (Radix UI) estilizados com Tailwind CSS.

## 🚀 Como Rodar o Projeto

Siga os passos abaixo para executar a aplicação em sua máquina.

### Pré-requisitos
-   Python 3.10+
-   Node.js 18+

### 1. Executando o Backend (API)

Abra um terminal na pasta `backend`:

```bash
# 1. Instale as dependências
pip install -r requirements.txt

# 2. Crie as migrações do banco de dados
python manage.py makemigrations
python manage.py migrate

# 3. Inicie o servidor
python manage.py runserver
```

O servidor backend estará rodando em: `http://localhost:8000`

### 2. Executando o Frontend (Interface)

Abra um novo terminal na pasta `frontend`:

```bash
# 1. Instale as dependências
npm install

# 2. Inicie o servidor de desenvolvimento
npm run dev
```

Acesse a aplicação no navegador: `http://localhost:5173`

## 🧪 Decisões de Modelagem (Django)

Para atender ao requisito de persistência e histórico, foram criados dois modelos principais:

-   **`MockUser`:** Armazena o identificador único do usuário (ex: "UsuarioA").
-   **`ChatInteraction`:** Armazena cada mensagem trocada.
    -   Possui uma `ForeignKey` para `MockUser`.
    -   Campos: `user_message` (pergunta), `bot_response` (resposta mockada) e `created_at` (timestamp).
    -   Isso permite consultas eficientes filtrando por `user_id`, essencial para a tela de histórico.

## 📧 Contato

Projeto desenvolvido como parte do processo seletivo da 4Blue.
