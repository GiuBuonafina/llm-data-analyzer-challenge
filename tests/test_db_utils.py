import pytest
import os
from core import db_utils
from sqlalchemy import create_engine

def test_create_db_engine():
    # Testa se a engine é criada corretamente
    engine = db_utils.create_db_engine("sqlite:///:memory:")
    assert engine is not None

def test_get_schema_empty():
    # Testa se o esquema é retornado como string vazia quando não há esquema
    engine = create_engine("sqlite:///:memory:")
    schema = db_utils.get_schema(engine, schema_name=None)  
    assert isinstance(schema, str)
    assert schema == ""

def test_executar_sql_select():
    # Testa execução de SQL SELECT
    db_path = "test_temp.db"
    # Remove o arquivo antes do teste
    if os.path.exists(db_path):
        os.remove(db_path)
    engine = create_engine(f"sqlite:///{db_path}")
    from sqlalchemy import text
    with engine.begin() as conn: 
        conn.execute(text("CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT);"))
        conn.execute(text("INSERT INTO test (name) VALUES ('Giulia');"))
    df = db_utils.executar_sql(engine, "SELECT * FROM test;")
    assert df is not None
    assert not df.empty
    assert "name" in df.columns
    engine.dispose()
    # Remove o arquivo após o teste
    if os.path.exists(db_path):
        os.remove(db_path)

def test_executar_sql_invalid():
    # Testa execução de SQL inválido
    engine = create_engine("sqlite:///:memory:")
    df = db_utils.executar_sql(engine, "SELECT * FROM non_existing_table;")
    assert df is None