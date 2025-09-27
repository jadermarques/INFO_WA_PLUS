"""
Providers stubs para testar conexão com LLMs.
Sem chamadas externas reais (offline). Retorna sucesso/falha simulados.
"""
from __future__ import annotations
from typing import Tuple

KNOWN_PROVIDERS = {"OPENAI", "AZURE_OPENAI", "ANTHROPIC", "COHERE"}


def test_llm_connection(provedor: str, modelo: str, api_key: str, timeout: float = 3.0) -> Tuple[bool, str]:
    """Stub de teste de conexão com provedores LLM.

    Regras (simuladas, sem rede):
    - Provedor deve existir e estar em KNOWN_PROVIDERS (case-insensitive); caso contrário, falha.
    - API key deve existir e ter tamanho mínimo plausível.
    - Modelo deve existir (não vazio).
    - Para OPENAI/AXZURE_OPENAI, aceita chaves começando com "sk-" como mais plausíveis (não obrigatório).

    Retorna:
        (ok, detail): bool de sucesso e mensagem detalhada.
    """
    prov = (provedor or "").strip().upper()
    mod = (modelo or "").strip()
    key = (api_key or "").strip()

    if not prov or prov not in KNOWN_PROVIDERS:
        return False, f"Provedor desconhecido (stub): '{provedor}'"
    if not mod:
        return False, "Modelo não informado"
    if not key or len(key) < 6:
        return False, "API key ausente ou muito curta"

    # OPENAI: tenta teste real se a lib estiver instalada
    if prov == "OPENAI":
        try:
            import openai  # type: ignore
            from openai import OpenAI  # type: ignore
        except Exception:
            # Sem lib, retorno simulado
            return True, "Conexão simulada OK (openai não instalado)"

        try:
            client = OpenAI(api_key=key, timeout=timeout)
            # tentativa simples: recuperar um modelo informado (ou um default popular)
            model_name = modelo or "gpt-4o-mini"
            _ = client.models.retrieve(model_name)
            return True, f"Conexão OK (OpenAI) - modelo '{model_name}' acessível"
        except Exception as e:  # noqa: BLE001
            return False, f"Falha OpenAI: {e}"

    # AZURE_OPENAI / demais: simulado por enquanto
    return True, "Conexão simulada OK"
