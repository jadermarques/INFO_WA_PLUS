# Copilot Instructions for INFO_WA_PLUS

- Stack: Python 3.11+, Streamlit multipage GUI, Typer CLI, SQLite (DB-API 2.0), CrewAI (planned), MCP-compatible integration (planned).
- Layout: `src/app/{domain,infrastructure,interfaces/{cli,web}}` with tests under `tests/`.
- Config: Read `DB_PATH` and `LOG_LEVEL` from `.env` via `src/app/config.py` (`settings`). Default DB is `./data.db`.

## Architecture
- Domain: `src/app/domain/models.py` defines simple dataclasses (`ModeloLLM`, `BaseConhecimento`). No ORM.
- Infrastructure: `src/app/infrastructure/`
  - `db.py`: context-managed connection via `get_conn()`, `init_db(schema.sql)`, atomic helpers `execute`, `query_all`.
  - `schema.sql`: tables `modelo_llm` and `base_conhecimento` as per requisitos.
  - `repositories.py`: CRUD helpers used by CLI/GUI (add/list for both entities).
  - `backup.py`: copies DB file to timestamped path.
  - `agents.py`: stubs dos agentes (preparar dados, métricas, sentimento, resolução) e orquestração (`pipeline_analise`).
- Interfaces:
  - CLI: `src/app/interfaces/cli/app.py` (Typer). Commands: `db-init`, `modelo-ia-add`, `modelo-ia-list`, `base-add`, `base-list`, `backup`.
  - GUI: `src/app/interfaces/web/app.py` + pages em `pages/` (dashboard, configuracoes, cadastros, agentes, analise, testes, logs). Usa `st.Page` + `st.navigation`. Em `pages/analise.py`, o botão Processar chama `pipeline_analise`. Em `pages/agentes.py`, é possível executar cada agente individualmente.

## Conventions
- PEP 8/257, public functions with type hints. Keep modules minimal and cohesive.
- Use repositories from interfaces; do not import `sqlite3` from UI/CLI.
- Wrap all DB access in `get_conn()`; never keep global connections.
- Status fields use `int` (0/1) to mirror SQLite; GUI converts from checkbox.

## Developer Workflows
- Setup: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt && cp .env.example .env`.
- Initialize DB: `make db-init` (uses `schema.sql`).
- Run GUI: `make gui` (opens Streamlit app with left nav).
- Use CLI: `python -m src.app.interfaces.cli.app --help` or `make cli`.
- Backup: `make backup` writes to `./backups` (default).
- Tests: `pytest -q` (see `tests/test_smoke.py`).

## Patterns to Follow
- Adding new entities: update `schema.sql`, create repo functions in `repositories.py`, expose CLI commands and Streamlit forms/tables under `pages/`.
- Validations: basic presence checks in GUI; stricter validation should be placed before calling repo helpers.
- Logging: prefer printing concise success/error messages in CLI; Streamlit surfaces errors with `st.error`.

## Integration Points
- CrewAI/MCP: atualmente os agentes são stubs em `infrastructure/agents.py`. Ao integrar provedores reais, mantenha a orquestração isolada (ex.: `agents.py` ou `agents_service.py`).
- File uploads: `pages/analise.py` armazena o texto em `st.session_state["uploaded_conversation"]` e dispara `pipeline_analise`.

## Examples
- Insert LLM model via CLI: `python -m src.app.interfaces.cli.app modelo-ia-add --provedor OPENAI --modelo gpt-4o-mini --api-key sk-...`
- List bases in GUI: open Cadastros → displays `base_conhecimento_list()` result.
 - Executar análise pela GUI: vá em "Análise de Conversa", faça upload `.txt` e clique em "Processar".
 - Testar agentes: em "Agentes & Crew", clique em "Rodar agentes".

## Notes
- Default DB path is relative to CWD; set `DB_PATH` if running from different dirs.
- Keep changes surgical; avoid renaming public command names without updating README/Makefile.
