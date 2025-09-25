from __future__ import annotations
import typer
from pathlib import Path
from rich import print

from src.app.infrastructure.db import init_db
from src.app.infrastructure.repositories import (
    modelo_llm_add,
    modelo_llm_list,
    modelo_llm_delete_all,
    base_conhecimento_add,
    base_conhecimento_list,
    base_conhecimento_delete_all,
)
from src.app.infrastructure.backup import run_backup

app = typer.Typer(help="CLI INFO_WA_PLUS")


@app.command("db-init")
def db_init(
    schema: Path = typer.Option("src/app/infrastructure/schema.sql", exists=True, readable=True),
):
    """Inicializa o banco de dados (cria tabelas)."""
    init_db(str(schema))
    print("[green]Banco inicializado com sucesso.[/green]")


@app.command("modelo-ia-add")
def modelo_ia_add(
    provedor: str = typer.Option(..., help="Nome do provedor (ex.: OPENAI)"),
    modelo: str = typer.Option(..., help="Nome do modelo (ex.: gpt-4o-mini)"),
    api_key: str = typer.Option(..., help="API key do provedor"),
    status: int = typer.Option(1, min=0, max=1),
):
    """Cadastra um modelo de LLM com sua API key."""
    _id = modelo_llm_add(provedor, modelo, api_key, status)
    print({"id": _id, "provedor": provedor, "modelo": modelo, "status": status})


@app.command("modelo-ia-list")
def modelo_ia_list(ativos: bool = typer.Option(False, help="Listar apenas ativos")):
    """Lista modelos cadastrados."""
    rows = modelo_llm_list(only_active=ativos)
    print(rows)


@app.command("base-add")
def base_add(
    nome: str = typer.Option(..., help="Nome da base de conhecimento"),
    arquivo: Path = typer.Option(..., exists=False, help="Caminho do arquivo"),
    descricao: str = typer.Option("", help="Descrição"),
    status: int = typer.Option(1, min=0, max=1),
):
    """Cadastra uma base de conhecimento."""
    _id = base_conhecimento_add(nome, str(arquivo), descricao, status)
    print({"id": _id, "nome": nome, "arquivo": str(arquivo), "status": status})


@app.command("base-list")
def base_list(ativos: bool = typer.Option(False, help="Listar apenas ativos")):
    """Lista bases de conhecimento cadastradas."""
    rows = base_conhecimento_list(only_active=ativos)
    print(rows)


@app.command("backup")
def backup(dest: Path = typer.Option("./backups", help="Diretório de destino")):
    """Gera uma cópia do arquivo de banco de dados."""
    path = run_backup(str(dest))
    print({"backup": path})


@app.command("purge")
def purge():
    """Apaga TODOS os registros das tabelas (cuidado!)."""
    modelo_llm_delete_all()
    base_conhecimento_delete_all()
    print("[yellow]Tabelas limpas.[/yellow]")


@app.command("seed")
def seed():
    """Popula o banco com alguns registros de exemplo."""
    # modelos
    modelo_llm_add("OPENAI", "gpt-4o-mini", "sk-demo-1", 1)
    modelo_llm_add("OPENAI", "gpt-4o", "sk-demo-2", 0)
    modelo_llm_add("GEMINI", "1.5-flash", "sk-demo-3", 1)
    # bases
    base_conhecimento_add("FAQ", "./docs/faq.txt", "Perguntas frequentes", 1)
    base_conhecimento_add("Políticas", "./docs/politicas.pdf", "Documentos de políticas", 1)
    base_conhecimento_add("Exemplos", "./dados/exemplos.txt", "Amostras de conversas", 0)
    print("[green]Seed concluído.[/green]")


if __name__ == "__main__":
    app()
