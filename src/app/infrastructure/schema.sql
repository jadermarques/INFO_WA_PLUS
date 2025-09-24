-- schema for INFO_WA_PLUS
CREATE TABLE IF NOT EXISTS modelo_llm (
  modl_id INTEGER PRIMARY KEY AUTOINCREMENT,
  modl_provedor TEXT NOT NULL,
  modl_modelo_llm TEXT NOT NULL,
  modl_api_key TEXT NOT NULL,
  modl_status INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS base_conhecimento (
  baco_id INTEGER PRIMARY KEY AUTOINCREMENT,
  baco_nome TEXT NOT NULL,
  baco_arquivo TEXT NOT NULL,
  baco_descricao TEXT NOT NULL,
  baco_status INTEGER DEFAULT 1
);
