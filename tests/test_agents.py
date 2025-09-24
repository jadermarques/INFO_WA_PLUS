from src.app.infrastructure.agents import (
    preparar_dados,
    especialista_metricas,
    especialista_sentimento,
    especialista_resolucao,
    lider_sintese,
    pipeline_analise,
)


def test_pipeline_stub():
    text = "Oi, obrigado. Problema não resolvido."
    result = pipeline_analise(text)
    assert "insights" in result
    assert "metricas" in result["insights"]
    assert "contradicao_detectada" in result


def test_agents_individuals():
    data = preparar_dados("Obrigado, mas ainda não resolvido")
    m = especialista_metricas(data)
    s = especialista_sentimento(data)
    r = especialista_resolucao(data)
    final = lider_sintese(data, [m, s, r])
    assert m.name == "metricas"
    assert s.name == "sentimento"
    assert r.name == "resolucao"
    assert isinstance(final, dict)
