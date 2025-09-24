from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, List

@dataclass
class AnalysisInput:
    raw_text: str

@dataclass
class SpecialistOutput:
    name: str
    report: Dict[str, Any]


def preparar_dados(input_text: str) -> Dict[str, Any]:
    # Stub: transforma texto em JSON simples
    lines = [l.strip() for l in input_text.splitlines() if l.strip()]
    return {
        "messages": lines,
        "length": len(input_text),
        "lines": len(lines),
    }


def especialista_metricas(data: Dict[str, Any]) -> SpecialistOutput:
    msgs = data.get("messages", [])
    return SpecialistOutput(
        name="metricas",
        report={
            "qtd_mensagens": len(msgs),
            "tam_texto": data.get("length", 0),
            "tempo_primeira_resposta": 25,  # mock
        },
    )


def especialista_sentimento(data: Dict[str, Any]) -> SpecialistOutput:
    msgs = data.get("messages", [])
    sentimento = "neutro"
    if any("obrigado" in m.lower() for m in msgs):
        sentimento = "positivo"
    return SpecialistOutput(name="sentimento", report={"sentimento": sentimento})


def especialista_resolucao(data: Dict[str, Any]) -> SpecialistOutput:
    msgs = data.get("messages", [])
    resolvido = any("resolvido" in m.lower() for m in msgs)
    return SpecialistOutput(name="resolucao", report={"status_resolucao": "resolvido" if resolvido else "nao_resolvido"})


def lider_sintese(data_json: Dict[str, Any], especialistas: List[SpecialistOutput]) -> Dict[str, Any]:
    combined = {o.name: o.report for o in especialistas}
    contradicao = False
    if combined.get("sentimento", {}).get("sentimento") == "positivo" and combined.get("resolucao", {}).get("status_resolucao") == "nao_resolvido":
        contradicao = True
    relatorio = {
        "resumo": "Relatório consolidado (stub)",
        "contradicao_detectada": contradicao,
        "insights": combined,
    }
    return relatorio


def pipeline_analise(input_text: str) -> Dict[str, Any]:
    data_json = preparar_dados(input_text)
    outs = [
        especialista_metricas(data_json),
        especialista_sentimento(data_json),
        especialista_resolucao(data_json),
    ]
    final = lider_sintese(data_json, outs)
    return final
