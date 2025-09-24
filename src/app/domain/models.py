from __future__ import annotations
from dataclasses import dataclass


@dataclass(slots=True)
class ModeloLLM:
    modl_id: int | None
    modl_provedor: str
    modl_modelo_llm: str
    modl_api_key: str
    modl_status: int = 1


@dataclass(slots=True)
class BaseConhecimento:
    baco_id: int | None
    baco_nome: str
    baco_arquivo: str
    baco_descricao: str
    baco_status: int = 1
