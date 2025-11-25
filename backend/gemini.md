# Gemini Context: Backend com Arquitetura Limpa em Django para "Chatbot de Atendimento Simulado"

Este arquivo estabelece as diretrizes e o contexto para o desenvolvimento do backend da 4Blue, utilizando **Arquitetura Limpa (Clean Architecture)** com Python e Django.

---

## O Desafio: "Chatbot de Atendimento Simulado"

O objetivo é construir um protótipo fullstack (Backend + Frontend) de um sistema de chat para simular uma tarefa real de desenvolvimento, avaliando a capacidade de implementar novas funcionalidades e criar uma solução completa.

### Tecnologias Obrigatórias
- **Backend:** Python 3+ com Django (ou Django REST Framework).
- **Frontend:** React.
- **Banco de Dados:** Utilizará **SQLite** (padrão do Django).
- **Controle de Versão:** Git.

---

## 1. Visão Geral da Arquitetura

O projeto seguirá uma variação da Arquitetura Limpa, separando claramente o domínio do negócio, a lógica da aplicação e a infraestrutura. O objetivo é criar um sistema de baixo acoplamento, testável, e independente de frameworks.

A regra principal é a **Regra de Dependência**: as camadas externas dependem das camadas internas, nunca o contrário.

As camadas são organizadas da seguinte forma (de dentro para fora):

1.  **Dominio:** Contém as `Entidades` (regras de negócio corporativas) e as interfaces dos `Repositorios`. É o núcleo do software.
2.  **Aplicacao:** Contém os `CasosDeUso` (regras de negócio da aplicação) que orquestram o fluxo de dados utilizando as abstrações do domínio.
3.  **Adaptadores de Interface:** Conversores e adaptadores (Controladores, Apresentadores, implementações de Repositórios).
4.  **Frameworks & Drivers:** A camada mais externa (Django, Banco de Dados, etc.).

---

## 2. Mapeamento da Arquitetura em Pastas

A estrutura de diretórios do projeto refletirá essas camadas.

```
F:\projetos\4blue\backend\
├── src/
│   ├── dominio/
│   │   ├── __init__.py
│   │   ├── entidades/           # Camada 1: Entidades (POPOs)
│   │   │   ├── usuario_mock.py
│   │   │   └── interacao_chat.py
│   │   └── repositorios/        # Camada 1: Interfaces dos Repositórios
│   │       ├── interface_repositorio_usuario_mock.py
│   │       └── interface_repositorio_interacao_chat.py
│   │
│   ├── aplicacao/               # Camada 2: Lógica da Aplicação
│   │   ├── __init__.py
│   │   └── casos_de_uso/        # Casos de Uso
│   │       ├── criar_interacao_chat.py
│   │       └── obter_historico_chat_usuario.py
│   │
│   ├── infraestrutura/          # Camadas 3 e 4
│   │   ├── __init__.py
│   │   ├── http/                # Framework HTTP (Django REST Framework)
│   │   │   ├── configuracoes.py
│   │   │   ├── urls.py
│   │   │   └── controladores/     # Endpoints da API (Views)
│   │   │       ├── mapeadores.py
│   │   │       └── views.py
│   │   └── persistencia/        # Implementação da Persistência (SQLite/Django ORM)
│   │       ├── django/
│   │       │   ├── models/
│   │       │   └── repositorios/  # Implementação concreta dos repositórios
│   │       │       ├── repositorio_usuario_mock_django.py
│   │       │       └── repositorio_interacao_chat_django.py
│   │       └── em_memoria/
│   │           └── repositorios/  # Implementação em memória para testes (opcional)
│   │
│   └── main.py                  # Ponto de entrada, configuração e injeção de dependência
│
├── tests/
│   ├── dominio/
│   │   └── entidades/
│   ├── aplicacao/
│   │   └── casos_de_uso/
│   └── infraestrutura/
│       ├── http/
│       └── persistencia/
│
├── manage.py
├── requirements.txt
└── gemini.md
```

---

## 3. Detalhes das Camadas

### Camada 1: Dominio (Entidades e Interfaces de Repositório)
- **Local:** `src/dominio/`
- **Conteúdo:**
    - **`entidades/`**: Objetos de negócio puros (POPOs). Representam os conceitos centrais do Chatbot.
    - **`repositorios/`**: Contratos (interfaces abstratas) que definem como os dados das entidades são recuperados e armazenados. Os `casos_de_uso` dependerão destas interfaces, não de suas implementações.
- **Exemplo de Entidade (`src/dominio/entidades/`):**
    - **`UsuarioMock`:**
        - `id`: UUIDField (primary_key, default=uuid.uuid4, editable=False)
        - `identificador`: CharField (max_length=50, unique=True) - (Usuário A/B)
        - `criado_em`: DateTimeField (auto_now_add=True)
        - `__str__`: deve retornar o `identificador`.
    - **`InteracaoChat`:**
        - `id`: UUIDField (primary_key, default=uuid.uuid4, editable=False)
        - `usuario`: ForeignKey para 'UsuarioMock'
        - `mensagem_usuario`: TextField (mensagem do usuário)
        - `resposta_bot`: TextField (resposta simulada da API)
        - `criado_em`: DateTimeField (auto_now_add=True, db_index=True)
        - `Meta`: `ordering = ['criado_em']`
        - `__str__`: deve retornar `"{usuario.identificador} - {hora}"`.

### Camada 2: Aplicacao (Casos de Uso)
- **Local:** `src/aplicacao/casos_de_uso/`
- **Conteúdo:** Implementam a lógica de negócio específica da aplicação. Orquestram o fluxo de dados entre o domínio e a camada de persistência através das interfaces de repositório.
- **Exemplo:**
    - `CriarInteracaoChatCasoDeUso`: Recebe dados brutos, utiliza a interface `InterfaceRepositorioInteracaoChat` para salvar a interação e retorna o resultado.
    - `ObterHistoricoChatUsuarioCasoDeUso`: Recebe um identificador de usuário e utiliza `InterfaceRepositorioInteracaoChat` para buscar seu histórico.

### Camada 3: Adaptadores de Interface

- **`src/infraestrutura/http/controladores/` (Controladores e Mapeadores):** Adaptam as requisições HTTP para chamadas aos `casos_de_uso` e convertem os dados de retorno para respostas HTTP (JSON). `views.py` atua como o Controlador e `mapeadores.py` (antes Serializers) converte os dados. **Este backend funciona como uma API RESTful e não renderiza templates.**
- **`src/infraestrutura/persistencia/django/repositorios/`:** Implementações concretas das interfaces de repositório definidas em `src/dominio/repositorios/`. É aqui que a lógica de banco de dados (usando o ORM do Django) reside.

### Camada 4: Frameworks & Drivers

- **`src/infraestrutura/http/` (Django/DRF):** A implementação concreta do framework HTTP, servindo como uma **API RESTful**.
- **`src/infraestrutura/persistencia/django/models/` (Django ORM):** Define o schema do banco de dados **SQLite**. É um detalhe de implementação da persistência que corresponde às entidades do domínio.

---

## 4. Requisitos Funcionais (Backend)

1.  **"Login Mockado" (Simulado):**
    *   Não há sistema de login complexo.
    *   O backend deve estar preparado para receber um identificador de usuário (`A` ou `B`) com as requisições de chat.

2.  **A Tela de Chat:**
    *   A API (Django) deve salvar a mensagem enviada pelo usuário no banco de dados, vinculando-a ao usuário correto.
    *   A API deve retornar uma resposta mockada (simulada) para o frontend (diferentes para cada usuário, ex: "Obrigado por seu contato. Em breve responderemos.").

3.  **A Tela de Histórico:**
    *   A API deve fornecer um endpoint para buscar e exibir o histórico de mensagens (perguntas e respostas) para o usuário que estiver ativo (A ou B).

---

## 5. Comandos Úteis

-   **Iniciar Servidor:** `python manage.py runserver`
-   **Rodar Testes:** `python manage.py test`
-   **Instalar Dependências:** `pip install -r requirements.txt`
-   **Criar Migrações:** `python manage.py makemigrations`
-   **Aplicar Migrações:** `python manage.py migrate`

---

## 6. Convenções de Código

-   **Estilo:** PEP 8.
-   **Tipagem:** Uso obrigatório de Type Hints em todas as assinaturas de função e método.
-   **Injeção de Dependência:** As dependências das camadas externas (como repositórios concretos) serão injetadas nas camadas internas (casos de uso) para manter o baixo acoplamento e facilitar os testes.

---

## 7. Critérios de Avaliação (Foco Backend)

-   **Qualidade do Código:** Organização, clareza e boas práticas em Python/Django.
-   **Lógica de Negócio:** Capacidade de implementar a filtragem de dados por usuário (requisito principal do histórico) e a geração de respostas mockadas.
-   **Modelagem de Dados:** Como você estruturou seus models no Django para armazenar usuários e mensagens de chat.
-   **Funcionalidade:** O aplicativo backend cumpre os requisitos descritos (salvar mensagens, retornar respostas mockadas, fornecer histórico por usuário).
-   **Documentação:** A clareza do `README.md` (instruções de setup, decisões técnicas, como os models foram estruturados no Django).
