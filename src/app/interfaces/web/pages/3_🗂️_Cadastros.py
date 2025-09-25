import streamlit as st
import io
import csv
import sys
from pathlib import Path

ROOT = str(Path(__file__).resolve().parents[5])
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from src.app.infrastructure.repositories import (
    modelo_llm_add, modelo_llm_list, modelo_llm_update, modelo_llm_delete,
    base_conhecimento_add, base_conhecimento_list, base_conhecimento_update, base_conhecimento_delete
)

st.header("🗂️ Cadastros")

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

    # Controles de visualização
    with st.container(border=True):
        st.markdown("**Lista de Modelos LLM**")
    data = modelo_llm_list()
    # Filtros
    fc1, fc2, fc3 = st.columns([2, 1, 1])
    with fc1:
        llm_q = st.text_input("Buscar (Provedor/Modelo)", key="llm_filter_q")
    with fc2:
        llm_status = st.selectbox("Ativo", ["Todos", "Sim", "Não"], key="llm_filter_status")
    with fc3:
        if st.button("Limpar filtros", key="llm_clear_filters"):
            st.session_state["llm_filter_q"] = ""
            st.session_state["llm_filter_status"] = "Todos"
            st.rerun()

    q = (llm_q or "").strip().lower()
    status_sel = llm_status
    def llm_passes(r: dict) -> bool:
        if q:
            if q not in (r.get("modl_provedor", "").lower()) and q not in (r.get("modl_modelo_llm", "").lower()):
                return False
        if status_sel == "Sim" and int(r.get("modl_status", 0)) != 1:
            return False
        if status_sel == "Não" and int(r.get("modl_status", 0)) != 0:
            return False
        return True

    filtered_data = [r for r in data if llm_passes(r)]
    # ordenação padrão: ID desc
    filtered_data.sort(key=lambda r: int(r.get("modl_id", 0)), reverse=True)
    st.caption(f"Mostrando {len(filtered_data)} de {len(data)} registro(s)")
    # Preferências de exibição
    show_keys = st.checkbox("Exibir API Keys", value=st.session_state.get("llm_show_keys", False), key="llm_show_keys")

    # Preparar linhas amigáveis
    friendly_rows = []
    by_id = {r["modl_id"]: r for r in data}
    # recuperar preseleção da sessão
    pre_ids = set(st.session_state.get("llm_preselect_ids", []))
    for r in filtered_data:
        api_val = r.get("modl_api_key", "") if show_keys else ("••••••" if r.get("modl_api_key") else "")
        rec = {
            "Selecionar": (int(r["modl_id"]) in pre_ids),
            "ID": r["modl_id"],
            "Provedor": r["modl_provedor"],
            "Modelo": r["modl_modelo_llm"],
            "API Key": api_val,
            "Ativo": bool(int(r.get("modl_status", 0)) == 1),
        }
        friendly_rows.append(rec)

    edited = st.data_editor(
        friendly_rows,
        num_rows="fixed",
        use_container_width=True,
        column_config={
            "Selecionar": st.column_config.CheckboxColumn("Selecionar"),
            "ID": st.column_config.NumberColumn("ID", disabled=True),
            "Provedor": st.column_config.TextColumn("Provedor"),
            "Modelo": st.column_config.TextColumn("Modelo"),
            "API Key": st.column_config.TextColumn("API Key", disabled=not show_keys),
            "Ativo": st.column_config.CheckboxColumn("Ativo"),
        },
        hide_index=True,
        key="llm_table",
    )

    col_s1, col_s2, col_s3, col_s4 = st.columns([1, 1, 1, 2])
    with col_s1:
        if st.button("Salvar alterações", type="primary", key="llm_save_all"):
            changed = 0
            for row in edited:
                rid = int(row["ID"]) if row.get("ID") is not None else None
                if rid is None:
                    continue
                orig = by_id.get(rid)
                if not orig:
                    continue
                prov_n = row.get("Provedor") or ""
                modelo_n = row.get("Modelo") or ""
                # Quando as chaves estão ocultas, não sobrescrever o valor real
                if show_keys:
                    apikey_n = row.get("API Key") or ""
                else:
                    apikey_n = orig.get("modl_api_key", "")
                ativo_n = 1 if row.get("Ativo") else 0
                if (
                    prov_n != orig["modl_provedor"]
                    or modelo_n != orig["modl_modelo_llm"]
                    or apikey_n != orig.get("modl_api_key", "")
                    or ativo_n != int(orig.get("modl_status", 0))
                ):
                    modelo_llm_update(rid, prov_n, modelo_n, apikey_n, ativo_n)
                    changed += 1
            st.success(f"{changed} registro(s) atualizado(s).")
            st.rerun()
    with col_s2:
        if st.button("Excluir selecionados", key="llm_delete_selected"):
            sel_ids = [int(r["ID"]) for r in edited if r.get("Selecionar")]
            if not sel_ids:
                st.info("Nenhum registro selecionado.")
            else:
                st.session_state["llm_delete_batch"] = sel_ids
    with col_s3:
        if st.button("Selecionar todos", key="llm_select_all"):
            st.session_state["llm_preselect_ids"] = [int(r["modl_id"]) for r in filtered_data]
            st.rerun()
    with col_s4:
        # Exportar CSV do conjunto filtrado
        if st.button("Exportar CSV", key="llm_export"):
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(["ID", "Provedor", "Modelo", "API Key", "Ativo"])
            for r in filtered_data:
                writer.writerow([
                    r.get("modl_id"),
                    r.get("modl_provedor"),
                    r.get("modl_modelo_llm"),
                    (r.get("modl_api_key", "") if show_keys else ("••••••" if r.get("modl_api_key") else "")),
                    1 if int(r.get("modl_status", 0)) == 1 else 0,
                ])
            st.download_button(
                "Baixar CSV (filtrados)",
                data=output.getvalue().encode("utf-8"),
                file_name="modelos_llm.csv",
                mime="text/csv",
                key="llm_download_csv",
            )

    # limpar seleção (sempre disponível ao lado dos botões)
    if st.button("Limpar seleção", key="llm_clear_sel"):
        st.session_state["llm_preselect_ids"] = []
        st.rerun()

    if st.session_state.get("llm_delete_batch"):
        ids = st.session_state["llm_delete_batch"]
        st.warning(f"Confirma excluir {len(ids)} registro(s): {ids}?")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Confirmar exclusão", key="llm_confirm_delete"):
                for rid in ids:
                    modelo_llm_delete(rid)
                st.success(f"{len(ids)} registro(s) excluído(s).")
                st.session_state.pop("llm_delete_batch", None)
                st.rerun()
        with c2:
            if st.button("Cancelar", key="llm_cancel_delete"):
                st.session_state.pop("llm_delete_batch", None)
                st.info("Exclusão cancelada.")

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
    with st.container(border=True):
        st.markdown("**Lista de Bases de Conhecimento**")
    dados = base_conhecimento_list()
    # Filtros
    bc1, bc2, bc3 = st.columns([2, 1, 1])
    with bc1:
        baco_q = st.text_input("Buscar (Nome/Arquivo)", key="baco_filter_q")
    with bc2:
        baco_status = st.selectbox("Ativo", ["Todos", "Sim", "Não"], key="baco_filter_status")
    with bc3:
        if st.button("Limpar filtros", key="baco_clear_filters"):
            st.session_state["baco_filter_q"] = ""
            st.session_state["baco_filter_status"] = "Todos"
            st.rerun()

    bq = (baco_q or "").strip().lower()
    bstatus = baco_status
    def baco_passes(r: dict) -> bool:
        if bq:
            if bq not in (r.get("baco_nome", "").lower()) and bq not in (r.get("baco_arquivo", "").lower()):
                return False
        if bstatus == "Sim" and int(r.get("baco_status", 0)) != 1:
            return False
        if bstatus == "Não" and int(r.get("baco_status", 0)) != 0:
            return False
        return True

    dados_filtered = [r for r in dados if baco_passes(r)]
    dados_filtered.sort(key=lambda r: int(r.get("baco_id", 0)), reverse=True)
    st.caption(f"Mostrando {len(dados_filtered)} de {len(dados)} registro(s)")

    friendly = []
    by_baco_id = {r["baco_id"]: r for r in dados}
    baco_pre_ids = set(st.session_state.get("baco_preselect_ids", []))
    for r in dados_filtered:
        rec = {
            "Selecionar": (int(r["baco_id"]) in baco_pre_ids),
            "ID": r["baco_id"],
            "Nome": r["baco_nome"],
            "Arquivo": r["baco_arquivo"],
            "Descrição": r.get("baco_descricao", ""),
            "Ativo": bool(int(r.get("baco_status", 0)) == 1),
        }
        friendly.append(rec)

    edited_bases = st.data_editor(
        friendly,
        num_rows="fixed",
        use_container_width=True,
        column_config={
            "Selecionar": st.column_config.CheckboxColumn("Selecionar"),
            "ID": st.column_config.NumberColumn("ID", disabled=True),
            "Nome": st.column_config.TextColumn("Nome da Base"),
            "Arquivo": st.column_config.TextColumn("Arquivo (path)"),
            "Descrição": st.column_config.TextColumn("Descrição"),
            "Ativo": st.column_config.CheckboxColumn("Ativo"),
        },
        hide_index=True,
        key="baco_table",
    )

    csave, cdel, cselall, cexport = st.columns([1, 1, 1, 2])
    with csave:
        if st.button("Salvar alterações", type="primary", key="baco_save_all"):
            changed = 0
            for row in edited_bases:
                bid = int(row["ID"]) if row.get("ID") is not None else None
                if bid is None:
                    continue
                orig = by_baco_id.get(bid)
                if not orig:
                    continue
                nome_n = row.get("Nome") or ""
                arq_n = row.get("Arquivo") or ""
                desc_n = row.get("Descrição") or ""
                ativo_n = 1 if row.get("Ativo") else 0
                if (
                    nome_n != orig["baco_nome"]
                    or arq_n != orig["baco_arquivo"]
                    or desc_n != orig.get("baco_descricao", "")
                    or ativo_n != int(orig.get("baco_status", 0))
                ):
                    base_conhecimento_update(bid, nome_n, arq_n, desc_n, ativo_n)
                    changed += 1
            st.success(f"{changed} registro(s) atualizado(s).")
            st.rerun()
    with cdel:
        if st.button("Excluir selecionados", key="baco_delete_selected"):
            sel = [int(r["ID"]) for r in edited_bases if r.get("Selecionar")]
            if not sel:
                st.info("Nenhum registro selecionado.")
            else:
                st.session_state["baco_delete_batch"] = sel
    with cselall:
        if st.button("Selecionar todos", key="baco_select_all"):
            st.session_state["baco_preselect_ids"] = [int(r["baco_id"]) for r in dados_filtered]
            st.rerun()
    with cexport:
        if st.button("Exportar CSV", key="baco_export"):
            out = io.StringIO()
            w = csv.writer(out)
            w.writerow(["ID", "Nome", "Arquivo", "Descrição", "Ativo"])
            for r in dados_filtered:
                w.writerow([
                    r.get("baco_id"), r.get("baco_nome"), r.get("baco_arquivo"), r.get("baco_descricao", ""),
                    1 if int(r.get("baco_status", 0)) == 1 else 0,
                ])
            st.download_button(
                "Baixar CSV (filtrados)",
                data=out.getvalue().encode("utf-8"),
                file_name="bases_conhecimento.csv",
                mime="text/csv",
                key="baco_download_csv",
            )

    if st.button("Limpar seleção", key="baco_clear_sel"):
        st.session_state["baco_preselect_ids"] = []
        st.rerun()

    if st.session_state.get("baco_delete_batch"):
        ids = st.session_state["baco_delete_batch"]
        st.warning(f"Confirma excluir {len(ids)} registro(s): {ids}?")
        b1, b2 = st.columns(2)
        with b1:
            if st.button("Confirmar exclusão", key="baco_confirm_delete"):
                for bid in ids:
                    base_conhecimento_delete(bid)
                st.success(f"{len(ids)} registro(s) excluído(s).")
                st.session_state.pop("baco_delete_batch", None)
                st.rerun()
        with b2:
            if st.button("Cancelar", key="baco_cancel_delete"):
                st.session_state.pop("baco_delete_batch", None)
                st.info("Exclusão cancelada.")


tab_modelos, tab_bases = st.tabs(["Modelos LLM", "Base de Conhecimento"])
with tab_modelos:
    render_modelos()
with tab_bases:
    render_bases()
