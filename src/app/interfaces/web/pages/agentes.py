import streamlit as st
import sys
from pathlib import Path

ROOT = str(Path(__file__).resolve().parents[5])
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from src.app.infrastructure.agents import (
	preparar_dados,
	especialista_metricas,
	especialista_sentimento,
	especialista_resolucao,
	lider_sintese,
)

st.header("🧠 Agentes & Crew")

HAS_NEW_NAV = hasattr(st, "navigation") and hasattr(st, "Page")

def render_testes():
	st.write("Teste individual de agentes (stubs)")
	texto = st.text_area("Texto de entrada", "Olá, obrigado pelo atendimento. Ainda não resolvido.")
	if st.button("Rodar agentes"):
		data = preparar_dados(texto)
		m = especialista_metricas(data)
		s = especialista_sentimento(data)
		r = especialista_resolucao(data)
		final = lider_sintese(data, [m, s, r])
		st.subheader("Saídas")
		st.json({"metricas": m.report, "sentimento": s.report, "resolucao": r.report, "final": final})

def render_tarefas():
	st.info("Listar/Executar tarefas dos agentes (stub)")

def render_ferramentas():
	st.info("Configurar ferramentas externas MCP (stub)")

def render_crews():
	st.info("Definir grupos de agentes (stub)")

def render_flows():
	st.info("Fluxos de análise (stub)")

def render_processos():
	st.info("Processos orquestrados (stub)")

if HAS_NEW_NAV:
	submenu = st.selectbox(
		"Submenus de Agentes",
		["Testes", "Tarefas", "Ferramentas MCP", "Crews", "Flows", "Processos"],
		key="submenu_agentes_select",
	)
	if submenu == "Testes":
		render_testes()
	elif submenu == "Tarefas":
		render_tarefas()
	elif submenu == "Ferramentas MCP":
		render_ferramentas()
	elif submenu == "Crews":
		render_crews()
	elif submenu == "Flows":
		render_flows()
	elif submenu == "Processos":
		render_processos()
else:
	with st.expander("Testes", expanded=True):
		render_testes()
	with st.expander("Tarefas", expanded=False):
		render_tarefas()
	with st.expander("Ferramentas MCP", expanded=False):
		render_ferramentas()
	with st.expander("Crews", expanded=False):
		render_crews()
	with st.expander("Flows", expanded=False):
		render_flows()
	with st.expander("Processos", expanded=False):
		render_processos()
