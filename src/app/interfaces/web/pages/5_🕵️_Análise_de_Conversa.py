import streamlit as st
from io import StringIO
import sys
from pathlib import Path

ROOT = str(Path(__file__).resolve().parents[5])
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from src.app.infrastructure.agents import pipeline_analise

st.header("🕵️ Análise de Conversa")

def render_importar():
    st.subheader("Importar conversa (upload)")
    uploaded = st.file_uploader("Arquivo de conversa (.txt)", type=["txt"]) 
    if uploaded is not None:
        content = uploaded.getvalue().decode("utf-8", errors="ignore")
        st.session_state["uploaded_conversation"] = content
        st.success("Arquivo carregado com sucesso")

def render_processar():
    st.subheader("Processar análise (mock)")
    if st.button("Processar"):
        if "uploaded_conversation" not in st.session_state:
            st.error("Nenhum arquivo importado.")
        else:
            text = st.session_state["uploaded_conversation"]
            result = pipeline_analise(text)
            st.success("Análise concluída (stub)")
            st.json(result)

def render_prompt():
    st.subheader("Prompt de análise de conversa")
    prompt = st.text_area("Prompt", "Resuma os principais tópicos e sentimento.")
    if st.button("Executar prompt (simulado)"):
        st.write("Resultado (mock): Relatório gerado com base no prompt.")

def render_relatorios():
    st.subheader("Relatórios (mock)")
    st.write("Lista de relatórios gerados aparecerá aqui.")

tab_importar, tab_processar, tab_prompt, tab_relatorios = st.tabs(
    ["Importar", "Processar", "Prompt", "Relatórios"]
)
with tab_importar:
    render_importar()
with tab_processar:
    render_processar()
with tab_prompt:
    render_prompt()
with tab_relatorios:
    render_relatorios()
