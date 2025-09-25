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

tab_testes, tab_tarefas, tab_ferramentas, tab_crews, tab_flows, tab_processos = st.tabs(
	["Testes", "Tarefas", "Ferramentas MCP", "Crews", "Flows", "Processos"]
)
with tab_testes:
	render_testes()
with tab_tarefas:
	render_tarefas()
with tab_ferramentas:
	render_ferramentas()
with tab_crews:
	render_crews()
with tab_flows:
	render_flows()
with tab_processos:
	render_processos()
