import streamlit as st
from pathlib import Path

st.set_page_config(
	page_title="INFO_WA_PLUS",
	page_icon="💬",
	layout="wide",
	initial_sidebar_state="expanded",
)

st.title("INFO_WA_PLUS")
st.caption("Análise de conversas do WhatsApp")

# Se a pasta pages/ existir (modo multipage nativo), não use st.navigation
pages_dir = Path(__file__).parent / "pages"
if pages_dir.exists():
	# Usar apenas a navegação multipage nativa do Streamlit (evitar duplicidade)
	pass
else:
	# Sem pasta pages/: use st.navigation com páginas raiz
	try:
		pages = [
			st.Page("pages/dashboard.py", title="Dashboard", icon="📊"),
			st.Page("pages/configuracoes.py", title="Configurações", icon="⚙️"),
			st.Page("pages/cadastros.py", title="Cadastros", icon="🗂️"),
			st.Page("pages/agentes.py", title="Agentes & Crew", icon="🧠"),
			st.Page("pages/analise.py", title="Análise de Conversa", icon="🕵️"),
			st.Page("pages/testes.py", title="Testes", icon="🧪"),
			st.Page("pages/logs.py", title="Logs", icon="📜"),
		]
		nav = st.navigation(pages)
		nav.run()
	except Exception:
		# Fallback por links
		st.caption("Usando navegação compatível.")
		with st.sidebar:
			st.markdown("---")
			st.caption("Navegação")
			st.page_link("pages/dashboard.py", label="Dashboard", icon="📊")
			st.page_link("pages/configuracoes.py", label="Configurações", icon="⚙️")
			st.page_link("pages/cadastros.py", label="Cadastros", icon="🗂️")
			st.page_link("pages/agentes.py", label="Agentes & Crew", icon="🧠")
			st.page_link("pages/analise.py", label="Análise de Conversa", icon="🕵️")
			st.page_link("pages/testes.py", label="Testes", icon="🧪")
			st.page_link("pages/logs.py", label="Logs", icon="📜")
