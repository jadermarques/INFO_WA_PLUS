import streamlit as st
from io import StringIO
import sys
from pathlib import Path

ROOT = str(Path(__file__).resolve().parents[5])
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from src.app.infrastructure.agents import pipeline_analise

st.header("🕵️ Análise de Conversa")

HAS_NEW_NAV = hasattr(st, "navigation") and hasattr(st, "Page")

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

if HAS_NEW_NAV:
    submenu = st.selectbox(
        "Submenus de Análise",
        ["Importar", "Processar", "Prompt", "Relatórios"],
        key="submenu_analise_select",
    )
    if submenu == "Importar":
        render_importar()
    elif submenu == "Processar":
        render_processar()
    elif submenu == "Prompt":
        render_prompt()
    elif submenu == "Relatórios":
        render_relatorios()
else:
    with st.expander("Importar", expanded=True):
        render_importar()
    with st.expander("Processar", expanded=False):
        render_processar()
    with st.expander("Prompt", expanded=False):
        render_prompt()
    with st.expander("Relatórios", expanded=False):
        render_relatorios()
