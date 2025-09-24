import streamlit as st

st.set_page_config(
	page_title="INFO_WA_PLUS",
	page_icon="💬",
	layout="wide",
	initial_sidebar_state="expanded",
)

st.title("INFO_WA_PLUS")
st.caption("Análise de conversas do WhatsApp")

try:
	# Preferencial (versões recentes do Streamlit): apenas páginas raiz
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
	# Fallback: criar links explícitos no sidebar para as páginas
	st.caption("Usando a navegação padrão do Streamlit.")
	with st.sidebar:
		st.markdown("---")
		st.caption("Navegação (compatível)")
		st.page_link("src/app/interfaces/web/app.py", label="Home", icon="🏠")
		st.page_link("pages/dashboard.py", label="Dashboard", icon="📊")
		st.page_link("pages/configuracoes.py", label="Configurações", icon="⚙️")
		st.page_link("pages/cadastros.py", label="Cadastros", icon="🗂️")
		st.page_link("pages/agentes.py", label="Agentes & Crew", icon="🧠")
		st.page_link("pages/analise.py", label="Análise de Conversa", icon="🕵️")
		st.page_link("pages/testes.py", label="Testes", icon="🧪")
		st.page_link("pages/logs.py", label="Logs", icon="📜")
