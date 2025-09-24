import streamlit as st
import sys
from pathlib import Path

ROOT = str(Path(__file__).resolve().parents[5])
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from src.app.infrastructure.repositories import (
    modelo_llm_add, modelo_llm_list,
    base_conhecimento_add, base_conhecimento_list
)

st.header("🗂️ Cadastros")

HAS_NEW_NAV = hasattr(st, "navigation") and hasattr(st, "Page")

def render_modelos():
    st.subheader("Modelos LLM")
    with st.form("form_modelo"):
        provedor = st.text_input("Provedor", placeholder="OPENAI")
        modelo = st.text_input("Modelo", placeholder="gpt-4o-mini")
        api_key = st.text_input("API Key", type="password")
        ativo = st.checkbox("Ativo", value=True)
        if st.form_submit_button("Salvar"):
            if not (provedor and modelo and api_key):
                st.error("Campos obrigatórios: provedor, modelo, api_key")
            else:
                _id = modelo_llm_add(provedor, modelo, api_key, 1 if ativo else 0)
                st.success(f"Salvo com id={_id}")
    st.table(modelo_llm_list())

def render_bases():
    st.subheader("Base de Conhecimento")
    with st.form("form_base"):
        nome = st.text_input("Nome da base")
        arquivo = st.text_input("Caminho do arquivo (.txt/.pdf/...)")
        descricao = st.text_area("Descrição")
        ativo2 = st.checkbox("Ativo", value=True)
        if st.form_submit_button("Salvar base"):
            if not (nome and arquivo):
                st.error("Campos obrigatórios: nome e arquivo")
            else:
                _id = base_conhecimento_add(nome, arquivo, descricao, 1 if ativo2 else 0)
                st.success(f"Salvo com id={_id}")
    st.table(base_conhecimento_list())

if HAS_NEW_NAV:
    submenu = st.selectbox(
        "Submenus de Cadastros",
        ["Modelos LLM", "Base de Conhecimento"],
        key="submenu_cadastros_select",
    )
    if submenu == "Modelos LLM":
        render_modelos()
    elif submenu == "Base de Conhecimento":
        render_bases()
else:
    with st.expander("Modelos LLM", expanded=True):
        render_modelos()
    with st.expander("Base de Conhecimento", expanded=True):
        render_bases()
