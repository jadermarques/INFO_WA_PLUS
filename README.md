# INFO_WA_PLUS

Projeto de análise de conversas do WhatsApp com GUI (Streamlit) e CLI (Typer). DB: SQLite local.

## Setup rápido

```bash
make setup          # cria venv, instala dependências e copia .env.example -> .env
make db-init        # inicializa tabelas
make gui            # inicia a GUI (usa .venv/bin/streamlit)
```

## Comandos

```bash
make setup         # venv + deps + .env
make install       # reinstala deps do requirements.txt
make install-core  # instala apenas dependências core
make db-init       # cria tabelas no SQLite
make gui           # inicia Streamlit (usa venv)
make cli           # mostra ajuda da CLI
make backup        # executa backup do arquivo .db
make test          # roda testes
```

CLI (exemplos):
```bash
.venv/bin/python -m src.app.interfaces.cli.app modelo-ia-add --provedor OPENAI --modelo gpt-4o-mini --api-key sk-... --status 1
.venv/bin/python -m src.app.interfaces.cli.app modelo-ia-list
.venv/bin/python -m src.app.interfaces.cli.app base-add --nome "Base Teste" --arquivo ./conversa1.txt --descricao "Exemplo" --status 1
.venv/bin/python -m src.app.interfaces.cli.app base-list
.venv/bin/python -m src.app.interfaces.cli.app seed   # popula dados de exemplo
.venv/bin/python -m src.app.interfaces.cli.app purge  # apaga todos os registros
```

## Estrutura

- `src/app/domain`: regras e modelos de domínio
- `src/app/infrastructure`: SQLite, schema.sql e helpers
- `src/app/interfaces/cli`: comandos Typer
- `src/app/interfaces/web`: app Streamlit + pages
- `tests`: testes simples

## Banco de Dados

- Use `DB_PATH` no `.env` (default `./data.db`)
- Transações: context managers com commit/rollback
- `schema.sql` contém as tabelas `modelo_llm` e `base_conhecimento`

## Fluxo "lite" (sem GUI)

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-core.txt
pytest -q           # roda testes
make db-init        # inicializa banco
python -m src.app.interfaces.cli.app --help
```

Atalho (com GUI):
```bash
make setup
make gui
```

## Compatibilidade Streamlit
- Quando a pasta `pages/` existe, a navegação usa `st.page_link` (multipage nativo) e não chama `st.navigation` (evitando warnings).
- Se não houver `pages/`, a app usa `st.navigation` com fallback por links.
