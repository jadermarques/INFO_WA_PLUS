# Projeto Info_AI_Studio

## Resumo da aplicacao

Nome do app: INFO_WA_PLUS

Personas: usuários que precisa de uma analise completa a partir de arquivos de conversas do whatsapp (em formato texto)
Canais de uso: GUI (Streamlit) + CLI (Typer).
Dados: SQLite em arquivo local (DB_PATH, default ./data.db). Backups: cópia com frequencia a ser programada do arquivo (.db) para pasta segura.
Métricas de sucesso: (i) cadastro de item ≤ 10s; (ii) zero erros de gravação em 7 dias; (iii) tempo de abertura da home ≤ 1s com até 5 mil itens.
Padrões de código: PEP 8 + PEP 257 (docstrings curtas)


## Tecnologias a serem utilizadas

Banco de dados: SQLite em arquivo local (DB_PATH, default ./data.db)
Interface: Strealit
Linguagem: Python >= 3.11
Framework: Crewai compatível com MCP (model context protocol)

## Especificação da GUI (Streamlit Multipage)

Navegação:
    Método (mais customizável): st.Page + st.navigation para configurar rotas/urls/ícones. 
Menu lateral
- dashboard
- configuracoes
-- configuracoes MPC (model context protocol)
-- layout arquivo
-- backup
- cadastros
-- modelo llm
-- base conhecimento
- agentes
-- agentes
-- tarefas
-- ferramentas externas/MCP
-- crews
-- flows
-- processos
- análise conversa
-- importar conversa
-- processar análise
-- prompt de análise de conversa
-- relatórios
- testes
- logs

## Especificação da CLI (Typer)
OBS: será especificado posteriormente.

Para cada comando, documente: propósito, args/opts obrigatórios, validações (ex.: email vazio), saída/exit codes e erros esperados.
Base: Typer (oficial, baseado em type hints).

## Requisitos funcionais

RF-01 — Cadastrar PROVEDOR / MODELO / API_KEY
Descrição: registrar os modelos de LLMs que poderao ser utilizados com suas respectiva API_KEY. Por exemplo, PROVEDOR=OPENAI;MODELO=GPT-5-NANO;OPENAI_API_KEY=xxxxxxxxxxxx; 
Entrada: provedor, modelo, api_key
Interfaces: GUI página “Configurações”; CLI modelo-ia --provedor --modelo --api_key.


RF-02 — Cadastrar Base de Conhecimento
Descrição da interface: 
    id_base (id, obrigatorio)
    nome base (texto, obrigatorio)
    descricao base (texto, opcional)
    ativo (default sim, obrigatorio)
Interfaces: GUI página "cadastros/base conhecimento"


RF-03 — Importar Conversa
Descrição da interface: Este interface deverá permitir o upload do arquivo.
Interfaces: GUI página "análise conversa/importar conversa"

RF-04 — Processar Conversa
Descrição da interface: Este interface irá invocar os agentes necessário para iniciar o fluxo de processo de análise de conversas.
Interfaces: GUI página "análise conversa/processar conversa"


A opcao Testes do menu lateral deverá permitir que seja feito um teste individual com cada agentes.

## Requisitos não-funcionais

Qualidade & Estilo: PEP 8, PEP 257, type hints em funções públicas. 
Configuração: .env com DB_PATH.
Observabilidade: logs no console (nível INFO, DEBUG, ERROR, FULL; mensagens de sucesso/erro claras).
Portabilidade: comandos simples: make gui, make cli, make test.
Desempenho-alvo: home ≤ 1s com 5k itens; listar itens ≤ 2s.


## Arquitetura e Pastas (layout src/)
Separação por camadas: domínio (regras), infra (DB/SQLite), interfaces (CLI/GUI), tests. Layout src/ para evitar imports acidentais e favorecer o pacote instalado.
.
├── README.md
├── .env.example
├── src/
│   └── app/
│       ├── __init__.py
│       ├── domain/            # regras e contratos do negócio (sem ORM)
│       ├── infrastructure/    # db (sqlite3), schema.sql, helpers
│       └── interfaces/
│           ├── cli/           # comandos Typer (db-init, users-create, items-add)
│           └── web/           # Streamlit app + pages/
│               ├── app.py
│               └── pages/
│                   ├── (...)

└── tests/                     # smoke test + unitários simples



## Modelo de Dados

Entidades e Regras:
    modelo_llm
        modl_id (int PK autoincrement)
        modl_provedor (tex not null)
        modl_modelo_llm (text not null)
        modl_api_key (text not null)
        modl_status (bool default 1)
    base_conhecimento
        baco_id (int PK autoincrement)
        baco_nome (text not null)
        baco_arquivo (text not null) (upload de arquivo .txt, .doc, .docx, .pdf)
        baco_descricao (text not null)
        base_status (bool default 1)


Transações & Acesso (DB-API 2.0):
    Abrir conexão (sqlite3.connect(DB_PATH)), row_factory = sqlite3.Row, uso de executemany/execute, commit e close.
    Utilizar helpers atômicos (context manager) para leitura/escrita.
    Bases oficiais: sqlite3 (stdlib/DB-API 2.0) e documentação do SQLite


## Critérios de Aceitação
OBS: será definido posteriormente

## Testes (mínimo viável)
OBS: será definido posteriormente

## Criacao de README.md
- Setup de venv, instalação, configuração .env, como rodar GUI (streamlit run) e CLI (app --help), inicializar banco, gerar backup e analise dos arquivos.

# Agentes e Orquestração do CrewAI

Observação: os elementos do crewai que estão descritos abaixo já podem ser cadastrados na base de dados do sistema, de forma que seus dados (parâmetros) já estejam disponíveis nas respectivas interfaces.

Conceito Central: A Equipe de Análise Orquestrada
Em vez de um fluxo linear, teremos um fluxo em duas fases:

Fase de Análise Individual: Os agentes especialistas analisam a conversa a partir de suas perspectivas únicas.

Fase de Colaboração e Síntese: O agente Líder recebe todas as análises, compara os achados, identifica contradições ou pontos cegos, e pode até "pedir" uma revisão antes de compilar o relatório final.

## Descricao dos agentes

Arquitetura de Agentes para um Modelo de Equipe
Vamos redefinir a equipe para incluir um maestro.

1. Engenheiro de Dados Multimídia (O Preparador)
Função: Este agente continua sendo o ponto de partida. Sua função é preparar o campo para a equipe, transformando os dados brutos (texto, áudio, imagem) em um único JSON estruturado e limpo. Ele não colabora na análise, mas fornece a "matéria-prima" essencial para todos.

Interação: Fornece o mesmo output para todos os especialistas simultaneamente.

Os Especialistas (A Equipe de Campo)
Estes são os analistas focados. Eles trabalham em paralelo, cada um com sua especialidade.

2. Especialista em Métricas
Função: Exatamente como antes, focado nos KPIs quantitativos.

Interação: Fornece seu relatório numérico ao Líder da Análise.

3. Especialista em Sentimento
Função: Como antes, focado na jornada emocional e no tom da conversa.

Interação: Fornece sua análise qualitativa ao Líder da Análise.

4. Especialista em Resolução
Função: Como antes, focado em identificar o problema e a eficácia da solução.

Interação: Fornece seu diagnóstico ao Líder da Análise.

O Maestro (O Elo Colaborativo)
Este é o novo agente que transforma o processo.

5. Líder de Análise e Qualidade (O Maestro)
Função: Este agente não faz a análise inicial. Seu papel é orquestrar, revisar e sintetizar. Ele atua como o gerente de qualidade do time, garantindo que o produto final seja coeso e preciso.

Goal: Orquestrar a equipe de especialistas para produzir um relatório de análise de atendimento coeso, preciso e de alta qualidade. Sua principal responsabilidade é revisar as análises individuais, identificar contradições ou sinergias, solicitar esclarecimentos (se necessário) e, finalmente, redigir o relatório final consolidado que representa a visão unificada da equipe.

Backstory: Você é o chefe de um time de "Customer Experience Insights". Você não analisa os dados brutos, mas é um mestre em conectar os pontos entre diferentes domínios de análise. Você sabe quando a análise de sentimento de um especialista contradiz a análise de resolução de outro e tem a habilidade de questionar e aprofundar a investigação para chegar à verdade. Seu produto final é a inteligência acionável, não apenas dados.

Interação: Este é o hub central. Ele recebe os outputs de todos os especialistas.

O Fluxo de Trabalho Colaborativo na Prática
Veja como a interação em equipe aconteceria em uma única execução da Crew:

Passo 1: Preparação

A tarefa_preparar_dados é executada pelo Engenheiro de Dados. O resultado é o JSON estruturado.

Passo 2: Análise dos Especialistas (Em Paralelo)

A tarefa_calcular_metricas, tarefa_analisar_sentimento e tarefa_verificar_resolucao são executadas, cada uma por seu respectivo especialista. Todas elas recebem o mesmo input: o JSON da tarefa anterior.

Passo 3: A "Reunião" do Líder (O Passo Colaborativo Chave)

Uma nova tarefa, tarefa_revisao_e_sintese, é atribuída ao Líder da Análise.

O contexto (context) desta tarefa é a lista com os resultados das três tarefas anteriores.

Dentro do prompt desta tarefa, a mágica acontece. O Líder é instruído a agir como um time:

"Compare os resultados: O relatório de sentimento indica que o cliente terminou 'satisfeito', mas o relatório de resolução aponta que o problema foi 'não resolvido'. Investigue essa contradição. Releia as últimas mensagens no JSON original e determine se a satisfação era genuína ou apenas uma formalidade educada."

"Conecte os pontos: O relatório de métricas mostra um 'tempo de primeira resposta' muito alto (25 minutos). Como isso impactou o sentimento inicial do cliente, conforme descrito pelo Especialista em Sentimento?"

"Peça aprofundamento (simulado): O Especialista em Resolução identificou o problema como 'dificuldade de login'. Com base na descrição da imagem de 'tela de erro com a mensagem usuário bloqueado', refine o diagnóstico para 'problema de conta bloqueada, não apenas dificuldade de login'."

"Formule o relatório final: Com base na sua revisão crítica e na combinação dos insights dos especialistas, produza o relatório final, incluindo a pontuação e as recomendações estratégicas."

Passo 4: Saída Final

O resultado da tarefa_revisao_e_sintese é o output final da Crew, um relatório que não é apenas uma soma das partes, mas uma síntese crítica delas.


