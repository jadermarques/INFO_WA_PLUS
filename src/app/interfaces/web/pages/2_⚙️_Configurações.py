import streamlit as st
import sys
from pathlib import Path

# Garantir que o diretório raiz do projeto esteja no sys.path
ROOT = str(Path(__file__).resolve().parents[5])
if ROOT not in sys.path:
	sys.path.insert(0, ROOT)

from src.app.config import settings
from src.app.infrastructure.db import init_db
from src.app.infrastructure.backup import run_backup

st.header("⚙️ Configurações")
st.write(f"DB_PATH atual: `{settings.db_path}`")
st.write("Ajuste variáveis via arquivo `.env`.")

def render_mcp():
	st.subheader("🧩 Configurações MCP")
	st.info("Defina parâmetros de conexões MCP (stub)")

def render_layout():
	st.subheader("🧾 Layout do Arquivo")
	st.info("Defina/parsen o layout de arquivo de conversa (stub)")

def render_backup():
	st.subheader("💾 Backup")
	col1, col2 = st.columns(2)
	with col1:
		if st.button("Inicializar Banco (schema.sql)"):
			try:
				init_db("src/app/infrastructure/schema.sql")
				st.success("Banco inicializado.")
			except Exception as e:
				st.error(f"Erro ao inicializar: {e}")
	with col2:
		if st.button("Backup do Banco"):
			try:
				path = run_backup("./backups")
				st.success(f"Backup criado em {path}")
			except Exception as e:
				st.error(f"Erro no backup: {e}")

tab_mcp, tab_layout, tab_backup = st.tabs(["MCP", "Layout do Arquivo", "Backup"])
with tab_mcp:
	render_mcp()
with tab_layout:
	render_layout()
with tab_backup:
	render_backup()
