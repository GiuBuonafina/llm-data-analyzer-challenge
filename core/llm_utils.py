import re
from langchain_openai import AzureChatOpenAI

def gerar_sql_llm_chat(user_question, schema, openai_config, sintax, data_dictionary, history):
    """
    Gera uma consulta SQL a partir de uma pergunta em linguagem natural usando LLM.
    """
    llm = AzureChatOpenAI(
        openai_api_key=openai_config["AZURE_OPENAI_API_KEY"],
        azure_endpoint=openai_config["AZURE_OPENAI_ENDPOINT"],
        deployment_name=openai_config["AZURE_OPENAI_DEPLOYMENT_NAME"],
        openai_api_version=openai_config["AZURE_OPENAI_API_VERSION"],
        temperature=0
    )
    history_str = ""
    for role, msg in history:
        history_str += f"<|{role}|>\n{msg}\n"
    prompt = f'''
<|system|>
You are a specialist in creating and building SQL queries. You must follow the syntax rules according to
the engine. You must respond ONLY WITH THE QUERY according to USER. You must strictly follow all RULES.
<|sintax|>
{sintax}
<|rules|>
- Return SQL only
- DO NOT RETURN EXPLANATIONS
- Do not use names that don't exist in the SCHEMA
- FOLLOW SYNTAX RULES in SQL generation
- Create queries based on SCHEMA
- If unable to, return NO_CONTEXT
- The answer MUST ALWAYS be between ```sql and ```
<|schema|>
{schema}
<|data dictionary|>
{data_dictionary}
<|history|>
{history_str}
<|user|>:
{user_question}
<|assistant|>:
'''
    try:
        response = llm.invoke(prompt)
        return response.content.strip()
    except Exception as e:
        print("Erro ao chamar a LLM para gerar SQL:", str(e))
        return "NO_CONTEXT"

def extrair_sql_da_resposta(resposta_llm):
    """
    Extrai e limpa a consulta SQL da resposta da LLM.
    Retorna a string SQL pronta para uso ou lança erro se não encontrar.
    """
    if not resposta_llm or "NO_CONTEXT" in resposta_llm:
        raise ValueError("A LLM não conseguiu gerar uma consulta SQL válida para o contexto fornecido.")

    match = re.search(r"```sql(.*?)```", resposta_llm, re.DOTALL | re.IGNORECASE)
    if match:
        sql = match.group(1).strip()
    else:
        sql = resposta_llm.strip()
    linhas = sql.splitlines()
    linhas_sql = [linha for linha in linhas if not linha.strip().lower().startswith("--")]
    sql_final = "\n".join(linhas_sql).strip()
    if not sql_final.lower().startswith("select"):
        raise ValueError("A resposta da LLM não contém uma consulta SQL SELECT válida.")
    return sql_final

def gerar_resposta_natural(df, user_question, consulta_sql, openai_config, history):
    """
    Gera uma resposta em linguagem natural para o usuário, baseada no DataFrame retornado da consulta SQL,
    na pergunta original e na query SQL gerada.
    """
    llm = AzureChatOpenAI(
        openai_api_key=openai_config["AZURE_OPENAI_API_KEY"],
        azure_endpoint=openai_config["AZURE_OPENAI_ENDPOINT"],
        deployment_name=openai_config["AZURE_OPENAI_DEPLOYMENT_NAME"],
        openai_api_version=openai_config["AZURE_OPENAI_API_VERSION"],
        temperature=0
    )
    history_str = ""
    for role, msg in history:
        history_str += f"<|{role}|>\n{msg}\n"

    df_str = df.to_markdown(index=False) if df is not None and not df.empty else "No results found."
    prompt = f"""
<|system|>
You are a data analyst assistant. Your job is to answer the user's question in clear, natural English, based on the SQL query result below.
Always be concise, objective, and use the data to justify your answer. If the result is empty, explain that no data was found.

<|history|>
{history_str}
<|user_question|>
{user_question}

<|sql_query|>
{consulta_sql}

<|sql_result|>
{df_str}

<|assistant|>
"""
    try:
        response = llm.invoke(prompt)
        return response.content.strip()
    except Exception as e:
        return f"Desculpe, eu não pude gerar uma resposta em linguagem natural. Erro: {str(e)}"

def classificar_mensagem(user_message, openai_config, history):
    """
    Classifica a mensagem do usuário como 'sql_request' ou 'casual_interaction' usando uma LLM.
    """
    llm = AzureChatOpenAI(
        openai_api_key=openai_config["AZURE_OPENAI_API_KEY"],
        azure_endpoint=openai_config["AZURE_OPENAI_ENDPOINT"],
        deployment_name=openai_config["AZURE_OPENAI_DEPLOYMENT_NAME"],
        openai_api_version=openai_config["AZURE_OPENAI_API_VERSION"],
        temperature=0
    )
    
    history_str = ""
    for role, msg in history:
        history_str += f"<|{role}|>\n{msg}\n"

    prompt = f"""
<|system|>
You are an assistant specialized in determining whether a query is a data request or a casual interaction with the user. Your task is to analyze the query and return one of the following fixed responses to classify the query:
If the query is a data request (e.g., "What's the most expensive product?", "How many sales did we have today?", etc.), return: "sql_request"
If the query is a casual interaction, such as a greeting or thank you (e.g., "hi", "thanks", "good afternoon", etc.), return: "casual_interaction"

Important: Only return "sql_request" or "casual_interaction" and nothing else. Do not provide explanations or additional context. Simply classify the query according to the examples above.

<|history|>
{history_str}

<|user|>
{user_message}

<|assistant|>
"""
    try:
        response = llm.invoke(prompt)
        return response.content.strip().lower()
    except Exception as e:
        print("Erro ao classificar mensagem:", str(e))
        return "casual_interaction"

def responder_casual_interaction(history, user_message, openai_config):
    """
    Responde a interações casuais usando uma LLM, considerando o histórico de mensagens.
    Não conversa sobre assuntos que não tenham relação com análise de dados, negócios ou perguntas sobre o sistema.
    """
    llm = AzureChatOpenAI(
        openai_api_key=openai_config["AZURE_OPENAI_API_KEY"],
        azure_endpoint=openai_config["AZURE_OPENAI_ENDPOINT"],
        deployment_name=openai_config["AZURE_OPENAI_DEPLOYMENT_NAME"],
        openai_api_version=openai_config["AZURE_OPENAI_API_VERSION"]
    )
    history_str = ""
    for role, msg in history:
        history_str += f"<|{role}|>\n{msg}\n"
    prompt = f"""
<|system|>
You are a friendly data analyst assistant. Respond to the user's last message in a natural and polite way, considering the conversation history.
Do not engage in conversations that are not related to data analysis, business insights, or questions about the system. Politely redirect the user if the topic is not relevant.

<|history|>
{history_str}
<|user|>
{user_message}

<|assistant|>
"""
    try:
        response = llm.invoke(prompt)
        return response.content.strip()
    except Exception as e:
        return f"Desculpe, eu não puder responder devido ao erro: {str(e)}"