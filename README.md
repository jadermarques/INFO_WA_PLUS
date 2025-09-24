# INFO_WA_PLUS

Projeto de análise de conversas do WhatsApp com GUI (Streamlit) e CLI (Typer). DB: SQLite local.

## Setup rápido

```bash
python3 -m venv .venv
source .venv/bin/activate
# Instalação rápida p/ testes (sem GUI):
pip install -r requirements-core.txt
# Para GUI (Streamlit), depois instale o extra:
pip install -r requirements.txt
cp .env.example .env  # ajuste DB_PATH se necessário
```

## Comandos

```bash
make db-init     # cria tabelas no SQLite
make gui         # inicia Streamlit multipage (requer requirements.txt)
make cli         # mostra ajuda da CLI
make backup      # executa backup do arquivo .db
make install-core  # instala apenas dependências de core (sem GUI)
make setup         # executa setup completo (venv + deps + .env)
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
make setup          # cria venv, instala core + GUI e copia .env
make gui
```

## Compatibilidade Streamlit
- Navegação preferida usa `st.Page` + `st.navigation` (requer Streamlit recente). Foi adicionado um fallback automático para versões antigas usando `st.sidebar.page_link`.
