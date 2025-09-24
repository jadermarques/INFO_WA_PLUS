from __future__ import annotations
from typing import Optional

from .db import execute, query_all


# modelo_llm repo

def modelo_llm_add(provedor: str, modelo: str, api_key: str, status: int = 1) -> int:
    sql = (
        "INSERT INTO modelo_llm (modl_provedor, modl_modelo_llm, modl_api_key, modl_status)"
        " VALUES (?, ?, ?, ?)"
    )
    return execute(sql, (provedor, modelo, api_key, status))


def modelo_llm_list(only_active: bool = False) -> list[dict]:
    sql = "SELECT * FROM modelo_llm" + (" WHERE modl_status=1" if only_active else "")
    rows = query_all(sql)
    return [dict(row) for row in rows]


# base_conhecimento repo

def base_conhecimento_add(nome: str, arquivo: str, descricao: str, status: int = 1) -> int:
    sql = (
        "INSERT INTO base_conhecimento (baco_nome, baco_arquivo, baco_descricao, baco_status)"
        " VALUES (?, ?, ?, ?)"
    )
    return execute(sql, (nome, arquivo, descricao, status))


def base_conhecimento_list(only_active: bool = False) -> list[dict]:
    sql = "SELECT * FROM base_conhecimento" + (" WHERE baco_status=1" if only_active else "")
    rows = query_all(sql)
    return [dict(row) for row in rows]
