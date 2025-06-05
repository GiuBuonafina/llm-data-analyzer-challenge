import pytest
from core import llm_utils
from unittest.mock import MagicMock, patch

def test_extrair_sql_da_resposta_valida():
    # Testa se a função extrai corretamente uma consulta SQL válida
    resposta = "```sql\nSELECT * FROM tabela;\n```"
    sql = llm_utils.extrair_sql_da_resposta(resposta)
    assert sql.strip().lower().startswith("select")

def test_extrair_sql_da_resposta_invalida():
    # Testa se a função lança erro para resposta inválida
    with pytest.raises(ValueError):
        llm_utils.extrair_sql_da_resposta("NO_CONTEXT")

def test_extrair_sql_da_resposta_sem_select():
    # Testa se a função lança erro quando não encontra uma consulta SQL SELECT
    with pytest.raises(ValueError):
        llm_utils.extrair_sql_da_resposta("```sql\nDELETE FROM tabela;\n```")

# Para funções que usam LLM, usamos mock:
@patch("core.llm_utils.AzureChatOpenAI")
def test_classificar_mensagem_sql_request(mock_llm):
    # Testa se a função classifica corretamente uma mensagem como sql_request
    mock_llm.return_value.invoke.return_value.content = "sql_request"
    result = llm_utils.classificar_mensagem("Qual a média de idade?", {"AZURE_OPENAI_API_KEY": "fake", "AZURE_OPENAI_ENDPOINT": "fake", "AZURE_OPENAI_DEPLOYMENT_NAME": "fake", "AZURE_OPENAI_API_VERSION": "fake"}, [])
    assert result == "sql_request"