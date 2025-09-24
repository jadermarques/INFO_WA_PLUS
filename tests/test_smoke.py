from src.app.infrastructure import db
from src.app.infrastructure import repositories as repo


def test_db_init(tmp_path, monkeypatch):
    test_db = tmp_path / "data.db"
    monkeypatch.setenv("DB_PATH", str(test_db))
    # reload settings via module import
    from importlib import reload
    import src.app.config as config
    reload(config)
    reload(db)

    db.init_db("src/app/infrastructure/schema.sql")

    mid = repo.modelo_llm_add("OPENAI", "gpt-4o-mini", "key")
    assert mid > 0
    bid = repo.base_conhecimento_add("Base", "/tmp/base.txt", "desc")
    assert bid > 0

    modelos = repo.modelo_llm_list()
    bases = repo.base_conhecimento_list()
    assert len(modelos) == 1
    assert len(bases) == 1
