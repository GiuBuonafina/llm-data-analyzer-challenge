import pandas as pd
from sqlalchemy import create_engine, inspect
from sqlalchemy.exc import SQLAlchemyError

def create_db_engine(db_uri):
    return create_engine(db_uri)

def get_schema(engine, schema_name="dbo"):
    """
    Retorna o schema do banco de dados (tabelas e colunas).
    """
    inspector = inspect(engine)
    schema_str = ""
    for table_name in inspector.get_table_names(schema=schema_name):
        columns = inspector.get_columns(table_name, schema=schema_name)
        col_infos = [f"{col['name']} ({col['type']})" for col in columns]
        schema_str += f"Tabela {table_name}: {', '.join(col_infos)}\n"
    return schema_str

def executar_sql(engine, consulta_sql):
    """
    Executa a consulta SQL no banco usando SQLAlchemy e retorna um DataFrame.
    Trata erros comuns e retorna mensagens amigáveis.
    """
    try:
        df = pd.read_sql_query(consulta_sql, engine)
        return df
    except SQLAlchemyError as e:
        print("Erro ao executar a consulta SQL:", str(e))
        return None
    except Exception as e:
        print("Erro inesperado:", str(e))
        return None